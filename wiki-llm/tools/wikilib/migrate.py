"""Bring a bundle to this tool's schema version.

1 → 2: TestSuites changed shape (one per Feature or ChangeRequest, cases in
STORY-* and GENERAL folders), so every schema-1 suite is removed and reported
with the targets it verified; the test design skills write them again. Git history
keeps the removed files.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from . import frontmatter, markdown, sync
from .errors import Refused
from .schema import Schema

TARGET_RE = re.compile(r"\b(?:FEAT|CR)-[a-z0-9]+(?:-[a-z0-9]+)*")


def _one_to_two(root: Path) -> dict:
    removed: list[str] = []
    retest: set[str] = set()
    for suite in sorted(root.glob("*/tests/TS-*")):
        if not suite.is_dir():
            continue
        overview = suite / "overview.md"
        if overview.is_file():
            _, body, _ = frontmatter.parse(overview.read_text(encoding="utf-8"))
            section = markdown.section(body, "Verifies", level=1)
            retest.update(TARGET_RE.findall(section.text if section else ""))
        shutil.rmtree(suite)
        removed.append(suite.relative_to(root).as_posix())
    return {"removed": removed, "retest": sorted(retest)}


STEPS = {("1", "2"): _one_to_two}


def run(root: Path, found: str | None, schema: Schema) -> dict:
    if found == schema.version:
        return {"ok": True, "from": found, "to": schema.version, "written": []}
    step = STEPS.get((found, schema.version))
    if step is None:
        raise Refused(f"no migration from schema {found} to {schema.version} is available in this version")
    result = step(root)
    index = root / "index.md"
    index.write_text(re.sub(r'^schema_version: "?[^"\n]*"?$', f'schema_version: "{schema.version}"', index.read_text(encoding="utf-8"), count=1, flags=re.M), encoding="utf-8")
    written = sync.write(root, schema)
    return {"ok": True, "from": found, "to": schema.version, "written": sorted({"index.md"} | {p.relative_to(root).as_posix() for p in written}), **result}
