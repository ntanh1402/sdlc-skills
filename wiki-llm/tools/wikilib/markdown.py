"""Small Markdown helpers: headings, sections, links, list items, tables.

All helpers ignore fenced code blocks, so a `# comment` inside a fence is not
a heading and a link inside a fence is not a link.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

HEADING_RE = re.compile(r"^(#{1,6}) +(.+?)\s*$")
# A fence opens or closes with at most three spaces of indent; four make an indented code line.
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
LINK_RE = re.compile(r"(?<!\!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
ANY_LINK_RE = re.compile(r"!?\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
ITEM_RE = re.compile(r"^[*-] +")
SEPARATOR = " — "
FULL_LINK = r"\[[^\]]*\]\([^)\s]+\)"
LOOSE_ITEM_RE = re.compile(r"^\s*(?:\d+[.)]|\+)\s+" + FULL_LINK + r"|^\s+[*-]\s+" + FULL_LINK)
LINK_LINE_RE = re.compile(r"^\s*" + FULL_LINK + SEPARATOR)


@dataclass(frozen=True)
class Heading:
    level: int
    title: str
    line: int


@dataclass(frozen=True)
class Section:
    heading: Heading
    start: int  # first line after the heading
    end: int  # one past the last line of the section
    text: str


@dataclass(frozen=True)
class Item:
    text: str  # the whole list item, continuation lines joined by spaces
    label: str  # text of the first link, "" when there is none
    target: str  # destination of the first link, "" when there is none
    segments: tuple[str, ...]  # parts after the link, split on " — "


def _scan(lines: list[str]) -> tuple[list[bool], str | None]:
    """Per line, whether it belongs to a fenced block; and the opening line of a
    fence still open at the end, or None.

    A fence closes only on a line of the opener's character, at least as long,
    with nothing after it. Any other fence-like line inside a fence is content.
    """
    flags: list[bool] = []
    marker = ""  # the run of ` or ~ that opened the current fence
    opener: str | None = None
    for line in lines:
        match = FENCE_RE.match(line)
        if not marker:
            # a backtick fence cannot carry a backtick after its marker
            if match and not (match.group(1)[0] == "`" and "`" in match.group(2)):
                marker, opener = match.group(1), line.strip()
                flags.append(True)
            else:
                flags.append(False)
            continue
        flags.append(True)
        if match and match.group(1)[0] == marker[0] and len(match.group(1)) >= len(marker) and not match.group(2).strip():
            marker, opener = "", None
    return flags, opener


def _fenced(lines: list[str]) -> list[bool]:
    return _scan(lines)[0]


def unclosed_fence(body: str) -> str | None:
    """The opening line of a code fence that is never closed, or None."""
    return _scan(body.split("\n"))[1]


def headings(body: str) -> list[Heading]:
    lines = body.split("\n")
    fenced = _fenced(lines)
    found: list[Heading] = []
    for number, line in enumerate(lines):
        if fenced[number]:
            continue
        match = HEADING_RE.match(line)
        if match:
            found.append(Heading(len(match.group(1)), match.group(2), number))
    return found


def sections(body: str, level: int, within: Section | None = None) -> list[Section]:
    """Sections opened by headings of `level`, optionally inside a parent section."""
    lines = body.split("\n")
    low = within.start if within else 0
    high = within.end if within else len(lines)
    inside = [item for item in headings(body) if low <= item.line < high]
    result: list[Section] = []
    for position, heading in enumerate(inside):
        if heading.level != level:
            continue
        end = high
        for later in inside[position + 1 :]:
            if later.level <= level:
                end = later.line
                break
        result.append(Section(heading, heading.line + 1, end, "\n".join(lines[heading.line + 1 : end])))
    return result


def section(body: str, title: str, level: int = 1, within: Section | None = None) -> Section | None:
    for candidate in sections(body, level, within):
        if candidate.heading.title == title:
            return candidate
    return None


def strip_fences(text: str) -> str:
    lines = text.split("\n")
    fenced = _fenced(lines)
    return "\n".join("" if fenced[number] else line for number, line in enumerate(lines))


def mask_inline_code(text: str) -> str:
    """Replace inline code spans with x, keeping every offset."""
    return INLINE_CODE_RE.sub(lambda match: "x" * len(match.group(0)), text)


def mask_code(text: str) -> str:
    """Blank out fenced lines and inline code, keeping every offset, so a
    pattern match on the result can be applied to `text`."""
    lines = text.split("\n")
    fenced = _fenced(lines)
    kept = "\n".join(" " * len(line) if fenced[number] else line for number, line in enumerate(lines))
    return mask_inline_code(kept)


def link_spans(text: str) -> list[re.Match]:
    """Matches of every link and image outside code, with offsets into `text`.
    Group 1 is the label and group 2 the target."""
    return list(ANY_LINK_RE.finditer(mask_code(text)))


def links(text: str, images: bool = False) -> list[tuple[str, str]]:
    """Every (label, target) link outside code fences and inline code; images only on request."""
    pattern = ANY_LINK_RE if images else LINK_RE
    stripped = strip_fences(text)
    masked = mask_inline_code(stripped)
    return [(stripped[m.start(1):m.end(1)], stripped[m.start(2):m.end(2)]) for m in pattern.finditer(masked)]


def items(text: str) -> list[Item]:
    """Top-level list items. A blank line or a new item ends the current one."""
    result: list[Item] = []
    current: list[str] | None = None

    def flush() -> None:
        if current is None:
            return
        joined = " ".join(part.strip() for part in current)
        match = LINK_RE.search(joined)
        if not match:
            result.append(Item(joined, "", "", ()))
            return
        parts = joined[match.end() :].split(SEPARATOR)
        result.append(Item(joined, match.group(1), match.group(2), tuple(part.strip() for part in parts[1:])))

    for line in strip_fences(text).split("\n"):
        if ITEM_RE.match(line):
            flush()
            current = [ITEM_RE.sub("", line, count=1)]
        elif not line.strip():
            flush()
            current = None
        elif current is not None:
            current.append(line)
    flush()
    return result


def loose_items(text: str) -> list[str]:
    """Lines that read like a relationship but are not top-level list items:
    a numbered, `+` or indented bullet that starts with a link, and a paragraph
    that starts with a link followed by " — "."""
    found: list[str] = []
    opens_paragraph = True  # the previous line is blank, or there is none
    for line in strip_fences(text).split("\n"):
        if LOOSE_ITEM_RE.match(line) or (opens_paragraph and LINK_LINE_RE.match(line)):
            found.append(line.strip())
        opens_paragraph = not line.strip()
    return found


def slug(title: str) -> str:
    """GitHub-style heading anchor."""
    return re.sub(r"[^\w\- ]", "", title.strip().lower()).replace(" ", "-")


def anchors(body: str) -> set[str]:
    return {slug(heading.title) for heading in headings(body)}


def table(text: str) -> tuple[list[str], list[list[str]]]:
    """Header cells and rows of the first pipe table in `text`."""
    rows: list[list[str]] = []
    for line in strip_fences(text).split("\n"):
        stripped = line.strip()
        if not stripped.startswith("|"):
            if rows:
                break
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if all(cell and set(cell) <= set("-: ") for cell in cells):
            continue
        rows.append(cells)
    if not rows:
        return [], []
    return rows[0], rows[1:]


def mermaid_kinds(text: str) -> list[str]:
    """First word of every ```mermaid block, e.g. 'flowchart' or 'sequenceDiagram'."""
    kinds: list[str] = []
    for match in re.finditer(r"```mermaid\s*\n(.*?)```", text, re.DOTALL):
        words = match.group(1).split()
        kinds.append(words[0] if words else "")
    return kinds


def is_none(text: str) -> bool:
    """True when a section's content is the literal `None` marker."""
    return text.strip().startswith("None")
