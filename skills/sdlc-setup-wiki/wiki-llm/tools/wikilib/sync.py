"""Write the parts of a bundle that are derived from other parts.

Two kinds of generated content:
  * every `index.md`, written whole;
  * sections whose heading spec in schema.json has a `generated` block,
    written between that heading and the next heading of the same level.
"""

from __future__ import annotations

import os
from pathlib import Path

from . import frontmatter, markdown
from .bundle import Bundle, Concept
from .schema import Schema


def _link(target: Path, source_dir: Path) -> str:
    return Path(os.path.relpath(target, source_dir)).as_posix()


def _entry(title: str, link: str, description: str) -> str:
    return f"* [{title}]({link}) - {description}" if description else f"* [{title}]({link})"


def _page(blocks: list[tuple[str, list[str]]], header: str = "") -> str:
    parts = []
    for heading, lines in blocks:
        parts.append(f"# {heading}\n\n" + "\n".join(lines or ["None"]) + "\n")
    return header + "\n".join(parts)


# --- indexes -------------------------------------------------------------------


def _root_index(bundle: Bundle) -> str:
    header = f'---\nokf_version: "{bundle.schema.okf_version}"\nschema_version: "{bundle.schema.version}"\n---\n\n'
    lines = [_entry(app.title, f"{app.key}/overview.md", app.description) for app in bundle.of_type("Application")]
    return _page([("Applications", lines)], header)


def _app_index(bundle: Bundle, app: Concept) -> str:
    own = [_entry("Overview", "overview.md", app.description)]
    for owned in sorted(bundle.owned(app), key=lambda item: item.path.name):
        own.append(_entry(owned.title, owned.path.name, owned.description))
    collections = [
        _entry(entry["title"], f"{entry['dir']}/index.md", entry["description"])
        for entry in bundle.schema.collections
        if (app.folder / entry["dir"]).is_dir()
    ]
    return _page([(app.title, own), ("Collections", collections)])


def _collection_index(bundle: Bundle, directory: Path, collection: dict) -> str:
    members = [
        concept
        for concept in bundle.of_type(*collection["types"])
        if (concept.folder or concept.path).parent == directory
    ]
    lines = [
        _entry(concept.title, _link(concept.path, directory), concept.description)
        for concept in sorted(members, key=lambda item: item.key)
    ]
    return _page([(collection["title"], lines)])


def _concept_index(bundle: Bundle, concept: Concept) -> str:
    spec = bundle.schema.types[concept.type]
    blocks: list[tuple[str, list[str]]] = [(concept.title, [_entry("Overview", "overview.md", concept.description)])]
    for owned_type in spec.get("owns", []):
        owned = sorted(bundle.owned(concept, owned_type), key=lambda item: item.key)
        if owned:
            plural = bundle.schema.types[owned_type]["plural"]
            blocks.append((plural, [_entry(item.title, item.path.name, item.description) for item in owned]))
    extra = [_entry(entry["name"], entry["name"], entry["description"]) for entry in spec.get("extra_files", [])]
    if extra:
        blocks.append(("Files", extra))
    if spec.get("log", True):
        blocks.append(("History", [_entry("Change log", "log.md", f"History of {concept.title}.")]))
    return _page(blocks)


def _indexes(bundle: Bundle) -> dict[Path, str]:
    result: dict[Path, str] = {bundle.root / "index.md": _root_index(bundle)}
    for app in bundle.of_type("Application"):
        result[app.folder / "index.md"] = _app_index(bundle, app)
        for collection in bundle.schema.collections:
            directory = app.folder / collection["dir"]
            if directory.is_dir():
                result[directory / "index.md"] = _collection_index(bundle, directory, collection)
    for concept in bundle.concepts:
        if concept.folder is not None and concept.type != "Application":
            result[concept.folder / "index.md"] = _concept_index(bundle, concept)
    return result


# --- generated sections ----------------------------------------------------------


def _merge(labels: set[str]) -> str:
    if "rw" in labels or {"read", "write"} <= labels:
        return "rw"
    return next(iter(sorted(labels)), "")


