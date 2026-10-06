"""Drafts: a skill's or a person's unapproved changes on their own branch.

A Draft is a branch `wiki/<key>` checked out in a worktree `.worktrees/<key>/`
of the Wiki repository. `start` and `resume` make the worktree; the writer edits
files in it; `finish` stamps provenance, checks log entries, syncs and
validates (a person confirms every changed file, or every one except those
named as unverified); `diff` shows the change set; `commit` commits, pushes and removes
the worktree. `refresh` merges the default branch in, and `verify` records a
person's confirmation of one file.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from . import frontmatter, git, locate, stamps, sync, validate
from .bundle import Bundle
from .errors import Refused, ToolError
from .rules.fields import ACTOR_RE
from .schema import Schema

BUNDLE_DIR = "wiki"
WORKTREES = ".worktrees"
# Paths a Draft may commit: the bundle, and what sdlc-setup-wiki writes
# (the Workspace note goes into AGENTS.md and CLAUDE.md of a Wiki repository
# that is its own Workspace).
COMMITTED = (BUNDLE_DIR, ".wiki-llm", ".gitignore", "README.md", "AGENTS.md", "CLAUDE.md")
KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
RECORD = "wiki-llm-finish.json"
# A skill keeps its Run plan in this file at the root of the Draft worktree.
RUN_PLAN = "plan.md"


# --- where things are ------------------------------------------------------------


def main_root(cwd: Path) -> Path:
    """The main working tree of the repository that contains `cwd`."""
    git.toplevel(cwd)
    common = Path(git.out(cwd, "rev-parse", "--path-format=absolute", "--git-common-dir"))
    return common.parent


def _branch(key: str, branch: str | None) -> str:
    if not KEY_RE.match(key):
        raise ToolError(f"a draft key is letters, digits, '.', '_' and '-': {key}")
    return branch or f"wiki/{key}"


def _fetch(repo: Path) -> None:
    if git.has_remote(repo):
        git.run(repo, "fetch", "--quiet", "origin")


@dataclass
class Worktree:
    """The Draft worktree that contains the current directory."""

    path: Path
    repo: Path
    branch: str

    @classmethod
    def here(cls, cwd: Path) -> "Worktree":
        top = git.toplevel(cwd)
        repo = main_root(cwd)
        if top.resolve() == repo.resolve():
            raise ToolError(f"run this inside a draft worktree ({WORKTREES}/<key>/); start one with: draft start <key>")
        branch = git.out(top, "branch", "--show-current")
        if not branch:
            raise ToolError("the draft worktree is not on a branch")
        return cls(top, repo, branch)

    @property
    def bundle(self) -> Path:
        return self.path / BUNDLE_DIR

    def git_dir(self) -> Path:
        return Path(git.out(self.path, "rev-parse", "--path-format=absolute", "--git-dir"))

    def merge_base(self, base: str) -> str:
        return git.out(self.path, "merge-base", "HEAD", base)


# --- start, resume, discard ------------------------------------------------------


def _ignore_run_plan(repo: Path) -> None:
    """Make git ignore <worktree>/plan.md, so finish, diff, commit and refresh never see it.

    The rule goes into the repository's own info/exclude, which every worktree
    shares and no commit carries."""
    exclude = Path(git.out(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")) / "info" / "exclude"
    line = f"/{RUN_PLAN}"
    text = exclude.read_text(encoding="utf-8") if exclude.is_file() else ""
    if line in text.splitlines():
        return
    exclude.parent.mkdir(parents=True, exist_ok=True)
    exclude.write_text(text + ("\n" if text and not text.endswith("\n") else "") + line + "\n", encoding="utf-8")


def start(cwd: Path, key: str, branch: str | None = None) -> dict:
    repo = main_root(cwd)
    name = _branch(key, branch)
    _fetch(repo)
    base = git.default_branch(repo)
    if git.has_ref(repo, f"refs/heads/{name}") or git.has_ref(repo, f"refs/remotes/origin/{name}"):
        raise Refused(f"branch {name} exists: use draft resume {key}")
    worktree = Path(WORKTREES) / key
    if (repo / worktree).exists():
        raise Refused(f"{worktree.as_posix()} exists: use draft resume {key}, or draft discard {key}")
    _ignore_run_plan(repo)
    git.run(repo, "worktree", "add", "--quiet", "--no-track", "-b", name, worktree.as_posix(), base)
    return {"ok": True, "branch": name, "worktree": worktree.as_posix(), "base": base}


def resume(cwd: Path, key: str, branch: str | None = None) -> dict:
    repo = main_root(cwd)
    name = _branch(key, branch)
    worktree = Path(WORKTREES) / key
    _ignore_run_plan(repo)
    if (repo / worktree).exists():
        return {"ok": True, "branch": name, "worktree": worktree.as_posix(), "base": git.default_branch(repo), "existing": True}
    _fetch(repo)
    if git.has_ref(repo, f"refs/heads/{name}"):
        git.run(repo, "worktree", "add", "--quiet", worktree.as_posix(), name)
    elif git.has_ref(repo, f"refs/remotes/origin/{name}"):
        git.run(repo, "worktree", "add", "--quiet", "--track", "-b", name, worktree.as_posix(), f"origin/{name}")
    else:
        raise Refused(f"no draft branch {name}, locally or on the remote: use draft start {key}")
    return {"ok": True, "branch": name, "worktree": worktree.as_posix(), "base": git.default_branch(repo), "existing": False}


def discard(cwd: Path, key: str, branch: str | None = None, remote: bool = False) -> dict:
    repo = main_root(cwd)
    name = _branch(key, branch)
    worktree = repo / WORKTREES / key
    removed = worktree.exists()
    if removed:
        git.run(repo, "worktree", "remove", "--force", str(worktree))
    git.run(repo, "worktree", "prune")
    deleted = git.has_ref(repo, f"refs/heads/{name}")
    if deleted:
        git.run(repo, "branch", "-D", name)
    deleted_remote = False
    if remote and git.has_remote(repo):
        if git.ok(repo, "ls-remote", "--exit-code", "--heads", "origin", name):
            git.run(repo, "push", "--quiet", "origin", "--delete", name)
            deleted_remote = True
    return {"ok": True, "branch": name, "removed_worktree": removed, "deleted_branch": deleted, "deleted_remote": deleted_remote}


# --- changed files ---------------------------------------------------------------


def changes(tree: Worktree, base_commit: str, paths: tuple[str, ...] = ()) -> dict[str, str]:
    """{repository path: A, M or D} between `base_commit` and the working tree,
    untracked files included."""
    spec = ["--", *paths] if paths else []
    result: dict[str, str] = {}
    listed = git.out(tree.path, "diff", "--name-status", "--no-renames", base_commit, *spec)
    for line in listed.split("\n"):
        if line:
            status, path = line.split("\t", 1)
            result[path] = status[0]
    untracked = git.out(tree.path, "ls-files", "--others", "--exclude-standard", *spec)
    for path in untracked.split("\n"):
        if path:
            result[path] = "A"
    return dict(sorted(result.items()))


def _authored(tree: Worktree, base_commit: str, path: str, status: str, schema: Schema) -> bool:
    """False for a file the tool writes whole (index.md) and for a Markdown file
    whose change lies only in generated sections or provenance fields."""
    if Path(path).name == "index.md" and path.startswith(BUNDLE_DIR + "/"):
        return False
    if status != "M" or not path.endswith(".md"):
        return True
    before = git.show(tree.path, base_commit, path) or ""
    after = (tree.path / path).read_text(encoding="utf-8", errors="replace")
    return stamps.authored_view(before, schema) != stamps.authored_view(after, schema)


def content_hash(tree: Worktree) -> str:
    """A hash of every file of the worktree that git would see."""
    digest = hashlib.sha256()
    listed = git.out(tree.path, "ls-files", "--cached", "--others", "--exclude-standard")
    for path in sorted(set(listed.split("\n")) - {""}):
        file = tree.path / path
        digest.update(path.encode() + b"\0")
        digest.update(file.read_bytes() if file.is_file() else b"\0deleted\0")
    return digest.hexdigest()


# --- finish ----------------------------------------------------------------------


def _check_actor(actor: str, option: str, human_only: bool = False) -> None:
    if not ACTOR_RE.match(actor) or (human_only and not actor.startswith("human:")):
        kind = "a human:<id> actor" if human_only else "an actor: human:<id>, process:<id> or <producer>/<version>"
        raise ToolError(f"{option} must be {kind}, got {actor}")


def _log_folders(bundle: Bundle) -> dict[Path, Path]:
    """{concept folder: its log.md} for every folder concept that keeps a log."""
    return {
        concept.folder: concept.folder / "log.md"
        for concept in bundle.concepts
        if concept.folder is not None and bundle.schema.types[concept.type].get("log", True) and concept.type != "Application"
    }


def _git_human(cwd: Path, option: str) -> str:
    """`human:<id>` from git config user.email, for an option given without a value."""
    email = git.run(cwd, "config", "user.email", check=False).stdout.strip()
    if not email:
        raise ToolError(f"git config user.email is not set: pass {option} human:<id>")
    return stamps.human(email)


def _unverified(cwd: Path, paths: tuple[str, ...], files: list[Path]) -> set[Path]:
    """The files to stamp that `paths` name: a file, or every one under a folder."""
    chosen: set[Path] = set()
    for given in paths:
        target = (cwd / given).resolve()
        found = [file for file in files if target == file.resolve() or target in file.resolve().parents]
        if not found:
            raise ToolError(f"--unverified {given}: not a concept file this draft changed, and none is under it")
        chosen.update(found)
    return chosen


def finish(
    cwd: Path, actor: str, verified_by: str | None = None, schema: Schema | None = None, unverified: tuple[str, ...] = ()
) -> dict:
    """verified_by "" means the person in git config user.email. `unverified`
    names changed files, or folders of them, that the person did not check:
    they are stamped `generated` and left without `verified`."""
    _check_actor(actor, "--by")
    if unverified and verified_by is None:
        raise ToolError("--unverified needs --verified-by: without it no changed file is confirmed")
    if verified_by == "":
        verified_by = _git_human(cwd, "--verified-by")
    if verified_by is not None:
        _check_actor(verified_by, "--verified-by", human_only=True)
    schema = schema or Schema.load()
    tree = Worktree.here(cwd)
    locate.check_version(tree.bundle, schema)
    base = git.default_branch(tree.repo)
    base_commit = tree.merge_base(base)
    changed = changes(tree, base_commit, (BUNDLE_DIR,))
    at = stamps.now()

    # 1. provenance
    bundle = Bundle.load(tree.bundle, schema)
    authored: set[Path] = set()
    stamping: dict[Path, str] = {}
    for path, status in changed.items():
        file = tree.path / path
        holder = bundle.content_holder(file)
        if holder is not None:
            authored.add(file)  # a content file: its Reference is approved as a whole
            if holder.path not in bundle.unreadable and not holder.fm_errors:
                stamping[holder.path] = holder.path.relative_to(tree.path).as_posix()
            continue
        if status == "D" or not _authored(tree, base_commit, path, status, schema):
            continue
        authored.add(file)
        concept = bundle.by_path.get(file)
        if concept is None or file in bundle.unreadable or concept.fm_errors:
            continue
        stamping[file] = path
    unchecked = _unverified(cwd, unverified, list(stamping))
    for file, path in stamping.items():
        text = bundle.text(file)
        text = frontmatter.set_field(text, "generated", stamps.render({"by": actor, "at": at}))
        if file in unchecked:
            text = stamps.set_verified(text, [])
        elif verified_by is not None:
            text = stamps.set_verified(text, [{"by": verified_by, "at": at}])
        elif bundle.by_path[file].meta.get("verified") == _base_meta(tree, base_commit, path).get("verified"):
            text = stamps.set_verified(text, [])
        file.write_text(text, encoding="utf-8")
    stamped = [bundle.rel(file) for file in stamping]

    # 2. log entries
    logs = _log_folders(bundle)
    missing: list[str] = []
    needing = set()
    for path, status in changed.items():
        file = tree.path / path
        if file.name in ("log.md", "index.md") or (status != "D" and file not in authored):
            continue
        holder = bundle.content_holder(file)
        if holder is not None:
            needing.add(holder.folder)
        elif file.parent in logs:
            needing.add(file.parent)
    for folder in sorted(needing):
        log = logs[folder]
        rel = log.relative_to(tree.path).as_posix()
        before = stamps.log_entries(git.show(tree.path, base_commit, rel) or "")
        after = stamps.log_entries(log.read_text(encoding="utf-8", errors="replace")) if log.is_file() else set()
        if not after - before:
            missing.append(bundle.rel(log))

    # 3. sync, then validate
    synced = [Bundle.load(tree.bundle, schema).rel(path) for path in sync.write(tree.bundle, schema)]
    report = validate.report(validate.run(tree.bundle, schema))
    ok = not missing and report["ok"]
    (tree.git_dir() / RECORD).write_text(json.dumps({"ok": ok, "hash": content_hash(tree)}), encoding="utf-8")
    return {
        "ok": ok,
        "stamped": sorted(stamped),
        "unverified": sorted(bundle.rel(file) for file in unchecked),
        "missing_logs": missing,
        "synced": synced,
        "validate": report,
    }


def _base_meta(tree: Worktree, base_commit: str, path: str) -> dict:
    text = git.show(tree.path, base_commit, path)
    return frontmatter.parse(text)[0] if text is not None else {}


# --- diff, commit ----------------------------------------------------------------


def diff(cwd: Path, schema: Schema | None = None) -> dict:
    schema = schema or Schema.load()
    tree = Worktree.here(cwd)
    locate.check_version(tree.bundle, schema)
    base = git.default_branch(tree.repo)
    base_commit = tree.merge_base(base)
    changed = changes(tree, base_commit)
    files = [
        {"path": path, "status": status, "authored": _authored(tree, base_commit, path, status, schema)}
        for path, status in changed.items()
    ]
    text = git.run(tree.path, "diff", base_commit).stdout
    tracked = set(git.out(tree.path, "ls-files").split("\n"))
    for path, status in changed.items():
        if status == "A" and path not in tracked:
            text += git.run(tree.path, "diff", "--no-index", "--", "/dev/null", path, check=False).stdout
    return {"ok": True, "base": base, "files": files, "diff": text}


def commit(cwd: Path, message: str) -> dict:
    tree = Worktree.here(cwd)
    record = tree.git_dir() / RECORD
    if not record.is_file():
        raise Refused("run draft finish before draft commit")
    finished = json.loads(record.read_text(encoding="utf-8"))
    if not finished["ok"]:
        raise Refused("the last draft finish was not ok: fix what it reported and run draft finish again")
    if finished["hash"] != content_hash(tree):
        raise Refused("the draft changed after draft finish: run draft finish again")
    pending = changes(tree, "HEAD")
    outside = [path for path in pending if path.split("/")[0] not in COMMITTED]
    if outside:
        raise Refused(f"the draft has changes outside the wiki: {', '.join(outside)}; remove them first")
    if not pending:
        raise Refused("nothing to commit")
    git.run(tree.path, "add", "--all", "--", *pending)
    git.run(tree.path, "commit", "--quiet", "-m", message)
    sha = git.out(tree.path, "rev-parse", "HEAD")
    pushed = False
    if git.has_remote(tree.repo):
        push = git.run(tree.path, "push", "--quiet", "-u", "origin", tree.branch, check=False)
        if push.returncode != 0:
            raise ToolError(
                f"committed {sha[:12]} on {tree.branch}, but the push failed: {push.stderr.strip()}; "
                f"push it with: git push -u origin {tree.branch}"
            )
        pushed = True
    git.run(tree.repo, "worktree", "remove", str(tree.path))
    note = (
        f"pushed {tree.branch}: open a pull request from it"
        if pushed
        else f"no remote: push {tree.branch} when one exists, then open a pull request"
    )
    return {"ok": True, "commit": sha, "branch": tree.branch, "pushed": pushed, "repository": str(tree.repo), "message": note}


# --- refresh ---------------------------------------------------------------------

CONFLICT_RE = re.compile(r"^<<<<<<< .*?\n(.*?)^=======\n(.*?)^>>>>>>> .*?\n", re.MULTILINE | re.DOTALL)


def _generated_names(text: str, schema: Schema) -> set[str]:
    meta, _, _ = frontmatter.parse(text)
    type_name = meta.get("type")
    names = [type_name] if isinstance(type_name, str) and type_name in schema.types else list(schema.types)
    return {spec["name"] for name in names for spec in schema.headings(name) if "generated" in spec}


def resolve_generated(text: str, schema: Schema) -> str | None:
    """Take our side of every conflict that lies inside a generated section;
    None when any conflict lies elsewhere."""
    names = _generated_names(text, schema)
    resolved: list[str] = []
    position = 0
    for match in CONFLICT_RE.finditer(text):
        before = text[:match.start()]
        headings = [line[2:].strip() for line in before.split("\n") if line.startswith("# ")]
        hunk = match.group(1) + match.group(2)
        if not headings or headings[-1] not in names or any(line.startswith("# ") for line in hunk.split("\n")):
            return None
        resolved += [text[position:match.start()], match.group(1)]
        position = match.end()
    return "".join(resolved) + text[position:]


def refresh(cwd: Path, schema: Schema | None = None) -> dict:
    schema = schema or Schema.load()
    tree = Worktree.here(cwd)
    merging = (tree.git_dir() / "MERGE_HEAD").exists()
    _fetch(tree.repo)
    base = git.default_branch(tree.repo)
    resolved: list[str] = []
    if not merging:
        if git.out(tree.path, "status", "--porcelain"):
            raise Refused("the draft has uncommitted changes: finish and commit them, or discard them, first")
        if git.ok(tree.path, "merge-base", "--is-ancestor", base, "HEAD"):
            return {"ok": True, "base": base, "merged": None, "resolved": [], "synced": [], "validate": None, "pushed": False}
        attempt = git.run(
            tree.path, "-c", "merge.conflictStyle=merge", "merge", "--no-ff", "--no-commit", "--quiet", base, check=False
        )
        conflicted = [path for path in git.out(tree.path, "diff", "--name-only", "--diff-filter=U").split("\n") if path]
        if attempt.returncode != 0 and not conflicted:
            raise ToolError(f"git merge {base} failed: {(attempt.stderr or attempt.stdout).strip()}")
        manual: list[str] = []
        for path in conflicted:
            file = tree.path / path
            if file.name == "index.md":
                git.run(tree.path, "checkout", "--ours", "--", path)
            else:
                text = resolve_generated(file.read_text(encoding="utf-8", errors="replace"), schema) if file.is_file() else None
                if text is None:
                    manual.append(path)
                    continue
                file.write_text(text, encoding="utf-8")
            resolved.append(path)
        if manual:
            git.run(tree.path, "merge", "--abort")
            raise Refused(f"a person has to resolve these: {', '.join(manual)}")
    elif [path for path in git.out(tree.path, "diff", "--name-only", "--diff-filter=U").split("\n") if path]:
        raise Refused("the merge still has unresolved files: resolve them, then run refresh again")
    locate.check_version(tree.bundle, schema)
    synced = [Bundle.load(tree.bundle, schema).rel(path) for path in sync.write(tree.bundle, schema)]
    report = validate.report(validate.run(tree.bundle, schema))
    if not report["ok"]:
        return {"ok": False, "base": base, "merged": None, "resolved": resolved, "synced": synced, "validate": report,
                "pushed": False, "message": "the merge is not committed: fix the errors in the draft, then run refresh again"}
    git.run(tree.path, "add", "--all", "--", *[p for p in COMMITTED if (tree.path / p).exists()])
    git.run(tree.path, "commit", "--quiet", "--no-edit")
    pushed = False
    if git.has_remote(tree.repo):
        git.run(tree.path, "push", "--quiet", "-u", "origin", tree.branch)
        pushed = True
    sha = git.out(tree.path, "rev-parse", "HEAD")
    return {"ok": True, "base": base, "merged": sha, "resolved": resolved, "synced": synced, "validate": report, "pushed": pushed}


# --- verify ----------------------------------------------------------------------


def verify(cwd: Path, target: str, by: str | None = None, schema: Schema | None = None) -> dict:
    schema = schema or Schema.load()
    tree = Worktree.here(cwd)
    locate.check_version(tree.bundle, schema)
    if by is None:
        by = _git_human(tree.path, "--by")
    _check_actor(by, "--by", human_only=True)
    bundle = Bundle.load(tree.bundle, schema)
    file = (cwd / target).resolve()
    concept = next((c for c in bundle.concepts if c.path.resolve() == file), None)
    if concept is None:
        raise ToolError(f"not a concept file of the draft's bundle: {target}")
    at = stamps.now()
    stamp = {"by": by, "at": at}
    file.write_text(stamps.add_verified(bundle.text(file), stamp), encoding="utf-8")
    folder = concept.folder or (concept.owner.folder if concept.owner is not None else None)
    log_rel = None
    if folder is not None and (folder / "log.md").is_file():
        log = folder / "log.md"
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log.write_text(stamps.add_log_entry(bundle.text(log), day, f"**Verification**: Confirmed by {by}."), encoding="utf-8")
        log_rel = bundle.rel(log)
    return {"ok": True, "path": concept.rel, "verified": stamp, "log": log_rel}
