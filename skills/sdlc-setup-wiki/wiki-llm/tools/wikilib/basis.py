"""Spec versions: what each design, story, Task and TestSuite was written from.

A Feature or ChangeRequest (a target) carries `version` and `versionDate`.
What is written from it records the version it read:

  designBasedOn  on the target itself, once `# Architecture` / `# Delta` is written
  basedOn        on a Task or user story: its own folder's target
  basedOn        on a TestSuite: a list, one entry per target under `# Verifies`

A record is outdated when it names an older version than the target's.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from . import markdown
from .bundle import Bundle, Concept

TARGETS = ("Feature", "ChangeRequest")
DESIGN_HEADING = {"Feature": "Architecture", "ChangeRequest": "Delta"}
NUMBER_RE = re.compile(r"^[1-9]\d*$")


@dataclass(frozen=True)
class Record:
    holder: Concept  # the file that carries the field
    field: str  # designBasedOn or basedOn
    target: Concept  # the Feature or ChangeRequest it was written from
    version: int
    at: str


def version(target: Concept) -> int | None:
    value = target.meta.get("version")
    return int(value) if isinstance(value, str) and NUMBER_RE.match(value) else None


def version_date(target: Concept) -> str:
    value = target.meta.get("versionDate")
    return value if isinstance(value, str) else ""


def designed(target: Concept) -> bool:
    """True once the target's `# Architecture` or `# Delta` is not None."""
    section = target.section([DESIGN_HEADING[target.type]])
    return section is not None and not markdown.is_none(section.text)


def parse_entry(value: object) -> tuple[int, str] | None:
    if not isinstance(value, dict):
        return None
    number, at = value.get("version"), value.get("at")
    if not isinstance(number, str) or not NUMBER_RE.match(number) or not isinstance(at, str):
        return None  # a bad value is reported by frontmatter.bad-value
    return int(number), at


def records(bundle: Bundle) -> list[Record]:
    """Every well-formed version record of the bundle."""
    found: list[Record] = []
    for target in bundle.of_type(*TARGETS):
        entry = parse_entry(target.meta.get("designBasedOn"))
        if entry:
            found.append(Record(target, "designBasedOn", target, *entry))
    for holder in bundle.of_type("Task", "UserStory"):
        entry = parse_entry(holder.meta.get("basedOn"))
        if entry and holder.owner is not None and holder.owner.type in TARGETS:
            found.append(Record(holder, "basedOn", holder.owner, *entry))
    for suite in bundle.of_type("TestSuite"):
        value = suite.meta.get("basedOn")
        verified = {target.key: target for target in verifies(bundle, suite)}
        for item in value if isinstance(value, list) else []:
            entry = parse_entry(item)
            target = verified.get(item.get("id")) if isinstance(item, dict) else None
            if entry and target is not None:
                found.append(Record(suite, "basedOn", target, *entry))
    return found


def verifies(bundle: Bundle, suite: Concept) -> list[Concept]:
    return [
        relation.concept
        for relation in bundle.relations(suite, ["Verifies"])
        if relation.concept is not None and relation.concept.type in TARGETS
    ]


def is_outdated(record: Record) -> bool:
    """Written from an older version. A Done Task is history and never outdated."""
    current = version(record.target)
    if current is None or record.version >= current:
        return False
    return not (record.holder.type == "Task" and record.holder.status == "Done")


def outdated(bundle: Bundle, target: Concept) -> list[Record]:
    return [record for record in records(bundle) if record.target is target and is_outdated(record)]


def report(bundle: Bundle, target: Concept) -> dict:
    found = outdated(bundle, target)
    return {
        "ok": not found,
        "subject": target.key,
        "version": version(target),
        "versionDate": version_date(target),
        "outdated": [
            {"path": record.holder.rel, "type": record.holder.type, "field": record.field, "version": record.version, "at": record.at}
            for record in sorted(found, key=lambda item: item.holder.rel)
        ],
    }
