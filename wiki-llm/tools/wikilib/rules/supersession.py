"""Supersession: an ADR is Superseded exactly when another ADR supersedes it."""

from __future__ import annotations

from ..bundle import Bundle, Finding

ORDER = 85


def check(bundle: Bundle) -> list[Finding]:
    findings: list[Finding] = []
    decisions = bundle.of_type("ArchitectureDecision")
    superseded = {
        relation.concept.path
        for decision in decisions
        for relation in bundle.relations(decision, ["Supersedes"])
        if relation.concept is not None
    }
    for decision in decisions:
        if decision.status == "Superseded" and decision.path not in superseded:
            findings.append(Finding("supersession.status", decision.rel, "status is Superseded but no decision lists it under # Supersedes"))
        if decision.status != "Superseded" and decision.path in superseded:
            findings.append(Finding("supersession.status", decision.rel, "another decision supersedes this one; status must be Superseded"))
    return findings
