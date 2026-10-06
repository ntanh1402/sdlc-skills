"""Write the generated tables of the schema pages from schema.json.

Each page keeps its hand-written prose. The tool owns only the text between
the two marker comments.
"""

from __future__ import annotations

from pathlib import Path

from . import markdown
from .bundle import SCHEME_RE
from .schema import SCHEMA_DIR, Schema

START = "<!-- generated:schema start -->"
END = "<!-- generated:schema end -->"
CATALOG_PAGE = "schema.md"
UNCHECKED_PAGES = {"okf-spec.md"}  # an external specification with illustrative links

KIND_TEXT = {
    "string": "text",
    "boolean": "`true` or `false`",
    "integer": "whole number",
    "uri": "URL or bundle path",
    "timestamp": "ISO 8601 timestamp with offset",
    "date": "`YYYY-MM-DD`",
    "actor_stamp": "`{ by, at }`",
    "actor_stamps": "`{ by, at }`, or a list of them",
    "sources": "list of `{ id, resource, title }`",
    "string_list": "`[a, b]`",
}
LEADING = ["type", "title", "description", "status"]
TRAILING = ["generated", "verified", "sources", "resource", "stale_after", "tags"]


def _codes(values: list[str]) -> str:
    return ", ".join(f"`{value}`" for value in values)


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return lines


def _field_rows(schema: Schema, name: str) -> list[list[str]]:
    fields = schema.fields(name)
    own = [key for key in fields if key not in LEADING and key not in TRAILING]
    order = [key for key in LEADING if key in fields] + own + [key for key in TRAILING if key in fields]
    rows = []
    for key in order:
        spec = fields[key]
        if key == "type":
            values = f"`{name}`"
        elif spec["kind"] == "enum":
            values = _codes(spec["values"])
        elif spec["kind"] == "suggested":
            values = f"lower-case words joined by `-`; common: {_codes(spec['values'])}"
        else:
            values = KIND_TEXT[spec["kind"]]
        required = "yes" if spec.get("required") else "no"
        if key == "verified" and schema.types[name].get("human_verified"):
            required = "yes, by a `human:` actor"
        rows.append([f"`{key}`", required, values])
    return rows


def _targets(schema: Schema, links: dict) -> str:
    names = ["any Design type" if target == "@design" else target for target in links["targets"]]
    low, high = links.get("min", 0), links.get("max")
    if high is not None and low == high:
        count = f"exactly {low}"
    elif high is not None:
        count = f"{low} to {high}"
    elif low:
        count = f"{low} or more"
    else:
        count = "any number"
    return f"{', '.join(names)} ({count})"


def _content(spec: dict) -> str:
    """What the section must hold besides links; link counts are in the `Links to` cell."""
    parts = []
    if "table" in spec:
        parts.append(f"table with columns {_codes(spec['table'])}")
    if "mermaid" in spec:
        parts.append(f"Mermaid `{spec['mermaid']}` diagram")
    if "requirements" in spec:
        low = spec["requirements"]["min"]
        parts.append(f"{f'{low} or more' if low else 'any number of'} `### REQ-*` entries")
    if "none_statuses" in spec:
        parts.append(f"`None` only while status is {' or '.join(f'`{status}`' for status in spec['none_statuses'])}")
    return "; ".join(parts)


def _heading_rows(schema: Schema, specs: list[dict], depth: int) -> list[list[str]]:
    rows = []
    for spec in specs:
        marker = "#" * depth
        generated = spec.get("generated")
        if generated:
            sources = ", ".join(
                f"{'any type' if source['type'] == '@any' else source['type']} `{'#' * len(source['heading'])} {source['heading'][-1]}`"
                for source in generated["sources"]
            )
            presence = "when not empty" if generated.get("when_empty") == "omit" else "always"
            rows.append([f"`{marker} {spec['name']}`", presence, "tool", f"mirrors {sources}", "", ""])
        else:
            links = spec.get("links")
            qualifier = ""
            if links and "qualifier" in links:
                need = "required" if links["qualifier"]["required"] else "optional"
                qualifier = f"{_codes(schema.qualifiers[links['qualifier']['set']])} ({need})"
            presence = spec["presence"]
            if spec.get("allow_none"):
                presence += "; may be `None`"
            targets = _targets(schema, links) if links else ""
            rows.append([f"`{marker} {spec['name']}`", presence, "author", targets, qualifier, _content(spec)])
        rows.extend(_heading_rows(schema, spec.get("nested", []), depth + 1))
    return rows


