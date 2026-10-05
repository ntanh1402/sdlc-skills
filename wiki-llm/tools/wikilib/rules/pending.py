"""Pending changes: an unbuilt Design concept names the work that will build it.

Terms used below:
  parent   a Feature or ChangeRequest
  open     a parent whose status is listed in schema `pending.open_parents`
  covers   a Task covers a concept when its `# Planned scope` links it
  entry    one list item under a concept's `# Pending changes`
  closed   a Task with status Done: its code is merged
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .. import markdown
from ..bundle import Bundle, Concept, Finding

ORDER = 80


def _as(qualifier: str | None) -> str:
    """' as <qualifier>' for a message; empty when the entry has no recognised qualifier."""
    return f" as {qualifier}" if qualifier else ""


def check(bundle: Bundle) -> list[Finding]:
    schema = bundle.schema
    config = schema.pending
    heading = [config["heading"]]
    open_parents: dict[str, list[str]] = config["open_parents"]
    status_by_change: dict[str, str] = config["status_by_change"]
    pending_statuses = set(status_by_change.values())
    findings: list[Finding] = []

    def is_open(parent: Concept) -> bool:
        return parent.status in open_parents.get(parent.type, [])

    # (parent file, concept file) -> Tasks of that parent covering that concept
    coverage: dict[tuple[Path, Path], list[Concept]] = defaultdict(list)
    task_scope: list[tuple[Concept, Concept, str | None]] = []
    for task in bundle.of_type("Task"):
        if task.owner is None:
            continue
        for relation in bundle.relations(task, config["task_scope"]):
            if relation.concept is not None and schema.is_design(relation.concept.type):
                coverage[(task.owner.path, relation.concept.path)].append(task)
                task_scope.append((task, relation.concept, relation.qualifier))

    def all_done(parent: Concept, concept: Concept) -> bool:
        tasks = coverage.get((parent.path, concept.path), [])
        return bool(tasks) and all(task.status == "Done" for task in tasks)

    # parent file -> every Task in its folder
    tasks_of: dict[Path, list[Concept]] = defaultdict(list)
    for task in bundle.of_type("Task"):
        if task.owner is not None:
            tasks_of[task.owner.path].append(task)

    def all_closed(parent: Concept) -> bool:
        tasks = tasks_of.get(parent.path, [])
        return bool(tasks) and all(task.status == "Done" for task in tasks)

    removing = status_by_change["removed"]

    entries: dict[Path, list[tuple[Concept, str | None]]] = defaultdict(list)
    for concept in bundle.concepts:
        if not schema.is_design(concept.type):
            continue
        has_section = concept.section(heading) is not None
        is_pending = concept.status in pending_statuses
        if concept.status == removing and not bundle.relations(concept, heading):
            findings.append(
                Finding(
                    "pending.removing-file",
                    concept.rel,
                    f"status {removing} with no pending entry left: the removal is built; set the status to Deprecated "
                    "and remove the section (the file stays: the Task and the request that removed it link it)",
                )
            )
        elif is_pending and not has_section:
            findings.append(Finding("pending.presence", concept.rel, f"status {concept.status} needs a # {heading[0]} section"))
        if has_section and not is_pending:
            findings.append(Finding("pending.presence", concept.rel, f"status {concept.status} must not have a # {heading[0]} section"))
        for relation in bundle.relations(concept, heading):
            parent = relation.concept
            if parent is None or parent.type not in open_parents:
                continue  # reported by the relationships rule
            entries[concept.path].append((parent, relation.qualifier))
            if not is_open(parent):
                findings.append(
                    Finding("pending.parent-open", concept.rel, f"{parent.key} has status {parent.status}; its pending entry must be removed")
                )
            if parent.type == "ChangeRequest":
                declared = any(
                    item.concept is concept and item.qualifier == relation.qualifier
                    for item in bundle.relations(parent, config["delta"])
                )
                where = " > ".join(config["delta"])
            else:
                section = parent.section(config["feature_scope"])
                targets = {bundle.resolve(parent.path, target)[0] for _, target in markdown.links(section.text)} if section else set()
                declared = concept.path in targets
                where = " > ".join(config["feature_scope"])
            if not declared:
                findings.append(
                    Finding("pending.undeclared", concept.rel, f"{parent.key} does not list this concept{_as(relation.qualifier)} under {where}")
                )
            if all_done(parent, concept):
                findings.append(
                    Finding("pending.leftover", concept.rel, f"every Task of {parent.key} that covers this concept is Done; remove the entry")
                )
        qualifiers = {qualifier for _, qualifier in entries[concept.path] if qualifier}
        if is_pending and qualifiers:
            expected = next(status_by_change[change] for change in status_by_change if change in qualifiers)
            if concept.status != expected:
                findings.append(
                    Finding("pending.status", concept.rel, f"pending entries ({', '.join(sorted(qualifiers))}) need status {expected}, not {concept.status}")
                )

    def has_entry(concept: Concept, parent: Concept, qualifier: str | None) -> bool:
        return any(item is parent and change == qualifier for item, change in entries[concept.path])

    for change in bundle.of_type("ChangeRequest"):
        if not is_open(change):
            continue
        for relation in bundle.relations(change, config["delta"]):
            concept = relation.concept
            if concept is None or not schema.is_design(concept.type) or all_done(change, concept):
                continue
            if not has_entry(concept, change, relation.qualifier):
                findings.append(
                    Finding("pending.missing-delta", concept.rel, f"{change.key} lists this concept{_as(relation.qualifier)}; add a pending entry for it")
                )

    for change in bundle.of_type("ChangeRequest"):
        if all_closed(change) and change.status != "Implemented":
            findings.append(
                Finding("pending.request-implemented", change.rel, f"every Task of {change.key} is Done; set its status to Implemented, not {change.status}")
            )
    for feature in bundle.of_type("Feature"):
        if feature.status == "InDev" and all_closed(feature):
            findings.append(
                Finding("pending.feature-built", feature.rel, f"every Task of {feature.key} is Done; set its status to Released when it ships", "warning")
            )

    for task, concept, qualifier in task_scope:
        if task.status == "Done":
            continue
        if not has_entry(concept, task.owner, qualifier):
            findings.append(
                Finding(
                    "pending.missing-task",
                    concept.rel,
                    f"{task.key} ({task.status}) plans this concept{_as(qualifier)}; add a pending entry for {task.owner.key}",
                )
            )
    return findings
