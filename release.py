#!/usr/bin/env python3
"""Set the Release version and refresh everything that carries it.

    python3 release.py            write every RELEASE file from wiki-llm/RELEASE, rebuild the release copy
    python3 release.py 1.1.0      set wiki-llm/RELEASE to 1.1.0 first

The release copy is skills/sdlc-setup-wiki/wiki-llm/: the tool and schema the
setup skill installs into a Wiki repository.

A patch release changes skills only. Once a release of a major.minor is
tagged (v<version>), a change to the tool or schema needs a new minor version.

Prints JSON; exits 0, or 2 on a bad version or a refused release.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "wiki-llm" / "tools"))

from wikilib import toolcopy  # noqa: E402
from wikilib.errors import ToolError  # noqa: E402

SETUP = HERE / "skills" / "sdlc-setup-wiki"


def _write(path: Path, text: str, written: list[str]) -> None:
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    written.append(path.relative_to(HERE).as_posix())


def _parts(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def _tool_changed(copy: Path) -> bool:
    """True when schema/ or tools/ differ from the files recorded in the release copy."""
    recorded = json.loads((copy / toolcopy.MANIFEST).read_text(encoding="utf-8"))["files"]
    current = {rel: hashlib.sha256(path.read_bytes()).hexdigest() for rel, path in toolcopy._files(toolcopy.TOOL_HOME).items()}
    return recorded != current


def _tagged(major: int, minor: int) -> bool:
    """True when this repository has a tag v<major>.<minor>.*."""
    out = subprocess.run(["git", "-C", str(HERE), "tag", "--list", f"v{major}.{minor}.*"], capture_output=True, text=True)
    return out.returncode == 0 and bool(out.stdout.strip())


def _check_tool_change(version: str, copy: Path) -> None:
    if not (copy / toolcopy.MANIFEST).is_file() or not _tool_changed(copy):
        return
    major, minor = _parts(version)[:2]
    if _tagged(major, minor):
        raise ToolError(
            f"the tool or schema changed and release {major}.{minor} is tagged: "
            f"a tool change needs a new minor version: python3 release.py {major}.{minor + 1}.0"
        )


def release(version: str | None) -> dict:
    if version is not None and not toolcopy.VERSION_RE.fullmatch(version):
        raise ToolError(f"not a version: {version}")
    copy = SETUP / "wiki-llm"
    _check_tool_change(version or toolcopy.release_version(), copy)

    written: list[str] = []
    if version is not None:
        _write(HERE / "wiki-llm" / toolcopy.RELEASE, version + "\n", written)
    version = toolcopy.release_version()
    for path in sorted({*HERE.glob(f"skills/*/{toolcopy.RELEASE}"), SETUP / toolcopy.RELEASE}):
        _write(path, version + "\n", written)
    toolcopy.install_into(copy)
    written.append(copy.relative_to(HERE).as_posix() + "/")
    return {"ok": True, "release_version": version, "written": written}


def main(argv: list[str]) -> int:
    try:
        result = release(argv[0] if argv else None)
    except ToolError as error:
        print(json.dumps({"ok": False, "error": str(error)}, indent=2))
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
