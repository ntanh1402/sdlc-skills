"""Headings: title, required headings, order, undeclared headings, nesting."""

from __future__ import annotations

from .. import markdown
from ..bundle import Bundle, Concept, Finding

ORDER = 30


def _check_level(
    concept: Concept,
    specs: list[dict],
    found: list[markdown.Section],
    where: str,
    findings: list[Finding],
    strict: bool,
) -> None:
    """Compare the sections found at one level with their specs."""
    declared = [spec["name"] for spec in specs]
    titles = [section.heading.title for section in found]
    for title in titles:
        if title not in declared and strict:
            findings.append(Finding("headings.unknown", concept.rel, f"{where}{title} is not a declared heading of {concept.type}"))
    for title in sorted({title for title in titles if titles.count(title) > 1 and title in declared}):
        findings.append(Finding("headings.duplicate", concept.rel, f"{where}{title} appears more than once"))
    for spec in specs:
        if spec["presence"] == "required" and spec.get("origin") != "generated" and spec["name"] not in titles:
            findings.append(Finding("headings.missing", concept.rel, f"missing required heading {where}{spec['name']}"))
    present = [title for title in titles if title in declared]
    if present != sorted(present, key=declared.index):
        findings.append(
            Finding("headings.order", concept.rel, f"headings under {where or 'the title'} must follow this order: {', '.join(declared)}")
        )


def _check_nested(concept: Concept, spec: dict, section: markdown.Section, depth: int, findings: list[Finding]) -> None:
    nested = spec.get("nested")
    if spec.get("allow_none") and markdown.is_none(section.text):
        allowed = spec.get("none_statuses")
        if allowed is not None and concept.status not in allowed:
            findings.append(
                Finding(
                    "headings.none-not-allowed",
                    concept.rel,
                    f"{spec['name']} may be None only while status is {' or '.join(allowed)}",
                )
            )
        return
    if not nested:
        return
    children = markdown.sections(concept.body, depth + 1, within=section)
    _check_level(concept, nested, children, f"{spec['name']} > ", findings, strict=False)
    for child_spec in nested:
        for child in children:
            if child.heading.title == child_spec["name"]:
                _check_nested(concept, child_spec, child, depth + 1, findings)


def check(bundle: Bundle) -> list[Finding]:
    schema = bundle.schema
    findings: list[Finding] = []
    for concept in bundle.concepts:
        spec = schema.types[concept.type]
        title_rule = spec.get("title", "title")
        top = markdown.sections(concept.body, 1)
        if title_rule != "free":
            expected = title_rule.split(":", 1)[1] if title_rule.startswith("fixed:") else concept.title
            first = markdown.headings(concept.body)[:1]
            if not first or first[0].level != 1 or first[0].title != expected:
                findings.append(Finding("headings.title", concept.rel, f"the first heading must be '# {expected}'"))
                continue
            if spec.get("title_nested"):
                _check_nested(concept, {"name": expected, "nested": spec["title_nested"]}, top[0], 1, findings)
            top = top[1:]
        if spec.get("free_headings"):
            continue
        specs = schema.headings(concept.type)
        _check_level(concept, specs, top, "", findings, strict=True)
        for heading_spec in specs:
            for section in top:
                if section.heading.title == heading_spec["name"]:
                    _check_nested(concept, heading_spec, section, 1, findings)
    return findings
