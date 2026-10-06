"""Provenance stamps and log entries, written into files in place."""

from __future__ import annotations

import re
from datetime import datetime, timezone

from . import frontmatter, markdown, sync
from .schema import Schema

PROVENANCE = ("generated", "verified")


def now() -> str:
    """The current time as an ISO 8601 UTC timestamp, to the second."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def render(stamp: dict) -> str:
    return f"{{ by: {stamp['by']}, at: {stamp['at']} }}"


def stamps_of(value: object) -> list[dict]:
    """A `verified` value as a list of stamps; anything else gives an empty list."""
    entries = value if isinstance(value, list) else [value]
    return [entry for entry in entries if isinstance(entry, dict)]


def set_verified(text: str, stamps: list[dict]) -> str:
    """Write `verified` as one mapping, as a block list, or remove it when empty."""
    if not stamps:
        return frontmatter.set_field(text, "verified", None)
    if len(stamps) == 1:
        return frontmatter.set_field(text, "verified", render(stamps[0]))
    return frontmatter.set_field(text, "verified", "".join(f"\n  - {render(stamp)}" for stamp in stamps))


def add_verified(text: str, stamp: dict) -> str:
    meta, _, _ = frontmatter.parse(text)
    return set_verified(text, stamps_of(meta.get("verified")) + [stamp])


def authored_view(text: str, schema: Schema) -> str:
    """The part of a concept file a writer owns: frontmatter without the
    provenance fields, and the body without its generated sections and the
    sections whose edits are not a change of content (`# References`)."""
    lines, body = frontmatter.split(text)
    kept = []
    skipping = False
    for line in lines or []:
        match = frontmatter.KEY_RE.match(line)
        if match:
            skipping = match.group(1) in PROVENANCE
        if not skipping:
            kept.append(line)
    meta, _, _ = frontmatter.parse(text)
    type_name = meta.get("type")
    if isinstance(type_name, str) and type_name in schema.types and markdown.unclosed_fence(body) is None:
        specs = schema.headings(type_name)
        order = [spec["name"] for spec in specs]
        for spec in specs:
            if "generated" in spec or spec.get("stamped") is False:
                body = sync.apply_section(body, spec["name"], None, order)
    return "\n".join(kept) + "\n---\n" + body.strip()


def log_entries(text: str) -> set[tuple[str, str]]:
    """Every (date, entry text) of a log."""
    body = text.removeprefix("﻿")
    return {
        (section.heading.title, item.text)
        for section in markdown.sections(body, 2)
        for item in markdown.items(section.text)
    }


def add_log_entry(text: str, day: str, entry: str) -> str:
    """Add `* <entry>` under `## <day>`, creating that heading when it is
    missing: before the first older date, so the log stays newest first."""
    bom = "﻿" if text.startswith("﻿") else ""
    body = text.removeprefix("﻿")
    lines = body.rstrip("\n").split("\n")
    dated = markdown.sections(body, 2)
    same = next((section for section in dated if section.heading.title == day), None)
    if same is not None:
        last = min(same.end, len(lines))
        while last > same.start and not lines[last - 1].strip():
            last -= 1
        lines[last:last] = [f"* {entry}"]
    else:
        older = next((section for section in dated if section.heading.title < day), None)
        position = older.heading.line if older is not None else len(lines)
        block = [f"## {day}", "", f"* {entry}", ""]
        if position == len(lines):
            block = ["", *block[:-1]]
        lines[position:position] = block
    return bom + "\n".join(lines) + "\n"


SAFE_ID_RE = re.compile(r"[^A-Za-z0-9._-]")


def human(email: str) -> str:
    """`human:<id>` from the part of an email address before `@`."""
    return "human:" + SAFE_ID_RE.sub("-", email.split("@", 1)[0])
