"""Frontmatter: accepted YAML forms, declared fields, value kinds, provenance."""

from __future__ import annotations

import re
from datetime import datetime, timezone

from ..bundle import Bundle, Concept, Finding

ORDER = 20

ACTOR_RE = re.compile(r"^(human:[A-Za-z0-9._-]+|process:[A-Za-z0-9._-]+|[A-Za-z0-9._-]+/[A-Za-z0-9._-]+)$")
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SOURCE_KEYS = {"id", "resource", "title"}


def _is_timestamp(value: str) -> bool:
    """True for an ISO 8601 timestamp with an offset that is also a real date and time."""
    if not TIMESTAMP_RE.match(value):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _stamp(value: object) -> str | None:
    if not isinstance(value, dict):
        return "expected { by, at }"
    if set(value) != {"by", "at"}:
        return "expected exactly the keys by and at"
    if not ACTOR_RE.match(value["by"]):
        return f"by must be human:<id>, process:<id> or <producer>/<version>, got {value['by']}"
    if not _is_timestamp(value["at"]):
        return f"at must be an ISO 8601 timestamp with an offset, got {value['at']}"
    return None


def _stamps(value: object) -> str | None:
    entries = value if isinstance(value, list) else [value]
    for entry in entries:
        problem = _stamp(entry)
        if problem:
            return problem
    return None


def _sources(value: object) -> str | None:
    if not isinstance(value, list):
        return "expected a list of { id, resource, title }"
    for entry in value:
        if not isinstance(entry, dict) or not entry.get("resource"):
            return "every source needs a resource"
        if not set(entry) <= SOURCE_KEYS:
            return f"unknown source keys: {sorted(set(entry) - SOURCE_KEYS)}"
    return None


def problem_with(value: object, spec: dict) -> str | None:
    """Return why `value` does not fit the field spec, or None when it does."""
    kind = spec["kind"]
    if kind == "actor_stamp":
        return _stamp(value)
    if kind == "actor_stamps":
        return _stamps(value)
    if kind == "sources":
        return _sources(value)
    if kind == "string_list":
        return None if isinstance(value, list) and all(isinstance(item, str) for item in value) else "expected a list like [a, b]"
    if not isinstance(value, str) or not value:
        return "expected a single value"
    if kind == "enum" and value not in spec["values"]:
        return f"must be one of {', '.join(spec['values'])}; got {value}"
    if kind == "boolean" and value not in ("true", "false"):
        return f"must be true or false; got {value}"
    if kind == "integer" and not re.match(r"^-?\d+$", value):
        return f"must be a whole number; got {value}"
    if kind == "timestamp" and not _is_timestamp(value):
        return f"must be an ISO 8601 timestamp with an offset; got {value}"
    if kind == "date" and not DATE_RE.match(value):
        return f"must be YYYY-MM-DD; got {value}"
    return None


def verified_by_human(concept: Concept) -> bool:
    value = concept.meta.get("verified")
    entries = value if isinstance(value, list) else [value]
    return any(isinstance(entry, dict) and str(entry.get("by", "")).startswith("human:") for entry in entries)


def check(bundle: Bundle, now: datetime | None = None) -> list[Finding]:
    schema = bundle.schema
    now = now or datetime.now(timezone.utc)
    findings: list[Finding] = []
    for concept in bundle.concepts:
        for error in concept.fm_errors:
            findings.append(Finding("frontmatter.syntax", concept.rel, error))
        fields = schema.fields(concept.type)
        for name, spec in fields.items():
            if name == "type":
                continue  # reported by layout.type-location
            if name not in concept.meta:
                if spec.get("required"):
                    findings.append(Finding("frontmatter.missing-field", concept.rel, f"missing required field {name}"))
                continue
            problem = problem_with(concept.meta[name], spec)
            if problem:
                findings.append(Finding("frontmatter.bad-value", concept.rel, f"{name}: {problem}"))
        for name in concept.meta:
            if name not in fields:
                findings.append(Finding("frontmatter.unknown-field", concept.rel, f"{name} is not a declared field of {concept.type}"))
        if schema.types[concept.type].get("human_verified") and not verified_by_human(concept):
            findings.append(
                Finding("frontmatter.reference-unverified", concept.rel, f"a {concept.type} must be verified by a human: actor")
            )
        stale = concept.meta.get("stale_after")
        if isinstance(stale, str) and _is_timestamp(stale):
            if datetime.fromisoformat(stale.replace("Z", "+00:00")) <= now:
                findings.append(Finding("stale.expired", concept.rel, f"content was due for review on {stale}", "warning"))
    return findings
