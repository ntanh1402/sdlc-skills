"""Rename a concept or a Requirement and every reference to it.

A concept is renamed by moving its file or folder. Every link in the bundle that
points at it is rewritten, and every whole-token mention of the old key in its
application's files. A Requirement is renamed in the headings of the Feature and
the ChangeRequests that carry it, in every link to its anchor, and in mentions
in its application's files. `index.md` files and generated sections are left
to `sync`, which runs last.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from . import git, markdown, sync
from .bundle import Bundle, Concept
from .errors import Refused, ToolError
from .rules.ids import NAME, changed_feature, feature_slug, requirement_ids
from .schema import Schema


def token(key: str) -> re.Pattern:
    """`key` as a whole token: not part of a longer key or word."""
    return re.compile(rf"(?<![A-Za-z0-9_-]){re.escape(key)}(?![A-Za-z0-9_-])")


@dataclass
class Plan:
    kind: str  # "concept" or "requirement"
    old: str
    new: str
    app: str
    holders: list[Concept] = field(default_factory=list)  # files whose anchor is renamed
    source: Path | None = None  # file or folder to move
    destination: Path | None = None
    scope: list[Path] = field(default_factory=list)  # files where mentions are replaced


class Base:
    """The default branch of the git repository holding the bundle, when there is one."""

    def __init__(self, root: Path):
        self.root = root
        self.ref: str | None = None
        if git.is_repository(root):
            self.ref = git.default_branch(root)
            self.top = git.toplevel(root).resolve()

    def path(self, path: Path) -> str:
        return path.resolve().relative_to(self.top).as_posix()

    def exists(self, path: Path) -> bool:
        return self.ref is not None and git.exists_at(self.root, self.ref, self.path(path))

    def text(self, path: Path) -> str:
        if self.ref is None:
            return ""
        return git.show(self.root, self.ref, self.path(path)) or ""

    def names(self, directory: Path) -> set[str]:
        """Every file and folder name under `directory` at the default branch."""
        if self.ref is None:
            return set()
        listed = git.run(
            self.root, "ls-tree", "-r", "--name-only", "--full-tree", self.ref, "--", self.path(directory) + "/"
        ).stdout
        return {part for line in listed.split("\n") if line for part in line.split("/")}


def _app_files(bundle: Bundle, app: str) -> list[Path]:
    return [path for path in bundle.markdown_files() if bundle.rel(path).split("/")[0] == app and path.name != "index.md"]


def _plan_concept(bundle: Bundle, base: Base, old: str, new: str, app: str | None, allow_merged: bool) -> Plan:
    schema = bundle.schema
    found = [c for c in bundle.concepts if c.key == old and (app is None or c.app == app)]
    if not found:
        raise Refused(f"no concept or requirement has the key {old}")
    if len(found) > 1:
        raise ToolError(f"{old} names {len(found)} concepts ({', '.join(c.rel for c in found)}): pass --app")
    concept = found[0]
    prefix = schema.types[concept.type].get("prefix")
    if not prefix:
        raise Refused(f"a {concept.type} has a fixed key; only concepts with a key prefix and Requirements can be renamed")
    pattern = schema.key_pattern(concept.type)
    if not new.startswith(prefix) or not re.match(pattern, new):
        raise Refused(f"{new} is not a {concept.type} key: it must match {pattern}")
    source = concept.folder or concept.path
    destination = source.with_name(new if concept.folder else f"{new}.md")
    app_dir = bundle.root / concept.app
    taken = any(c.key == new and c.app == concept.app and c.type == concept.type for c in bundle.concepts)
    if taken or destination.exists() or {new, f"{new}.md"} & base.names(app_dir):
        raise Refused(f"{new} already exists in this draft or on {base.ref}")
    if not allow_merged and base.exists(concept.path):
        raise Refused(f"{old} is on {base.ref}; keys do not change after they are merged (--allow-merged overrides)")
    return Plan("concept", old, new, concept.app, [concept], source, destination, _app_files(bundle, concept.app))


def _plan_requirement(
    bundle: Bundle, base: Base, old: str, new: str, app: str | None, change: str | None, allow_merged: bool
) -> Plan:
    holders: dict[str, list[Concept]] = {}  # Feature path -> the Feature and ChangeRequests carrying `old`
    features: dict[str, Concept] = {}
    for concept in bundle.of_type("Feature", "ChangeRequest"):
        if app is not None and concept.app != app:
            continue
        feature = concept if concept.type == "Feature" else changed_feature(bundle, concept)
        if feature is None:
            continue
        features[feature.rel] = feature
        if old in requirement_ids(concept) and (change is None or concept.key == change):
            holders.setdefault(feature.rel, []).append(concept)
    if not holders:
        where = f" in {change}" if change else ""
        raise Refused(f"no concept or requirement has the key {old}{where}")
    if len(holders) > 1:
        raise ToolError(f"{old} belongs to {len(holders)} Features ({', '.join(holders)}): pass --app")
    feature_rel, carriers = next(iter(holders.items()))
    feature = features[feature_rel]
    name = feature_slug(feature)
    if not re.match(rf"^REQ-{re.escape(name)}-{NAME}$", new):
        raise Refused(f"{new} must be REQ-{name}-<name>, lower-case words joined by -, because it belongs to {feature.key}")
    family = [feature] + [c for c in bundle.of_type("ChangeRequest") if changed_feature(bundle, c) is feature]
    heading = re.compile(rf"^### {re.escape(new)}\s*$", re.MULTILINE)
    if any(new in requirement_ids(c) or heading.search(base.text(c.path)) for c in family):
        raise Refused(f"{new} already exists in this draft or on {base.ref}")
    merged = re.compile(rf"^### {re.escape(old)}\s*$", re.MULTILINE)
    if not allow_merged and any(merged.search(base.text(c.path)) for c in carriers):
        raise Refused(f"{old} is on {base.ref}; keys do not change after they are merged (--allow-merged overrides)")
    if change is not None:
        folder = carriers[0].folder
        scope = [path for path in bundle.markdown_files() if path.parent == folder and path.name != "index.md"]
    else:
        scope = _app_files(bundle, feature.app)
    return Plan("requirement", old, new, feature.app, carriers, scope=scope)


def _points_at(bundle: Bundle, plan: Plan, source: Path, target: str) -> bool:
    path, anchor = bundle.resolve(source, target)
    if path is None:
        return False
    if plan.kind == "concept":
        moved = plan.source
        return path == moved or moved in path.parents
    return any(path == holder.path for holder in plan.holders) and anchor.lower() == plan.old.lower()


def _rewrite_link(plan: Plan, label: str, target: str) -> tuple[str, str]:
    old, new = token(plan.old), plan.new
    label = old.sub(new, label)
    if plan.kind == "concept":
        raw, hash_, anchor = target.partition("#")
        return label, old.sub(new, raw) + hash_ + anchor
    raw, _, _ = target.partition("#")
    return label, f"{raw}#{markdown.slug(new)}"


def _rewrite(bundle: Bundle, plan: Plan, path: Path, in_scope: bool) -> str:
    text = bundle.text(path)
    pieces: list[str] = []
    position = 0
    for match in markdown.link_spans(text):
        if not _points_at(bundle, plan, path, text[match.start(2) : match.end(2)]):
            continue
        label, target = _rewrite_link(plan, text[match.start(1) : match.end(1)], text[match.start(2) : match.end(2)])
        pieces += [text[position : match.start(1)], label, text[match.end(1) : match.start(2)], target]
        position = match.end(2)
    pieces.append(text[position:])
    text = "".join(pieces)
    if in_scope:
        text = token(plan.old).sub(plan.new, text)
    return text


def rename(root: Path, old: str, new: str, *, app: str | None = None, change: str | None = None,
           allow_merged: bool = False, schema: Schema | None = None) -> dict:
    schema = schema or Schema.load()
    bundle = Bundle.load(root, schema)
    base = Base(root)
    if old.startswith("REQ-"):
        plan = _plan_requirement(bundle, base, old, new, app, change, allow_merged)
    else:
        if change is not None:
            raise ToolError("--change applies to a Requirement key only")
        plan = _plan_concept(bundle, base, old, new, app, allow_merged)

    scope = set(plan.scope)
    rewritten: list[Path] = []
    for path in bundle.markdown_files():
        if path.name == "index.md" or path in bundle.unreadable:
            continue
        text = _rewrite(bundle, plan, path, path in scope)
        if text != bundle.text(path):
            path.write_text(text, encoding="utf-8")
            rewritten.append(path)

    moved = None
    if plan.source is not None:
        plan.source.rename(plan.destination)
        moved = {"from": bundle.rel(plan.source), "to": bundle.rel(plan.destination)}

        def after(path: Path) -> Path:
            inside = path == plan.source or plan.source in path.parents
            return plan.destination / path.relative_to(plan.source) if inside else path

        rewritten = [after(path) for path in rewritten]
    synced = sync.write(root, schema)
    return {
        "ok": True,
        "kind": plan.kind,
        "old": old,
        "new": new,
        "moved": moved,
        "rewritten": sorted(bundle.rel(path) for path in rewritten),
        "synced": [bundle.rel(path) for path in synced],
    }

