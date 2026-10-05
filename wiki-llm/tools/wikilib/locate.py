"""Find the bundle a command acts on, and refuse a bundle of another schema version."""

from __future__ import annotations

from pathlib import Path

from . import frontmatter
from .errors import ToolError
from .schema import Schema

NOT_FOUND = "no bundle found: run from inside a wiki repository or pass --root"


def schema_version(root: Path) -> str | None:
    """The `schema_version` of a bundle root's index.md, or None."""
    index = root / "index.md"
    if not index.is_file():
        return None
    meta, _, _ = frontmatter.parse(index.read_text(encoding="utf-8", errors="replace"))
    value = meta.get("schema_version")
    return value if isinstance(value, str) and value else None


def discover(start: Path) -> Path:
    """Walk up from `start`: a directory whose index.md has schema_version is
    the bundle; else its `wiki/` folder when that one has it."""
    for directory in [start, *start.parents]:
        for candidate in (directory, directory / "wiki"):
            if schema_version(candidate) is not None:
                return candidate
    raise ToolError(NOT_FOUND)


def bundle_root(explicit: str | None, start: Path) -> Path:
    """An explicit root (--root or WIKI_LLM_ROOT), else discovery from `start`."""
    if not explicit:
        return discover(start)
    root = Path(explicit)
    if not (root / "index.md").is_file():
        raise ToolError(f"not a bundle (no index.md): {root}")
    if schema_version(root) is None:
        raise ToolError(f"not a bundle (index.md has no schema_version): {root}")
    return root


def check_version(root: Path, schema: Schema) -> None:
    found = schema_version(root)
    if found != schema.version:
        raise ToolError(
            f"bundle is schema {found}, this tool is schema {schema.version}: "
            "run `wiki_llm.py migrate` (sdlc-setup-wiki does this)"
        )
