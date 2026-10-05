"""What a Feature or ChangeRequest has no TestCase or no Task for.

  tests  Requirements no TestCase links under `# Covers`. For a ChangeRequest,
         its new and modified Requirements; a link to the Requirement in the
         ChangeRequest or in its Feature counts.
  tasks  Design concepts no Task of the subject's own folder links under
         `# Planned scope`: those listed in a ChangeRequest's `## Target
         delta`, or linked from a Feature's `# Architecture` with a
         `# Pending changes` entry for the Feature. A concept the Feature
         reuses unchanged, or that another ChangeRequest changes, needs no
         Task of the Feature, and the schema allows none. Also each user
         story of the subject's folder that no Task of the folder links
         under `# Stories`.
  stories  Functional Requirements, not Wont, that no user story lists. For a
         ChangeRequest, its new and modified Requirements, listed by a story
         of its folder. For a Feature, a story of its folder or of a
         ChangeRequest that changes it counts, matched by key.
"""

from __future__ import annotations

from pathlib import Path

from . import markdown
from .bundle import Bundle, Concept
from .errors import ToolError
from .rules.content import PRIORITY_RE, TYPE_RE
from .rules.ids import changed_feature, requirement_ids


def subject(bundle: Bundle, type_name: str, key: str) -> Concept:
    found = [concept for concept in bundle.of_type(type_name) if concept.key == key]
    if len(found) != 1:
        raise ToolError(f"no {type_name} has the key {key}" if not found else f"{key} names {len(found)} {type_name}s")
    return found[0]


def _covered_anchors(bundle: Bundle) -> set[tuple[Path, str]]:
    """(file, lower-case anchor) of every Requirement a TestCase covers."""
    return {
        (relation.concept.path, relation.anchor.lower())
        for case in bundle.of_type("TestCase")
        for relation in bundle.relations(case, ["Covers"])
        if relation.kind == "Requirement"
    }


def tests(bundle: Bundle, concept: Concept) -> list[str]:
    covered = _covered_anchors(bundle)
    holders = [concept.path]
    if concept.type == "ChangeRequest":
        feature = changed_feature(bundle, concept)
        if feature is not None:
            holders.append(feature.path)
    return [
        requirement
        for requirement in requirement_ids(concept)
        if not any((path, requirement.lower()) in covered for path in holders)
    ]


def _design_targets(bundle: Bundle, concept: Concept) -> list[Concept]:
    if concept.type == "ChangeRequest":
        targets = [relation.concept for relation in bundle.relations(concept, bundle.schema.pending["delta"])]
    else:
        section = concept.section(bundle.schema.pending["feature_scope"])
        links = markdown.links(section.text) if section else []
        linked = [bundle.by_path.get(bundle.resolve(concept.path, target)[0]) for _, target in links]
        pending = [bundle.schema.pending["heading"]]
        targets = [
            target
            for target in linked
            if target is not None and any(entry.concept is concept for entry in bundle.relations(target, pending))
        ]
    unique = {target.path: target for target in targets if target is not None and bundle.schema.is_design(target.type)}
    return list(unique.values())


def tasks(bundle: Bundle, concept: Concept) -> list[str]:
    scope = bundle.schema.pending["task_scope"]
    owned = bundle.owned(concept, "Task")
    planned = {
        relation.concept.path
        for task in owned
        for relation in bundle.relations(task, scope)
        if relation.concept is not None
    }
    linked = {relation.path for task in owned for relation in bundle.relations(task, ["Stories"])}
    unplanned = [target.rel for target in _design_targets(bundle, concept) if target.path not in planned]
    unlinked = [story.rel for story in bundle.owned(concept, "UserStory") if story.path not in linked]
    return sorted(unplanned) + sorted(unlinked)


def _needs_story(concept: Concept) -> list[str]:
    """Functional Requirements of `concept` whose priority is not Wont."""
    section = concept.section(["Requirements"])
    if section is None:
        return []
    found = []
    for entry in markdown.sections(concept.body, 3, within=section):
        if not entry.heading.title.startswith("REQ-"):
            continue
        kinds = [kind.lower() for kind in TYPE_RE.findall(entry.text)]
        priorities = [priority.lower().replace("’", "'") for priority in PRIORITY_RE.findall(entry.text)]
        if kinds == ["functional"] and not {"wont", "won't"} & set(priorities):
            found.append(entry.heading.title)
    return found


def stories(bundle: Bundle, concept: Concept) -> list[str]:
    holders = [concept]
    if concept.type == "Feature":
        holders += [change for change in bundle.of_type("ChangeRequest") if changed_feature(bundle, change) is concept]
    listed = {
        relation.anchor.lower()
        for holder in holders
        for story in bundle.owned(holder, "UserStory")
        for relation in bundle.relations(story, ["Requirements"])
        if relation.kind == "Requirement"
    }
    return [requirement for requirement in _needs_story(concept) if requirement.lower() not in listed]


COVERAGE = {"tests": tests, "tasks": tasks, "stories": stories}


def report(bundle: Bundle, what: str, type_name: str, key: str) -> dict:
    concept = subject(bundle, type_name, key)
    uncovered = COVERAGE[what](bundle, concept)
    return {"ok": not uncovered, "subject": concept.key, "uncovered": uncovered}
