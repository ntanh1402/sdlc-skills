"""User stories: the story sentence, Given/When/Then criteria traced to the
listed Requirements, at least one Functional Requirement, links that stay in
the story's own folder; a Task links only stories of its own folder."""

from __future__ import annotations

import re
from pathlib import Path

from .. import markdown
from ..bundle import Bundle, Concept, Finding
from .content import TYPE_RE
from .ids import changed_feature

ORDER = 75

NUMBERED_RE = re.compile(r"^\d+[.)]\s+")
SENTENCE = (("As a", re.compile(r"\bas an?\b")), ("I want", re.compile(r"\bi want\b")), ("so that", re.compile(r"\bso that\b")))
STEPS = ("given", "when", "then")

Requirement = tuple[Path, str]  # (file, lower-case anchor)


def _plain(text: str) -> str:
    return " ".join(text.replace("*", "").replace("_", " ").split()).lower()


def _sentence(concept: Concept) -> str:
    """The prose between the title and the first heading after it."""
    top = markdown.sections(concept.body, 1)
    return markdown.strip_fences(top[0].text) if top else ""


def criteria(text: str) -> tuple[list[str], list[str]]:
    """(numbered items, lines that belong to no item) of an Acceptance criteria section."""
    found: list[list[str]] = []
    stray: list[str] = []
    current: list[str] | None = None
    for line in markdown.strip_fences(text).split("\n"):
        if NUMBERED_RE.match(line):
            current = [NUMBERED_RE.sub("", line, count=1)]
            found.append(current)
        elif not line.strip():
            continue
        elif current is not None:
            current.append(line.strip())
        else:
            stray.append(line.strip())
    return [" ".join(item) for item in found], stray


def _cited(bundle: Bundle, concept: Concept, text: str) -> set[Requirement]:
    cited: set[Requirement] = set()
    for _, target in markdown.links(text):
        path, anchor = bundle.resolve(concept.path, target)
        holder = bundle.by_path.get(path) if path else None
        if holder is not None and holder.type in ("Feature", "ChangeRequest") and anchor.lower().startswith("req-"):
            cited.add((path, anchor.lower()))
    return cited


def _kind(holder: Concept, anchor: str) -> str | None:
    """The type of one Requirement, lower case; None when it has not exactly
    one (content.requirement reports that) or is missing (links.anchor does)."""
    section = holder.section(["Requirements"])
    if section is None:
        return None
    for entry in markdown.sections(holder.body, 3, within=section):
        if entry.heading.title.lower() == anchor:
            types = [match.lower() for match in TYPE_RE.findall(entry.text)]
            return types[0] if len(types) == 1 else None
    return None


def _story(bundle: Bundle, concept: Concept, findings: list[Finding]) -> None:
    rel = concept.rel
    sentence = _plain(_sentence(concept))
    missing = [words for words, pattern in SENTENCE if not pattern.search(sentence)]
    if missing:
        findings.append(
            Finding("story.sentence", rel, f"the story sentence after the title needs 'As a …, I want …, so that …'; missing: {', '.join(missing)}")
        )

    listed_relations = [relation for relation in bundle.relations(concept, ["Requirements"]) if relation.kind == "Requirement"]
    listed = {(relation.path, relation.anchor.lower()): relation for relation in listed_relations}
    section = concept.section(["Acceptance criteria"])
    cited: set[Requirement] = set()
    if section is not None:
        items, stray = criteria(section.text)
        if not items or stray:
            findings.append(Finding("story.criteria", rel, "Acceptance criteria must be a numbered list and nothing else"))
        for number, item in enumerate(items, start=1):
            words = _plain(item)
            absent = [step.capitalize() for step in STEPS if not re.search(rf"\b{step}\b", words)]
            if absent:
                findings.append(Finding("story.criteria", rel, f"criterion {number} needs Given, When and Then; missing: {', '.join(absent)}"))
            these = _cited(bundle, concept, item)
            if not these:
                findings.append(Finding("story.criteria", rel, f"criterion {number} must link the Requirement it shows"))
            for requirement in sorted(these - set(listed), key=str):
                findings.append(
                    Finding("story.trace", rel, f"criterion {number} links {requirement[1].upper()}, which is not under # Requirements")
                )
            cited |= these
    for requirement in sorted(set(listed) - cited, key=str):
        findings.append(Finding("story.trace", rel, f"{requirement[1].upper()} is under # Requirements but no criterion links it"))

    for relation in listed_relations:
        if relation.concept is not concept.owner:
            findings.append(
                Finding("story.requirement-place", rel, f"{relation.anchor.upper()} must be linked in the overview.md of this story's own folder")
            )
    kinds = [_kind(relation.concept, relation.anchor.lower()) for relation in listed_relations]
    if kinds and None not in kinds and "functional" not in kinds:
        findings.append(Finding("story.functional", rel, "a story lists at least one Functional Requirement"))

    affects = [relation for relation in bundle.relations(concept, ["Affects"]) if relation.concept is not None]
    if affects and (concept.owner is None or concept.owner.type != "ChangeRequest"):
        findings.append(Finding("story.affects", rel, "# Affects belongs only to a story in a ChangeRequest's folder"))
    elif affects:
        feature = changed_feature(bundle, concept.owner)
        for relation in affects:
            target = relation.concept
            if target.type == "UserStory" and target.owner is not feature:
                findings.append(Finding("story.affects", rel, f"{target.key} is not a story of the Feature this ChangeRequest changes"))


def check(bundle: Bundle) -> list[Finding]:
    findings: list[Finding] = []
    for concept in bundle.of_type("UserStory"):
        _story(bundle, concept, findings)
    for task in bundle.of_type("Task"):
        for relation in bundle.relations(task, ["Stories"]):
            target = relation.concept
            if target is not None and target.type == "UserStory" and target.owner is not task.owner:
                findings.append(Finding("task.stories-place", task.rel, f"{target.key} is not a story of this Task's folder"))
    return findings
