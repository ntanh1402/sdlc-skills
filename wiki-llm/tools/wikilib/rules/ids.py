"""IDs: keys unique per type in an application; requirement and story keys
belong to one Feature; two open ChangeRequests do not add the same new
requirement key."""

from __future__ import annotations

import re
from collections import defaultdict

from .. import markdown
from ..bundle import Bundle, Concept, Finding

ORDER = 60

REQ_HEADING_RE = re.compile(r"^REQ-")
NAME = r"[a-z0-9]+(-[a-z0-9]+)*"
# Keys of these types are unique only inside their owner, or are fixed names.
LOCAL_KEYS = {"Application", "Reference", "Convention", "Glossary", "TestCase"}


def requirement_ids(concept: Concept) -> list[str]:
    """IDs of the `### REQ-*` entries under `# Requirements`."""
    section = concept.section(["Requirements"])
    if section is None:
        return []
    return [
        entry.heading.title
        for entry in markdown.sections(concept.body, 3, within=section)
        if REQ_HEADING_RE.match(entry.heading.title)
    ]


def feature_slug(feature: Concept) -> str:
    return feature.key[len("FEAT-") :]


def changed_feature(bundle: Bundle, change: Concept) -> Concept | None:
    """The one Feature a ChangeRequest links under `# Changes`."""
    for relation in bundle.relations(change, ["Changes"]):
        if relation.concept is not None and relation.concept.type == "Feature":
            return relation.concept
    return None


def _collisions(bundle: Bundle) -> list[Finding]:
    """Open ChangeRequests on one Feature that add the same requirement key,
    which the Feature does not have yet."""
    open_statuses = bundle.schema.pending["open_requests"]
    added: dict[tuple[str, str], list[Concept]] = defaultdict(list)
    for change in bundle.of_type("ChangeRequest"):
        feature = changed_feature(bundle, change)
        if feature is None or change.status not in open_statuses:
            continue
        existing = set(requirement_ids(feature))
        for requirement in set(requirement_ids(change)) - existing:
            added[(feature.rel, requirement)].append(change)
    findings: list[Finding] = []
    for (_, requirement), changes in sorted(added.items()):
        if len(changes) < 2:
            continue
        keys = " and ".join(sorted(change.key for change in changes))
        for change in changes:
            findings.append(
                Finding(
                    "ids.requirement-collision",
                    change.rel,
                    f"{requirement} is added by {keys}, both open; give one a new name with `wiki_llm.py rename`",
                )
            )
    return findings


def check(bundle: Bundle) -> list[Finding]:
    findings: list[Finding] = []

    seen: dict[tuple[str, str, str], list[Concept]] = defaultdict(list)
    for concept in bundle.concepts:
        if concept.type not in LOCAL_KEYS:
            seen[(concept.app, concept.type, concept.key)].append(concept)
    for (_, type_name, key), concepts in seen.items():
        if len(concepts) > 1:
            for concept in concepts:
                findings.append(
                    Finding("ids.duplicate-key", concept.rel, f"{type_name} key {key} is used {len(concepts)} times in this application")
                )

    for concept in bundle.of_type("Feature", "ChangeRequest"):
        owner = concept if concept.type == "Feature" else changed_feature(bundle, concept)
        ids = requirement_ids(concept)
        for requirement in sorted({item for item in ids if ids.count(item) > 1}):
            findings.append(Finding("ids.requirement-duplicate", concept.rel, f"{requirement} appears more than once"))
        if owner is None:
            continue
        pattern = re.compile(rf"^REQ-{re.escape(feature_slug(owner))}-{NAME}$")
        for requirement in ids:
            if not pattern.match(requirement):
                findings.append(
                    Finding(
                        "ids.requirement-format",
                        concept.rel,
                        f"{requirement} must be REQ-{feature_slug(owner)}-<name>, lower-case words joined by -, because it belongs to {owner.key}",
                    )
                )
    for story in bundle.of_type("UserStory"):
        holder = story.owner
        feature = changed_feature(bundle, holder) if holder is not None and holder.type == "ChangeRequest" else holder
        if feature is None or feature.type != "Feature":
            continue
        if not re.match(rf"^STORY-{re.escape(feature_slug(feature))}-{NAME}$", story.key):
            findings.append(
                Finding(
                    "ids.story-format",
                    story.rel,
                    f"{story.key} must be STORY-{feature_slug(feature)}-<name>, lower-case words joined by -, because it belongs to {feature.key}",
                )
            )
    findings.extend(_collisions(bundle))
    return findings
