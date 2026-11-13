"""TestSuites: case ids unique in a suite; each STORY-* group names a story of
the suite's target, links it under # Story, and holds cases that cover its
Requirements and acceptance criteria; steps a tester runs without the wiki,
with each Validation naming what it checks in bold; open questions keep a
group in Draft. Story drift (a story removed or renumbered after the tests
were written) is a warning: sdlc-write-stories may leave it, the test skills
fix it."""

from __future__ import annotations

import re

from .. import markdown
from ..bundle import Bundle, Concept, Finding
from ..sync import acs, case_id, story_link, suite_cases
from .stories import criteria

ORDER = 77

RUN_HEADINGS = ("Preconditions", "Steps", "Postconditions and cleanup")
SEE_STEP_RE = re.compile(r"\bsee step \d+", re.IGNORECASE)
BOLD_RE = re.compile(r"\*\*[^*]+\*\*")
NO_OPEN_QUESTIONS = ("Draft", "Deprecated")
GENERAL = "GENERAL"


def _key_re(bundle: Bundle) -> re.Pattern:
    prefixes = sorted({spec["prefix"] for spec in bundle.schema.types.values() if spec.get("prefix")} | {"REQ-"})
    return re.compile(rf"(?<![A-Za-z0-9_-])(?:{'|'.join(map(re.escape, prefixes))})[a-z0-9]+(?:-[a-z0-9]+)*")


def _requirements(bundle: Bundle, concept: Concept, heading: str) -> set[tuple]:
    return {(r.path, r.anchor.lower()) for r in bundle.relations(concept, [heading]) if r.kind == "Requirement"}


def _count(story: Concept) -> int:
    section = story.section(["Acceptance criteria"])
    return len(criteria(section.text)[0]) if section else 0


def _warn(rule: str, rel: str, message: str) -> Finding:
    return Finding(rule, rel, message, "warning")


def _open_questions(group: Concept, findings: list[Finding]) -> None:
    section = group.section(["Open questions"])
    if section is None:
        return
    items, stray = criteria(section.text)
    if stray and stray != ["None"]:
        findings.append(Finding("tests.open-questions", group.rel, "# Open questions must be a numbered list and nothing else"))
    for number, item in enumerate(items, start=1):
        if not markdown.links(item):
            findings.append(Finding("tests.open-questions", group.rel, f"open question {number} must link the Requirement, story, design or decision it is about"))
    if items and group.status not in NO_OPEN_QUESTIONS:
        findings.append(Finding("tests.open-questions", group.rel, f"a group with open questions stays Draft, not {group.status}"))


def _story_group(bundle: Bundle, group: Concept, stories: dict[str, Concept], targets: str, findings: list[Finding]) -> None:
    linked = [r for r in bundle.relations(group, ["Story"]) if r.path is not None]
    if not linked or linked[0].path.stem != group.key:
        findings.append(Finding("tests.group-story", group.rel, f"# Story must link {group.key}, the story this folder is named after"))
    story = stories.get(group.key)
    if story is None:
        findings.append(_warn("tests.story-folder", group.rel, f"{group.key} is not a user story of {targets}; move its cases to the folder of their story or to GENERAL"))
        return
    count, covered = _count(story), set()
    for case in bundle.owned(group, "TestCase"):
        link = story_link(bundle, case, group.key)
        numbers = acs(link) if link else None
        if numbers is None:
            findings.append(Finding("tests.story-ac", case.rel, f"# Covers must link {group.key} with the criteria it proves, as `— AC 1, 3`"))
            continue
        missing = [n for n in numbers if n > count]
        if missing:
            findings.append(_warn("tests.story-ac", case.rel, f"{group.key} has {count} acceptance criteria; AC {', '.join(map(str, missing))} does not exist"))
        covered.update(numbers)
        if not _requirements(bundle, case, "Covers") & _requirements(bundle, story, "Requirements"):
            findings.append(_warn("tests.story-covers", case.rel, f"the case covers none of the Requirements of {group.key}; cover one, or move it to GENERAL"))
    uncovered = [n for n in range(1, count + 1) if n not in covered]
    if uncovered:
        findings.append(_warn("tests.story-ac", group.rel, f"AC {', '.join(map(str, uncovered))} of {group.key} is covered by no case of this group"))


def _general_group(bundle: Bundle, group: Concept, findings: list[Finding]) -> None:
    if group.section(["Story"]) is not None:
        findings.append(Finding("tests.group-story", group.rel, "GENERAL holds cases of no single story; it has no # Story"))
    for case in bundle.owned(group, "TestCase"):
        stories = [r.path.stem for r in bundle.relations(case, ["Covers"]) if r.path is not None and r.path.stem.startswith("STORY-")]
        if stories:
            findings.append(Finding("tests.general-story", case.rel, f"a GENERAL case links no user story ({', '.join(stories)}); move it to the story's group, or drop the link"))


def _steps(case: Concept, key_re: re.Pattern, findings: list[Finding]) -> None:
    for heading in RUN_HEADINGS:
        part = case.section([heading])
        if part is None:
            continue
        keys = sorted(set(key_re.findall(part.text)))
        if keys:
            findings.append(Finding("tests.step-names", case.rel, f"# {heading} uses wiki keys {', '.join(keys)}; write the real name (table, topic, method and path) instead"))
        if SEE_STEP_RE.search(part.text):
            findings.append(Finding("tests.step-names", case.rel, f"# {heading} says 'see Step <n>'; each Action says itself what to do"))
    steps = case.section(["Steps"])
    header, rows = markdown.table(steps.text) if steps else ([], [])
    if "Validation" not in header:
        return  # a wrong table is reported by content.table
    column = header.index("Validation")
    for number, row in enumerate(rows, start=1):
        if column < len(row) and row[column] and not BOLD_RE.search(row[column]):
            findings.append(Finding("tests.validation-bold", case.rel, f"step {number}: the Validation names what it checks in bold, such as **status**"))


def _suite(bundle: Bundle, suite: Concept, key_re: re.Pattern, findings: list[Finding]) -> None:
    by_id: dict[int, list[Concept]] = {}
    for case in suite_cases(bundle, suite):
        by_id.setdefault(case_id(case), []).append(case)
    for number, same in sorted(by_id.items()):
        if len(same) > 1:
            for case in same:
                findings.append(Finding("tests.case-id", case.rel, f"id {number} is used by {len(same)} cases of {suite.key}; give each case its own"))

    targets = [r.concept for r in bundle.relations(suite, ["Verifies"]) if r.concept is not None]
    stories = {story.key: story for target in targets for story in bundle.owned(target, "UserStory")}
    names = " or ".join(t.key for t in targets) or "the suite target"
    for group in bundle.owned(suite, "TestGroup"):
        _open_questions(group, findings)
        if group.key == GENERAL:
            _general_group(bundle, group, findings)
        else:
            _story_group(bundle, group, stories, names, findings)
        for case in bundle.owned(group, "TestCase"):
            _steps(case, key_re, findings)


def check(bundle: Bundle) -> list[Finding]:
    findings: list[Finding] = []
    key_re = _key_re(bundle)
    for suite in bundle.of_type("TestSuite"):
        _suite(bundle, suite, key_re, findings)
    return findings
