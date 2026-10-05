"""Parse the YAML subset allowed in wiki frontmatter.

Accepted forms (every one is valid YAML):

    key: scalar
    key: "quoted scalar"
    key: [a, b]
    key: { k: v, k: v }
    key:
      - { k: v, k: v }
      - k: v
        k: v

Anything else is reported as an error string; parsing never raises.
"""

from __future__ import annotations

import re

KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):(?:\s+(.*))?$")
ITEM_RE = re.compile(r"^(\s+)-\s+(.*)$")
FORBIDDEN_START = set("[]{}&*!|>'\"%@`#,?")


def split(text: str) -> tuple[list[str] | None, str]:
    """Return (frontmatter lines, body). Lines are None when there is no block.

    A leading byte order mark, which some editors write, is not part of either.
    """
    text = text.removeprefix("\ufeff")
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], "\n".join(lines[index + 1 :])
    return None, text


def _scalar(raw: str, errors: list[str], where: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        value = raw[1:-1]
        if value[:1] in ("{", "["):
            errors.append(f"{where}: structured data belongs in the body")
        return value
    if not raw:
        errors.append(f"{where}: empty value")
        return ""
    if raw[0] in FORBIDDEN_START or raw.startswith("- "):
        errors.append(f"{where}: value must be quoted: {raw}")
    elif ": " in raw or " #" in raw or raw.endswith(":"):
        errors.append(f"{where}: value must be quoted: {raw}")
    return raw


def _flow_list(raw: str, errors: list[str], where: str) -> list[str]:
    inner = raw.strip()[1:-1].strip()
    if not inner:
        return []
    return [_scalar(part, errors, where) for part in inner.split(",")]


def _flow_map(raw: str, errors: list[str], where: str) -> dict[str, str]:
    inner = raw.strip()[1:-1].strip()
    result: dict[str, str] = {}
    if not inner:
        errors.append(f"{where}: empty mapping")
        return result
    for part in inner.split(", "):
        match = KEY_RE.match(part.strip())
        if not match or match.group(2) is None:
            errors.append(f"{where}: bad mapping entry: {part.strip()}")
            continue
        result[match.group(1)] = _scalar(match.group(2), errors, where)
    return result


def _is_flow_map(raw: str) -> bool:
    raw = raw.strip()
    return raw.startswith("{") and raw.endswith("}")


def _is_flow_list(raw: str) -> bool:
    raw = raw.strip()
    return raw.startswith("[") and raw.endswith("]")


def _block_list(lines: list[str], start: int, errors: list[str], key: str) -> tuple[list[dict[str, str]], int]:
    """Parse an indented list of mappings beginning at lines[start]."""
    items: list[dict[str, str]] = []
    index = start
    current: dict[str, str] | None = None
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if not line.startswith(" "):
            break
        item = ITEM_RE.match(line)
        if item:
            content = item.group(2)
            if _is_flow_map(content):
                items.append(_flow_map(content, errors, key))
                current = None
            else:
                match = KEY_RE.match(content)
                if not match or match.group(2) is None:
                    errors.append(f"{key}: list items must be mappings: {content}")
                    current = None
                else:
                    current = {match.group(1): _scalar(match.group(2), errors, key)}
                    items.append(current)
        else:
            match = KEY_RE.match(line.strip())
            if current is None or not match or match.group(2) is None:
                errors.append(f"{key}: unexpected line: {line.strip()}")
            else:
                current[match.group(1)] = _scalar(match.group(2), errors, key)
        index += 1
    return items, index


def parse(text: str) -> tuple[dict[str, object], str, list[str]]:
    """Return (metadata, body, errors) for one Markdown document."""
    lines, body = split(text)
    errors: list[str] = []
    if lines is None:
        return {}, body, ["missing or unterminated frontmatter block"]
    meta: dict[str, object] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip():
            continue
        match = KEY_RE.match(line)
        if not match:
            errors.append(f"unsupported frontmatter line: {line.strip()}")
            continue
        key, raw = match.group(1), match.group(2)
        if key in meta:
            errors.append(f"{key}: duplicate key")
        if raw is None or not raw.strip():
            items, index = _block_list(lines, index, errors, key)
            if not items:
                errors.append(f"{key}: empty value")
            meta[key] = items
        elif _is_flow_map(raw):
            meta[key] = _flow_map(raw, errors, key)
        elif _is_flow_list(raw):
            meta[key] = _flow_list(raw, errors, key)
        else:
            meta[key] = _scalar(raw, errors, key)
    return meta, body, errors


def set_field(text: str, key: str, value: str | None) -> str:
    """Return `text` with the top-level frontmatter `key` set to `value`, written
    as `key: value` (a value that starts with a newline continues as a block),
    or removed when `value` is None. A missing key is added at the end of the
    block. A text without a frontmatter block is returned unchanged."""
    bom = "﻿" if text.startswith("﻿") else ""
    lines = text.removeprefix("﻿").split("\n")
    if not lines or lines[0].strip() != "---":
        return text
    end = next((index for index in range(1, len(lines)) if lines[index].strip() == "---"), None)
    if end is None:
        return text
    start = next((index for index in range(1, end) if (KEY_RE.match(lines[index]) or [None, None])[1] == key), None)
    new = [] if value is None else f"{key}:{'' if value.startswith(chr(10)) else ' '}{value}".split("\n")
    if start is None:
        lines[end:end] = new
    else:
        stop = start + 1
        while stop < end and (lines[stop].startswith((" ", "\t")) or not lines[stop].strip()):
            stop += 1
        lines[start:stop] = new
    return bom + "\n".join(lines)