def type_block(schema: Schema, name: str) -> str:
    spec = schema.types[name]
    if spec["shape"] == "folder":
        files = ["index.md", "overview.md"] + (["log.md"] if spec.get("log", True) else [])
        files += [entry["name"] for entry in spec.get("extra_files", [])]
        shape = f"Folder with {_codes(files)}"
        if spec.get("content_files"):
            shape += ", and any content files and folders"
    else:
        shape = "One file"
    facts = [
        ["Type", f"`{name}`"],
        ["Phase", spec["phase"]],
        ["Path", f"`{spec['path']}`"],
        ["Shape", shape],
        ["Status", _codes(spec["statuses"]) if spec.get("lifecycle") else "None; this type has no `status` field"],
    ]
    if spec.get("owns"):
        facts.append(["Owns", ", ".join(spec["owns"])])
    lines = _table(["", ""], facts)
    lines += ["", "### Fields", ""] + _table(["Field", "Required", "Values"], _field_rows(schema, name))
    lines += ["", "### Headings", ""]
    title = spec.get("title", "title")
    rows = []
    if title != "free":
        first = title.split(":", 1)[1] if title.startswith("fixed:") else "<title>"
        rows.append([f"`# {first}`", "required; first heading", "author", "", "", ""])
        rows.extend(_heading_rows(schema, spec.get("title_nested", []), 2))
    rows.extend(_heading_rows(schema, schema.headings(name), 1))
    lines += _table(["Heading", "Presence", "Written by", "Links to", "Qualifier", "Content"], rows)
    if spec.get("free_headings"):
        lines += ["", "Any other headings are allowed."]
    return "\n".join(lines)


def catalog_block(schema: Schema) -> str:
    rows = [
        [spec["phase"], name, f"[{spec['page'][:-3]}]({spec['page']})", f"`{spec['path']}`"]
        for name, spec in schema.types.items()
    ]
    lines = _table(["Phase", "Type", "Schema page", "Path"], rows)
    lines += ["", f"**Design types:** {', '.join(schema.design_types)}.", ""]
    lines += _table(["Qualifier set", "Values"], [[name, _codes(values)] for name, values in schema.qualifiers.items()])
    return "\n".join(lines)


def replace_block(text: str, block: str) -> str | None:
    """Put `block` between the markers. None when the markers are missing."""
    start, end = text.find(START), text.find(END)
    if start < 0 or end < start:
        return None
    return text[: start + len(START)] + "\n" + block + "\n" + text[end:]


def render(schema: Schema, directory: Path = SCHEMA_DIR) -> dict[Path, str | None]:
    """Expected text of every schema page; None marks a page without markers or a missing page."""
    blocks = {directory / spec["page"]: type_block(schema, name) for name, spec in schema.types.items()}
    blocks[directory / CATALOG_PAGE] = catalog_block(schema)
    result: dict[Path, str | None] = {}
    for path, block in blocks.items():
        result[path] = replace_block(path.read_text(encoding="utf-8"), block) if path.is_file() else None
    return result


def stale(schema: Schema, directory: Path = SCHEMA_DIR) -> list[Path]:
    return sorted(
        path
        for path, text in render(schema, directory).items()
        if text is None or path.read_text(encoding="utf-8") != text
    )


def write(schema: Schema, directory: Path = SCHEMA_DIR) -> list[Path]:
    """Update every page that has markers. Returns the paths that changed."""
    changed = []
    for path, text in render(schema, directory).items():
        if text is not None and path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
            changed.append(path)
    return sorted(changed)


def broken_links(directory: Path = SCHEMA_DIR) -> list[tuple[Path, str]]:
    """Relative links in schema pages that do not lead to a file."""
    broken = []
    for path in sorted(directory.glob("*.md")):
        if path.name in UNCHECKED_PAGES:
            continue
        for _, target in markdown.links(path.read_text(encoding="utf-8")):
            raw = target.partition("#")[0]
            if not raw or SCHEME_RE.match(target):
                continue
            if not (path.parent / raw).is_file():
                broken.append((path, target))
    return broken