def entries(bundle: Bundle, concept: Concept, spec: dict) -> list[str]:
    """List lines of one generated section of `concept`."""
    found: dict[Path, tuple[Concept, set[str]]] = {}
    for source in spec["generated"]["sources"]:
        candidates = bundle.concepts if source["type"] == "@any" else bundle.of_type(source["type"])
        for candidate in candidates:
            for relation in bundle.relations(candidate, source["heading"]):
                if relation.concept is not concept:
                    continue
                label = source.get("label")
                if label == "@qualifier":
                    label = relation.qualifier
                labels = found.setdefault(candidate.path, (candidate, set()))[1]
                if label:
                    labels.add(label)
    lines = []
    for candidate, labels in sorted(found.values(), key=lambda pair: (pair[0].key, pair[0].rel)):
        label = _merge(labels)
        line = f"* [{candidate.title}]({_link(candidate.path, concept.path.parent)})"
        lines.append(f"{line} — {label}" if label else line)
    return lines


def apply_section(body: str, name: str, content: list[str] | None, order: list[str]) -> str:
    """Return `body` with section `# name` holding `content`; None removes the section."""
    lines = body.split("\n")
    top = markdown.sections(body, 1)
    existing = next((section for section in top if section.heading.title == name), None)
    if existing is not None:
        if content is None:
            del lines[existing.heading.line : existing.end]
        else:
            lines[existing.start : existing.end] = ["", *content, ""]
    elif content is not None:
        position = order.index(name)
        later = [s for s in top if s.heading.title in order and order.index(s.heading.title) > position]
        block = [f"# {name}", "", *content, ""]
        if later:
            lines[later[0].heading.line : later[0].heading.line] = block
        else:
            while lines and not lines[-1].strip():
                lines.pop()
            lines.extend(["", *block])
    return "\n".join(lines).rstrip("\n") + "\n"


def _sections(bundle: Bundle) -> tuple[dict[Path, str], list[Path], list[Path]]:
    """Text of every file with generated sections; the files left alone because
    writing them twice would not give the same text; and every file left alone
    for any reason (those, files that are not UTF-8, and files with an open fence)."""
    result: dict[Path, str] = {}
    unstable: list[Path] = []
    skipped: list[Path] = []
    for concept in bundle.concepts:
        specs = bundle.schema.headings(concept.type)
        generated = [spec for spec in specs if "generated" in spec]
        if not generated:
            continue
        if concept.path in bundle.unreadable:
            skipped.append(concept.path)
            continue  # bytes the tool could not read are never written back; reported by layout.encoding
        order = [spec["name"] for spec in specs]
        text = bundle.text(concept.path)
        _, body = frontmatter.split(text)
        if markdown.unclosed_fence(body) is not None:
            skipped.append(concept.path)
            continue  # headings cannot be told from code; reported by content.fence
        prefix = text[: len(text) - len(body)]
        contents: list[tuple[str, list[str] | None]] = []
        for spec in generated:
            content: list[str] | None = entries(bundle, concept, spec)
            if not content:
                content = ["None"] if spec["generated"].get("when_empty", "none") == "none" else None
            contents.append((spec["name"], content))

        def apply(current: str) -> str:
            for name, content in contents:
                current = apply_section(current, name, content, order)
            return current

        body = apply(body)
        if apply(body) != body:
            unstable.append(concept.path)
            skipped.append(concept.path)
            continue
        result[concept.path] = prefix + body
    return result, unstable, skipped


# --- public API --------------------------------------------------------------------


def plan(bundle: Bundle) -> tuple[dict[Path, str], list[Path], list[Path]]:
    """Every generated file path with the full text it should have; the files
    `sync` leaves alone because a second run would change them again; and every
    file with tool-written sections that `sync` leaves alone."""
    result = _indexes(bundle)
    sections, unstable, skipped = _sections(bundle)
    result.update(sections)
    return result, sorted(unstable), sorted(skipped)


def render(bundle: Bundle) -> dict[Path, str]:
    """Every generated file path with the full text it should have."""
    return plan(bundle)[0]


def stale(bundle: Bundle, rendered: dict[Path, str] | None = None) -> list[Path]:
    """Paths whose content differs from what `render` produces. A file that is
    not UTF-8 is never one of them: `sync` does not write over bytes it cannot read."""
    if rendered is None:
        rendered = render(bundle)

    def differs(path: Path, text: str) -> bool:
        if not path.is_file():
            return True
        current = bundle.text(path)
        return path not in bundle.unreadable and current != text

    return sorted(path for path, text in rendered.items() if differs(path, text))


def write(root: Path, schema: Schema | None = None) -> list[Path]:
    """Bring generated content up to date. Returns the paths that changed."""
    bundle = Bundle.load(root, schema or Schema.load())
    rendered = render(bundle)
    changed = stale(bundle, rendered)
    for path in changed:
        path.write_text(rendered[path], encoding="utf-8")
    return changed
