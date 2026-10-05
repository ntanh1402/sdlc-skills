#!/usr/bin/env python3
"""Set the Release version and refresh everything that carries it.

    python3 release.py            write every RELEASE file from wiki-llm/RELEASE, rebuild the release copy
    python3 release.py 1.1.0      set wiki-llm/RELEASE to 1.1.0 first

The release copy is skills/sdlc-setup-wiki/wiki-llm/: the tool and schema the
setup skill installs into a Wiki repository. The shared references in
skill-shared/ are copied into each skill that uses them, and each skill's
agents/openai.yaml is written from skill-shared/openai.json.

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
SHARED = HERE / "skill-shared"
LIFECYCLE = ("sdlc-write-spec", "sdlc-write-stories", "sdlc-design-arch", "sdlc-plan-tasks", "sdlc-design-tests", "sdlc-import")
WRITERS = (*LIFECYCLE, "sdlc-close-task", "sdlc-edit-wiki")  # every skill that writes a Draft
REFERENCES = {
    "read-protocol.md": (*WRITERS, "sdlc-build-task", "sdlc-ask-wiki", "sdlc-review-code"),
    "flow.md": (*WRITERS, "sdlc-build-task"),
    "write-protocol.md": WRITERS,
    "code-checks.md": ("sdlc-build-task", "sdlc-review-code"),
    "paste-format.md": ("sdlc-write-stories", "sdlc-ask-wiki"),
}
OPENAI_KEYS = ("display_name", "short_description", "default_prompt")


def _write(path: Path, text: str, written: list[str]) -> None:
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    written.append(path.relative_to(HERE).as_posix())


def openai_yaml(entry: dict) -> str:
    """A skill's agents/openai.yaml: the interface metadata some agents show."""
    return "interface:\n" + "".join(f"  {key}: {json.dumps(entry[key])}\n" for key in OPENAI_KEYS)


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
    skills = sorted(path.parent for path in HERE.glob("skills/*/SKILL.md"))
    entries = json.loads((SHARED / "openai.json").read_text(encoding="utf-8"))
    missing = [skill.name for skill in skills if skill.name not in entries]
    if missing:
        raise ToolError(f"skill-shared/openai.json has no entry for {', '.join(missing)}")

    written: list[str] = []
    if version is not None:
        _write(HERE / "wiki-llm" / toolcopy.RELEASE, version + "\n", written)
    version = toolcopy.release_version()
    for path in sorted({*HERE.glob(f"skills/*/{toolcopy.RELEASE}"), SETUP / toolcopy.RELEASE}):
        _write(path, version + "\n", written)
    toolcopy.install_into(copy)
    written.append(copy.relative_to(HERE).as_posix() + "/")
    for skill in skills:
        _write(skill / "agents" / "openai.yaml", openai_yaml(entries[skill.name]), written)
    for name, owners in REFERENCES.items():
        text = (SHARED / name).read_text(encoding="utf-8")
        for skill in skills:
            if skill.name in owners:
                _write(skill / "references" / name, text, written)
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
