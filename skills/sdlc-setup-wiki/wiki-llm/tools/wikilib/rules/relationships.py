"""Relationships: legal target types, how many, and qualifiers."""

from __future__ import annotations

from .. import markdown
from ..bundle import Bundle, Finding

ORDER = 40


def check(bundle: Bundle) -> list[Finding]:
    schema = bundle.schema
    findings: list[Finding] = []
    for concept in bundle.concepts:
        for path, links in schema.link_headings(concept.type):
            section = concept.section(path)
            if section is None:
                continue
            name = " > ".join(path)
            legal = schema.targets(links)
            relations = bundle.relations(concept, path)
            seen: set = set()
            for relation in relations:
                label = relation.item.label or relation.item.text
                if not relation.item.target:
                    findings.append(Finding("relationships.target-type", concept.rel, f"{name}: list item '{label}' has no link"))
                    continue
                if relation.path is None:
                    findings.append(Finding("relationships.target-type", concept.rel, f"{name}: '{label}' must link a concept in the bundle"))
                    continue
                if relation.concept is None:
                    if relation.path.is_file():
                        findings.append(
                            Finding(
                                "relationships.target-type",
                                concept.rel,
                                f"{name}: '{label}' links {relation.item.target}, which is not a concept; link a concept's overview.md or its own file",
                            )
                        )
                    continue  # a missing target is reported by links.unresolved
                if relation.kind not in legal:
                    findings.append(
                        Finding(
                            "relationships.target-type",
                            concept.rel,
                            f"{name} may link {', '.join(legal)}; '{label}' is a {relation.kind}",
                        )
                    )
                identity = (relation.path, relation.anchor)
                if identity in seen:
                    findings.append(Finding("relationships.duplicate", concept.rel, f"{name}: '{label}' is listed more than once"))
                seen.add(identity)
                qualifier = links.get("qualifier")
                if qualifier and qualifier["required"] and relation.qualifier is None:
                    allowed = ", ".join(schema.qualifiers[qualifier["set"]])
                    findings.append(
                        Finding("relationships.qualifier", concept.rel, f"{name}: '{label}' needs a qualifier ({allowed}) right after the link")
                    )
            for line in markdown.loose_items(section.text):
                findings.append(
                    Finding(
                        "relationships.unparsed",
                        concept.rel,
                        f"{name}: '{line}' is not read as a relationship; write it as a top-level `*` list item",
                    )
                )
            if len(relations) < links.get("min", 0):
                findings.append(Finding("relationships.cardinality", concept.rel, f"{name} needs at least {links['min']} link(s)"))
            if "max" in links and len(relations) > links["max"]:
                findings.append(Finding("relationships.cardinality", concept.rel, f"{name} allows at most {links['max']} link(s)"))
    return findings
