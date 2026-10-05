"""Layout: files are where the schema says, with the type and key it expects."""

from __future__ import annotations

import re

from ..bundle import Bundle, Finding

ORDER = 10


def check(bundle: Bundle) -> list[Finding]:
    schema = bundle.schema
    for path in bundle.markdown_files():
        bundle.text(path)  # a file that is not UTF-8 becomes a layout.encoding problem
    findings = list(bundle.problems)

    index = bundle.root / "index.md"
    if not index.is_file() or "okf_version" not in bundle.index_meta:
        findings.append(Finding("layout.root-index", "index.md", "bundle root needs index.md with okf_version"))
    elif bundle.index_meta.get("schema_version") != schema.version:
        findings.append(
            Finding(
                "layout.schema-version",
                "index.md",
                f"bundle declares schema_version {bundle.index_meta.get('schema_version')!r}; tool expects {schema.version!r}",
            )
        )

    for directory in bundle.directories:
        if directory != bundle.root and not (directory / "index.md").is_file():
            findings.append(
                Finding("layout.missing-file", bundle.rel(directory / "index.md"), "every directory needs index.md")
            )

    for concept in bundle.concepts:
        declared = concept.meta.get("type")
        if declared != concept.type:
            findings.append(
                Finding(
                    "layout.type-location",
                    concept.rel,
                    f"this location holds a {concept.type}, but frontmatter says type: {declared}",
                )
            )
        pattern = schema.key_pattern(concept.type)
        if pattern and not re.match(pattern, concept.key):
            findings.append(Finding("layout.key", concept.rel, f"key {concept.key} does not match {pattern}"))
    return findings
