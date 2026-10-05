"""The Tool copy: the schema and the tool kept in a Wiki repository's `.wiki-llm/`.

`install` replaces a copy with this tool's own files and writes a manifest of
their checksums. `check` compares a copy with its manifest, then its versions
with those of a source: by default this tool, else another tool folder or a
Release version given by a skill. Only the major and minor parts of a Release
version are compared: a patch release changes skills only, never the tool.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

from .errors import ToolError
from .schema import SCHEMA_DIR, Schema

TOOL_HOME = SCHEMA_DIR.parent  # wiki-llm/ in this repository or a skill, .wiki-llm/ in a Wiki repository
COPY_DIR = ".wiki-llm"
MANIFEST = "manifest.json"
RELEASE = "RELEASE"
SKIPPED_PARTS = {"__pycache__", "tests"}
VERSION_RE = re.compile(r"^\d+(\.\d+)*$")


def _release_of(home: Path) -> str | None:
    """The Release version of a tool folder: its RELEASE file, else its manifest; None when neither."""
    release = home / RELEASE
    if release.is_file():
        return _checked(release.read_text(encoding="utf-8").strip())
    manifest = home / MANIFEST
    if manifest.is_file():
        try:
            return _checked(json.loads(manifest.read_text(encoding="utf-8"))["release_version"])
        except (ValueError, KeyError, TypeError) as error:
            raise ToolError(f"{manifest} is damaged ({error})")
    return None


def release_version() -> str:
    """The Release version of this tool."""
    found = _release_of(TOOL_HOME)
    if found is None:
        raise ToolError(f"cannot tell this tool's release version: no {RELEASE} or {MANIFEST} in {TOOL_HOME}")
    return found


def _checked(text: str) -> str:
    _version(text)
    return text


def _version(text: str) -> tuple[int, ...]:
    if not VERSION_RE.fullmatch(text):
        raise ToolError(f"not a version: {text}")
    return tuple(int(part) for part in text.split("."))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _skipped(rel: Path) -> bool:
    return any(part in SKIPPED_PARTS for part in rel.parts) or rel.suffix == ".pyc"


def _files(home: Path) -> dict[str, Path]:
    """Every file of schema/ and tools/ under `home`, without tests and caches."""
    found: dict[str, Path] = {}
    for folder in ("schema", "tools"):
        for path in sorted((home / folder).rglob("*")):
            rel = path.relative_to(home)
            if path.is_file() and not _skipped(rel):
                found[rel.as_posix()] = path
    return found


def _copy_files(copy: Path) -> dict[str, Path]:
    """Every file of an installed copy except its manifest and Python caches."""
    return {
        path.relative_to(copy).as_posix(): path
        for path in sorted(copy.rglob("*"))
        if path.is_file()
        and path.relative_to(copy).as_posix() != MANIFEST
        and "__pycache__" not in path.relative_to(copy).parts
        and path.suffix != ".pyc"
    }


def install(repo: Path) -> dict:
    return install_into(repo / COPY_DIR)


def install_into(target: Path) -> dict:
    """Replace the folder `target` with this tool's schema/ and tools/ and a manifest."""
    if target.resolve() == TOOL_HOME.resolve():
        raise ToolError("copy install would replace the tool that is running: run it from another copy")
    if target.exists():
        shutil.rmtree(target)
    files = _files(TOOL_HOME)
    for rel, source in files.items():
        destination = target / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    manifest = {
        "release_version": release_version(),
        "schema_version": Schema.load().version,
        "files": {rel: _sha256(target / rel) for rel in files},
    }
    (target / MANIFEST).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "path": target.name, "release_version": manifest["release_version"],
            "schema_version": manifest["schema_version"], "files": len(files)}


def find(start: Path) -> Path:
    """The Wiki repository folder above `start` that holds a Tool copy."""
    for directory in [start, *start.parents]:
        if (directory / COPY_DIR / MANIFEST).is_file():
            return directory
    raise ToolError("no tool copy found: run sdlc-setup-wiki to create the wiki repository")


MESSAGES = {
    "edited": "the tool copy was edited by hand: run sdlc-setup-wiki to restore it",
    "older": "the wiki is older than these skills: run sdlc-setup-wiki to upgrade it",
    "newer": "the wiki was set up by a newer release: update your installed sdlc-skills",
    "current": "the tool copy matches these skills",
}


def _source(source: Path | None, release: str | None) -> dict:
    """The versions a copy is compared with."""
    if release is not None:
        return {"release_version": _checked(release), "schema_version": None}
    home = TOOL_HOME if source is None else source
    schema_file = home / "schema" / "schema.json"
    found = _release_of(home)
    if found is None or not schema_file.is_file():
        raise ToolError(f"not a tool folder (needs schema/schema.json and {RELEASE} or {MANIFEST}): {home}")
    return {"release_version": found, "schema_version": Schema.load(schema_file).version}


def check(repo: Path, source: Path | None = None, release: str | None = None) -> dict:
    copy = repo / COPY_DIR
    try:
        manifest = json.loads((copy / MANIFEST).read_text(encoding="utf-8"))
        recorded: dict[str, str] = dict(manifest["files"])
        mine = _version(manifest["release_version"])
        manifest["schema_version"]
    except (ValueError, KeyError, TypeError) as error:
        raise ToolError(f"{COPY_DIR}/{MANIFEST} is damaged ({error}): run sdlc-setup-wiki to restore the tool copy")
    present = _copy_files(copy)
    added = sorted(set(present) - set(recorded))
    missing = sorted(set(recorded) - set(present))
    changed = sorted(rel for rel in set(present) & set(recorded) if _sha256(present[rel]) != recorded[rel])
    running = _source(source, release)
    theirs = _version(running["release_version"])
    schema_differs = running["schema_version"] is not None and manifest["schema_version"] != running["schema_version"]
    if added or missing or changed:
        status = "edited"
    elif mine[:2] > theirs[:2]:
        status = "newer"
    elif mine[:2] < theirs[:2] or schema_differs:
        status = "older"
    else:
        status = "current"
    return {
        "ok": status == "current",
        "status": status,
        "message": MESSAGES[status],
        "copy": {"release_version": manifest["release_version"], "schema_version": manifest["schema_version"]},
        "source": running,
        "added": added,
        "missing": missing,
        "changed": changed,
    }
