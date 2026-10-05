"""link: write the Workspace note that tells skills where the Wiki repository is.

The note goes between two markers in each AGENTS.md and CLAUDE.md of the
Workspace, or into a new AGENTS.md when neither exists. A second run replaces
the note instead of adding another.
"""

from __future__ import annotations

import os
import shlex
from pathlib import Path

from . import toolcopy
from .errors import Refused, ToolError

START, END = "<!-- sdlc-skills:start -->", "<!-- sdlc-skills:end -->"
FILES = ("AGENTS.md", "CLAUDE.md")


def note(path: str) -> str:
    return "\n".join([
        START,
        "## Project wiki",
        "",
        f"The wiki repository of this workspace is `{path}` (relative to this file)."
        if not os.path.isabs(path) else f"The wiki repository of this workspace is `{path}`.",
        "sdlc-skills run its tool from inside that folder:",
        f"`cd {shlex.quote(path)} && python3 .wiki-llm/tools/wiki_llm.py <command>`",
        END,
    ]) + "\n"


def path_for(workspace: Path, wiki: Path) -> tuple[str, bool]:
    """The wiki path as the note writes it, and whether it is absolute."""
    if Path(os.path.commonpath([workspace, wiki])) == Path(workspace.anchor):
        return str(wiki), True
    return Path(os.path.relpath(wiki, workspace)).as_posix(), False


def warnings_for(path: str, absolute: bool) -> list[str]:
    if not absolute:
        return []
    return [f"the note holds an absolute path ({path}); people whose checkout is elsewhere "
            "must run sdlc-setup-wiki again"]


def _with_note(name: str, text: str, block: str) -> str:
    starts, ends = text.count(START), text.count(END)
    if starts == 0 and ends == 0:
        if not text.strip():
            return block
        return text.rstrip("\n") + "\n\n" + block
    if starts != 1 or ends != 1 or text.index(START) > text.index(END):
        raise Refused(f"{name} has a broken sdlc-skills note: keep one {START} … {END} pair, then run link again")
    before, rest = text.split(START, 1)
    after = rest.split(END, 1)[1]
    return before + block + after.removeprefix("\n")


def link(workspace: Path, wiki: Path) -> dict:
    if not workspace.is_dir():
        raise ToolError(f"the workspace is not a folder: {workspace}")
    ready = (wiki / toolcopy.COPY_DIR / toolcopy.MANIFEST).is_file() and (wiki / "wiki" / "index.md").is_file()
    if not ready and not (wiki / ".git").exists():
        raise ToolError(f"not a wiki repository (no .wiki-llm/ or wiki/, and not a git repository): {wiki}")
    workspace, wiki = workspace.resolve(), wiki.resolve()
    path, absolute = path_for(workspace, wiki)
    warnings = warnings_for(path, absolute)
    if not ready:
        warnings.append(f"{path} has no wiki on its checked-out branch yet: skills find it once the setup "
                        "pull request is merged")
    block = note(path)
    present = [name for name in FILES if (workspace / name).is_file()] or [FILES[0]]
    planned: dict[str, tuple[str, str]] = {}
    for name in present:
        file = workspace / name
        before = file.read_text(encoding="utf-8") if file.is_file() else ""
        planned[name] = (before, _with_note(name, before, block))
    written, unchanged = [], []
    for name, (before, after) in planned.items():
        if before == after:
            unchanged.append(name)
            continue
        (workspace / name).write_text(after, encoding="utf-8")
        written.append(name)
    return {"ok": True, "workspace": str(workspace), "wiki": path, "written": written,
            "unchanged": unchanged, "warnings": warnings}
