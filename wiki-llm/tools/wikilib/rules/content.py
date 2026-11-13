"""Content shape: code fences, requirement entries, tables, diagrams, payload examples, logs."""

from __future__ import annotations

import json
import re

from .. import markdown
from ..bundle import Bundle, Concept, Finding

ORDER = 70

PRIORITY_RE = re.compile(r"\*\*(Must|Should|Could|Won(?:'|’)t|Wont)\*\*", re.IGNORECASE)
TYPE_RE = re.compile(r"\b(Non[- ]?functional|Functional|Constraint)\s*\.", re.IGNORECASE)
METHOD_RE = re.compile(r"\bVerified by\s+(test|inspection|demo)\s*\.", re.IGNORECASE)
LOG_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _walk(specs: list[dict], prefix: list[str]):
    for spec in specs:
        path = prefix + [spec["name"]]
        yield path, spec
        yield from _walk(spec.get("nested", []), path)


def _requirements(concept: Concept, spec: dict, section: markdown.Section, findings: list[Finding]) -> None:
    entries = [
        entry for entry in markdown.sections(concept.body, 3, within=section) if entry.heading.title.startswith("REQ-")
    ]
    if len(entries) < spec["requirements"]["min"]:
        findings.append(Finding("content.requirement", concept.rel, "Requirements needs at least one ### REQ-* entry"))
    for entry in entries:
        name = entry.heading.title
        if len(PRIORITY_RE.findall(entry.text)) != 1:
            findings.append(Finding("content.requirement", concept.rel, f"{name} needs exactly one priority: **Must**, **Should**, **Could** or **Wont**"))
        if len(TYPE_RE.findall(entry.text)) != 1:
            findings.append(Finding("content.requirement", concept.rel, f"{name} needs exactly one type: Functional, Nonfunctional or Constraint"))
        if len(METHOD_RE.findall(entry.text)) != 1:
            findings.append(Finding("content.requirement", concept.rel, f"{name} needs exactly one 'Verified by test|inspection|demo.'"))


def _table(concept: Concept, spec: dict, section: markdown.Section, findings: list[Finding]) -> None:
    name = spec["name"]
    header, rows = markdown.table(section.text)
    if header != spec["table"]:
        findings.append(Finding("content.table", concept.rel, f"{name} needs a table with columns {' | '.join(spec['table'])}"))
    elif not rows or any(len(row) != len(header) or not all(row) for row in rows):
        findings.append(Finding("content.table", concept.rel, f"{name} needs at least one row and no empty cells"))


def _mermaid(concept: Concept, spec: dict, section: markdown.Section, findings: list[Finding]) -> None:
    if spec["mermaid"] not in markdown.mermaid_kinds(section.text):
        findings.append(Finding("content.mermaid", concept.rel, f"{spec['name']} needs a Mermaid {spec['mermaid']} block"))


def _names(text: str) -> tuple[list[str], list[str]]:
    """(all field names, required field names) from a Header or Body table."""
    header, rows = markdown.table(text)
    if not header or "Required" not in header:
        return [], []
    required_column = header.index("Required")
    names = [row[0].strip("`") for row in rows if row]
    required = [row[0].strip("`") for row in rows if len(row) > required_column and row[required_column] == "yes"]
    return names, required


def _payload(concept: Concept, findings: list[Finding]) -> None:
    example = concept.folder / "payload.example.json"
    if not example.is_file():
        return  # reported by layout.missing-file
    try:
        data = json.loads(example.read_bytes().decode("utf-8"))
    except UnicodeDecodeError:
        findings.append(Finding("content.payload", concept.rel, "payload.example.json is not valid UTF-8; save it as UTF-8"))
        return
    except json.JSONDecodeError as error:
        findings.append(Finding("content.payload", concept.rel, f"payload.example.json is not valid JSON: {error.msg}"))
        return
    if not isinstance(data, dict) or not {"key", "headers", "body"} <= set(data):
        findings.append(Finding("content.payload", concept.rel, "payload.example.json needs the keys key, headers and body"))
        return
    for json_key, heading in (("headers", "Header"), ("body", "Body")):
        if not isinstance(data[json_key], dict):
            findings.append(Finding("content.payload", concept.rel, f"example {json_key} must be a JSON object of field names and values"))
            continue
        section = concept.section(["Payload", heading])
        if section is None:
            continue
        names, required = _names(section.text)
        for name in data[json_key]:
            if name not in names:
                findings.append(Finding("content.payload", concept.rel, f"example {json_key} field {name} is missing from the {heading} table"))
        for name in required:
            if name not in data[json_key]:
                findings.append(Finding("content.payload", concept.rel, f"required {heading} field {name} is missing from payload.example.json"))


def _log(bundle: Bundle, concept: Concept, findings: list[Finding]) -> None:
    path = concept.folder / "log.md"
    if not path.is_file():
        return  # reported by layout.missing-file
    rel = bundle.rel(path)
    body = bundle.text(path).removeprefix("\ufeff")
    _fence(rel, body, findings)
    found = markdown.headings(body)
    if not found or found[0].level != 1:
        findings.append(Finding("content.log", rel, "a log starts with a '# <title>' heading"))
    dates = [section for section in markdown.sections(body, 2)]
    titles = [section.heading.title for section in dates]
    if any(not LOG_DATE_RE.match(title) for title in titles):
        findings.append(Finding("content.log", rel, "log headings must be '## YYYY-MM-DD'"))
        return
    if titles != sorted(titles, reverse=True):
        findings.append(Finding("content.log", rel, "log dates must be newest first"))
    if len(titles) != len(set(titles)):
        findings.append(Finding("content.log", rel, "each date appears once; add entries under the existing heading"))
    for section in dates:
        if not markdown.items(section.text):
            findings.append(Finding("content.log", rel, f"{section.heading.title} needs at least one bullet entry"))


def _fence(rel: str, body: str, findings: list[Finding]) -> None:
    opener = markdown.unclosed_fence(body)
    if opener is not None:
        findings.append(Finding("content.fence", rel, f"the code fence opened by '{opener}' is never closed; add the closing fence"))


def check(bundle: Bundle) -> list[Finding]:
    schema = bundle.schema
    findings: list[Finding] = []
    for concept in bundle.concepts:
        _fence(concept.rel, concept.body, findings)
        for path, spec in _walk(schema.headings(concept.type), []):
            section = concept.section(path)
            if section is None:
                continue
            if "requirements" in spec:
                _requirements(concept, spec, section, findings)
            if spec.get("allow_none") and markdown.is_none(section.text):
                continue
            if "table" in spec:
                _table(concept, spec, section, findings)
            if "mermaid" in spec:
                _mermaid(concept, spec, section, findings)
        if concept.type == "MessageChannel" and concept.folder is not None:
            _payload(concept, findings)
        if concept.folder is not None and schema.types[concept.type].get("log", True):
            _log(bundle, concept, findings)
    return findings
