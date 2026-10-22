"""Spec versions: each record names a version the target has had, an Approved
target was designed from its current version, and what was written from an
older version is reported."""

from __future__ import annotations

from .. import basis
from ..bundle import Bundle, Finding

ORDER = 78


def check(bundle: Bundle) -> list[Finding]:
    findings: list[Finding] = []

    for target in bundle.of_type(*basis.TARGETS):
        heading = basis.DESIGN_HEADING[target.type]
        has_field = "designBasedOn" in target.meta
        raw = target.meta.get("version")
        if isinstance(raw, str) and raw.lstrip("-").isdigit() and basis.version(target) is None:
            findings.append(Finding("basis.version", target.rel, f"version counts from 1; got {raw}"))
        if basis.designed(target) and not has_field:
            findings.append(Finding("basis.design", target.rel, f"# {heading} is written; add designBasedOn: the version it was designed from"))
        elif has_field and not basis.designed(target):
            findings.append(Finding("basis.design", target.rel, f"designBasedOn belongs only to a target whose # {heading} is written"))
        if target.status == "Approved" and basis.version(target) is not None:
            entry = basis.parse_entry(target.meta.get("designBasedOn"))
            if entry and entry[0] != basis.version(target):
                findings.append(
                    Finding(
                        "basis.approved",
                        target.rel,
                        f"status Approved needs a design of the current version {basis.version(target)}; # {heading} was designed from version {entry[0]}",
                    )
                )

    for record in basis.records(bundle):
        target, current = record.target, basis.version(record.target)
        if current is None:
            continue  # reported by frontmatter
        rel = record.holder.rel
        if record.version > current:
            findings.append(Finding("basis.ahead", rel, f"{record.field} names {target.key} version {record.version}; {target.key} is at version {current}"))
        elif record.version == current and record.at != basis.version_date(target):
            findings.append(
                Finding("basis.date", rel, f"{record.field} names {target.key} version {current} at {record.at}; that version is dated {basis.version_date(target)}")
            )
        elif basis.is_outdated(record):
            findings.append(
                Finding(
                    "basis.outdated",
                    rel,
                    f"written from {target.key} version {record.version}; it is now at version {current} ({basis.version_date(target)}): "
                    "update it, or record that it is still current",
                    "warning",
                )
            )

    for suite in bundle.of_type("TestSuite"):
        value = suite.meta.get("basedOn")
        if not isinstance(value, list):
            continue  # missing or malformed: reported by frontmatter
        named = [item.get("id") for item in value if isinstance(item, dict)]
        keys = [target.key for target in basis.verifies(bundle, suite)]
        for key in named:
            if key not in keys:
                findings.append(Finding("basis.target", suite.rel, f"basedOn names {key}, which is not under # Verifies"))
        for key in keys:
            if key not in named:
                findings.append(Finding("basis.target", suite.rel, f"{key} is under # Verifies; add its basedOn entry"))
    return findings
