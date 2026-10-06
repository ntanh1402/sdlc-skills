"""Load schema.json and answer questions about it."""

from __future__ import annotations

import json
from pathlib import Path

SCHEMA_DIR = Path(__file__).resolve().parents[2] / "schema"
DEFAULT_PATH = SCHEMA_DIR / "schema.json"


class Schema:
    def __init__(self, data: dict):
        self.data = data
        self.version: str = data["schema_version"]
        self.okf_version: str = data["okf_version"]
        self.types: dict[str, dict] = data["types"]
        self.design_types: list[str] = data["design_types"]
        self.qualifiers: dict[str, list[str]] = data["qualifiers"]
        self.pending: dict = data["pending"]
        self.references: dict = data["references"]
        self.collections: list[dict] = data["collections"]

    @classmethod
    def load(cls, path: Path | None = None) -> "Schema":
        return cls(json.loads((path or DEFAULT_PATH).read_text(encoding="utf-8")))

    # --- structure -------------------------------------------------------

    def collection(self, directory: str) -> dict | None:
        for entry in self.collections:
            if entry["dir"] == directory:
                return entry
        return None

    def type_for_key(self, candidates: list[str], key: str) -> str | None:
        """Pick the candidate type whose prefix or fixed filename matches `key`."""
        for name in candidates:
            spec = self.types[name]
            if spec.get("filename"):
                if spec["filename"] == f"{key}.md":
                    return name
            elif spec.get("prefix") and key.startswith(spec["prefix"]):
                return name
        for name in candidates:
            spec = self.types[name]
            if not spec.get("prefix") and not spec.get("filename"):
                return name
        return None

    def owned_types(self, owner: str) -> list[str]:
        return list(self.types[owner].get("owns", []))

    def key_pattern(self, name: str) -> str | None:
        spec = self.types[name]
        if spec.get("key_pattern"):
            return spec["key_pattern"]
        if spec.get("prefix"):
            return "^" + spec["prefix"] + "[a-z0-9]+(-[a-z0-9]+)*$"
        return None

    def is_design(self, name: str) -> bool:
        return name in self.design_types

    # --- fields ----------------------------------------------------------

    def fields(self, name: str) -> dict[str, dict]:
        """Common fields overlaid with the type's own; `status` added for lifecycle types."""
        spec = self.types[name]
        merged = {key: dict(value) for key, value in self.data["common_fields"].items()}
        if spec.get("lifecycle"):
            merged["status"] = {"kind": "enum", "values": spec["statuses"], "required": True}
        for key, value in spec.get("fields", {}).items():
            merged[key] = dict(value)
        return merged

    # --- headings --------------------------------------------------------

    def headings(self, name: str) -> list[dict]:
        """Top-level headings in order: the type's own, with `# References` before
        the first tool-written one, and Pending changes appended for Design types."""
        result = [dict(entry) for entry in self.types[name].get("headings", [])]
        position = next((index for index, entry in enumerate(result) if "generated" in entry), len(result))
        result.insert(position, dict(self.references))
        if self.is_design(name):
            result.append(
                {
                    "name": self.pending["heading"],
                    "presence": "conditional",
                    "links": {
                        "targets": list(self.pending["open_parents"]),
                        "min": 1,
                        "qualifier": {"set": "change", "required": True},
                    },
                }
            )
        return result

    def heading(self, name: str, path: list[str]) -> dict | None:
        """Find a heading spec by its path, e.g. ['Delta', 'Target delta']."""
        level = self.headings(name)
        found = None
        for title in path:
            found = next((entry for entry in level if entry["name"] == title), None)
            if found is None:
                return None
            level = found.get("nested", [])
        return found

    def link_headings(self, name: str) -> list[tuple[list[str], dict]]:
        """Every (heading path, links spec) of a type, nested ones included."""
        found: list[tuple[list[str], dict]] = []

        def walk(entries: list[dict], prefix: list[str]) -> None:
            for entry in entries:
                path = prefix + [entry["name"]]
                if "links" in entry:
                    found.append((path, entry["links"]))
                walk(entry.get("nested", []), path)

        walk(self.headings(name), [])
        return found

    def targets(self, links: dict) -> list[str]:
        """Expand the `@design` token in a links spec."""
        expanded: list[str] = []
        for target in links["targets"]:
            expanded.extend(self.design_types if target == "@design" else [target])
        return expanded
