"""init: write the skeleton of a new Wiki repository; add_app: add an Application.

The skeleton is a README that lists the checks, a .gitignore for draft
worktrees, the Tool copy, and a Bundle in wiki/ with one Application. Files a repository already has are kept,
and git is not touched. add_app writes one more Application into an existing Bundle, usually inside a Draft.
"""

from __future__ import annotations

import re
from pathlib import Path

from . import frontmatter, stamps, sync, toolcopy, validate
from .errors import Refused, ToolError
from .schema import Schema

IGNORED = [".worktrees/", "__pycache__/"]

README = """# {title} wiki

This repository holds the knowledge of {title} as a wiki of Markdown files in
`wiki/`. sdlc-skills read and write it; people may too.
`.wiki-llm/` is the tool that checks it. Do not edit `.wiki-llm/` by hand: the
`sdlc-setup-wiki` skill installs and upgrades it.

## Checks

Run these before merging a pull request, by hand or in CI. Each prints JSON and
exits 0 when the check passes.

```bash
python3 .wiki-llm/tools/wiki_llm.py copy check       # the tool copy is unedited
python3 .wiki-llm/tools/wiki_llm.py validate         # the wiki follows its schema
python3 .wiki-llm/tools/wiki_llm.py sync --check     # tool-written files are up to date
```

## Changing the wiki

Every change is made on a draft branch and merged by a pull request:

```bash
python3 .wiki-llm/tools/wiki_llm.py draft start <key>     # branch wiki/<key> in .worktrees/<key>/
cd .worktrees/<key>                                       # edit files under wiki/, add log entries
python3 .wiki-llm/tools/wiki_llm.py draft finish --by human:<you>
python3 .wiki-llm/tools/wiki_llm.py draft diff
python3 .wiki-llm/tools/wiki_llm.py draft commit -m "<message>"
```

Then open a pull request from `wiki/<key>`.
"""


def _scalar(value: str, option: str) -> str:
    """A frontmatter value, quoted when the plain form would not parse."""
    if not value.strip() or '"' in value or "\n" in value:
        raise ToolError(f"{option} must be one line of text without double quotes")
    _, _, errors = frontmatter.parse(f"---\nk: {value}\n---\n")
    return f'"{value}"' if errors else value


def _gitignore(path: Path) -> bool:
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    lines = text.split("\n")
    missing = [line for line in IGNORED if line not in lines]
    if not missing:
        return False
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + "\n".join(missing) + "\n", encoding="utf-8")
    return True


def _check_key(schema: Schema, app: str, option: str) -> None:
    if not re.match(schema.key_pattern("Application"), app):
        raise ToolError(f"{option} must be lower-case words joined by -, got {app}")


def _application(app: str, title: str, title_value: str, team_value: str) -> str:
    """The overview.md of a new Application, written by this tool."""
    actor = f"wiki-llm/{toolcopy.release_version()}"
    return (
        f"---\ntype: Application\ntitle: {title_value}\ndescription: The {app} application.\nstatus: Active\n"
        f"ownerTeam: {team_value}\ngenerated: {stamps.render({'by': actor, 'at': stamps.now()})}\n---\n\n"
        f"# {title}\n\nWhat {title} is and who uses it.\n\n# Architecture\n\nNone\n"
    )


def init(repo: Path, app: str, title: str, owner_team: str, schema: Schema | None = None) -> dict:
    schema = schema or Schema.load()
    _check_key(schema, app, "--app")
    for name in ("wiki", toolcopy.COPY_DIR):
        if (repo / name).exists():
            raise Refused(f"{repo / name} exists: this is already a wiki repository; sdlc-setup-wiki upgrades it")
    title_value, team_value = _scalar(title, "--title"), _scalar(owner_team, "--owner-team")
    repo.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    kept: list[str] = []

    readme = repo / "README.md"
    if readme.exists():
        kept.append("README.md")
    else:
        readme.write_text(README.format(title=title), encoding="utf-8")
        written.append("README.md")
    (written if _gitignore(repo / ".gitignore") else kept).append(".gitignore")
    toolcopy.install(repo)
    written.append(toolcopy.COPY_DIR + "/")

    root = repo / "wiki"
    (root / app).mkdir(parents=True)
    (root / "index.md").write_text(
        f'---\nokf_version: "{schema.okf_version}"\nschema_version: "{schema.version}"\n---\n\n# Applications\n',
        encoding="utf-8",
    )
    (root / app / "overview.md").write_text(_application(app, title, title_value, team_value), encoding="utf-8")
    synced = sync.write(root, schema)
    written += sorted({"wiki/index.md", f"wiki/{app}/overview.md"} | {path.relative_to(repo).as_posix() for path in synced})
    report = validate.report(validate.run(root, schema))
    return {"ok": report["ok"], "written": written, "kept": kept, "validate": report}


def add_app(root: Path, app: str, title: str, owner_team: str, schema: Schema | None = None) -> dict:
    """Write <root>/<app>/overview.md as init writes the first Application, then sync."""
    schema = schema or Schema.load()
    _check_key(schema, app, "--key")
    title_value, team_value = _scalar(title, "--title"), _scalar(owner_team, "--owner-team")
    folder = root / app
    if folder.exists():
        raise Refused(f"{app} exists: the wiki already has this application")
    folder.mkdir()
    (folder / "overview.md").write_text(_application(app, title, title_value, team_value), encoding="utf-8")
    repo = root.parent
    synced = sync.write(root, schema)
    written = sorted({f"{root.name}/{app}/overview.md"} | {path.relative_to(repo).as_posix() for path in synced})
    report = validate.report(validate.run(root, schema))
    return {"ok": report["ok"], "written": written, "validate": report}
