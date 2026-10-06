"""Read a bundle from disk into concepts, using schema.json for the layout."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import frontmatter, markdown
from .schema import Schema

RESERVED = {"index.md", "overview.md", "log.md"}
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


@dataclass(frozen=True)
class Finding:
    rule: str
    path: str
    message: str
    severity: str = "error"


@dataclass
class Concept:
    path: Path  # the concept document: overview.md for a folder concept
    rel: str  # POSIX path relative to the bundle root
    type: str  # type implied by location and key
    key: str  # folder name, or filename without .md
    app: str
    meta: dict
    body: str
    fm_errors: list[str]
    folder: Path | None = None  # set for folder concepts
    owner: "Concept | None" = None

    @property
    def title(self) -> str:
        value = self.meta.get("title")
        return value if isinstance(value, str) and value else self.key

    @property
    def description(self) -> str:
        value = self.meta.get("description")
        return value if isinstance(value, str) else ""

    @property
    def status(self) -> str:
        value = self.meta.get("status")
        return value if isinstance(value, str) else ""

    def section(self, path: list[str]) -> markdown.Section | None:
        """Section at a heading path: level 1, then level 2 inside it, and so on."""
        found: markdown.Section | None = None
        for depth, title in enumerate(path, start=1):
            found = markdown.section(self.body, title, level=depth, within=found)
            if found is None:
                return None
        return found


@dataclass(frozen=True)
class Relation:
    item: markdown.Item
    path: Path | None  # resolved target file; None for an external URL or no link
    anchor: str
    concept: Concept | None
    kind: str  # target type name, "Requirement", or "" when unknown
    qualifier: str | None


@dataclass
class Bundle:
    root: Path
    schema: Schema
    index_meta: dict = field(default_factory=dict)
    concepts: list[Concept] = field(default_factory=list)
    problems: list[Finding] = field(default_factory=list)
    directories: list[Path] = field(default_factory=list)  # every directory that needs an index.md
    by_path: dict[Path, Concept] = field(default_factory=dict)
    unreadable: set[Path] = field(default_factory=set)  # files that are not UTF-8; sync never writes them
    _texts: dict[Path, str] = field(default_factory=dict, repr=False)

    # --- lookups ---------------------------------------------------------

    def rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def of_type(self, *names: str) -> list[Concept]:
        return [concept for concept in self.concepts if concept.type in names]

    def owned(self, owner: Concept, *names: str) -> list[Concept]:
        return [c for c in self.concepts if c.owner is owner and (not names or c.type in names)]

    def content_holder(self, path: Path) -> Concept | None:
        """The concept whose folder holds `path` as a content file: any file below
        a Reference folder except its own overview.md, log.md and index.md."""
        for concept in self.concepts:
            folder = concept.folder
            if folder is None or not self.schema.types[concept.type].get("content_files"):
                continue
            if folder in path.parents and not (path.parent == folder and path.name in RESERVED):
                return concept
        return None

    def text(self, path: Path) -> str:
        """Text of a bundle file, decoded once. A file that is not UTF-8 becomes a
        layout.encoding problem and is marked unreadable; its bad bytes are
        replaced in the returned text so the other checks can go on."""
        if path not in self._texts:
            try:
                self._texts[path] = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                self.unreadable.add(path)
                self._problem("layout.encoding", path, "the file is not valid UTF-8; save it as UTF-8 (sync leaves it alone until then)")
                self._texts[path] = path.read_text(encoding="utf-8", errors="replace")
        return self._texts[path]

    def markdown_files(self) -> list[Path]:
        """Every Markdown file of the bundle, outside dot directories."""
        return sorted(
            path
            for path in self.root.rglob("*.md")
            if path.is_file()
            and not any(part.startswith(".") for part in path.relative_to(self.root).parts)
        )

    def resolve(self, source: Path, target: str) -> tuple[Path | None, str]:
        """Resolve a link target to (file path, anchor). External URLs give (None, '')."""
        if SCHEME_RE.match(target):
            return None, ""
        raw, _, anchor = target.partition("#")
        if not raw:
            return source, anchor
        base = self.root / raw.lstrip("/") if raw.startswith("/") else source.parent / raw
        return Path(os.path.normpath(base)), anchor

    def relations(self, concept: Concept, path: list[str]) -> list[Relation]:
        """Relationship entries under a heading: the first link of each list item."""
        spec = self.schema.heading(concept.type, path)
        section = concept.section(path)
        if spec is None or section is None:
            return []
        allowed = self.schema.qualifiers.get(spec.get("links", {}).get("qualifier", {}).get("set", ""), [])
        result: list[Relation] = []
        for item in markdown.items(section.text):
            target_path, anchor = self.resolve(concept.path, item.target) if item.target else (None, "")
            target = self.by_path.get(target_path) if target_path else None
            kind = target.type if target else ""
            if target and anchor.lower().startswith("req-") and target.type in ("Feature", "ChangeRequest"):
                kind = "Requirement"
            qualifier = item.segments[0] if item.segments and item.segments[0] in allowed else None
            result.append(Relation(item, target_path, anchor, target, kind, qualifier))
        return result

    # --- loading ---------------------------------------------------------

    @classmethod
    def load(cls, root: Path, schema: Schema) -> "Bundle":
        bundle = cls(root=Path(os.path.normpath(root)), schema=schema)
        bundle._walk()
        return bundle

    def _problem(self, rule: str, path: Path, message: str) -> None:
        self.problems.append(Finding(rule, self.rel(path), message))

    def _read(self, path: Path, type_name: str, key: str, app: str, folder: Path | None, owner: Concept | None) -> Concept:
        meta, body, errors = frontmatter.parse(self.text(path))
        concept = Concept(path, self.rel(path), type_name, key, app, meta, body, errors, folder, owner)
        self.concepts.append(concept)
        self.by_path[path] = concept
        return concept

    @staticmethod
    def _entries(directory: Path) -> list[Path]:
        return sorted(entry for entry in directory.iterdir() if not entry.name.startswith("."))

    def _walk(self) -> None:
        self.directories.append(self.root)
        index = self.root / "index.md"
        if index.is_file():
            self.index_meta, _, _ = frontmatter.parse(self.text(index))
        for entry in self._entries(self.root):
            if entry.is_dir():
                self._walk_app(entry)
            elif entry.name != "index.md":
                self._problem("layout.unknown-path", entry, "only index.md and application folders belong in the bundle root")

    def _walk_app(self, app_dir: Path) -> None:
        self.directories.append(app_dir)
        app = app_dir.name
        overview = app_dir / "overview.md"
        application = self._read(overview, "Application", app, app, app_dir, None) if overview.is_file() else None
        if application is None:
            self._problem("layout.missing-file", overview, "an application folder needs overview.md")
        owned = self.schema.owned_types("Application")
        other: list[Path] = []
        for entry in self._entries(app_dir):
            if entry.is_dir():
                collection = self.schema.collection(entry.name)
                if collection is None:
                    self._problem("layout.unknown-path", entry, "not a declared collection directory")
                else:
                    self._walk_collection(entry, collection, app)
            elif entry.name in ("index.md", "overview.md"):
                continue
            elif entry.suffix != ".md":
                other.append(entry)
            elif entry.name != "log.md" and self.schema.type_for_key(owned, entry.stem):
                self._read(entry, self.schema.type_for_key(owned, entry.stem), entry.stem, app, None, application)
            else:
                self._problem("layout.unknown-path", entry, "not a file an application folder may contain")
        self._check_other_files(app_dir, other)

    def _walk_collection(self, directory: Path, collection: dict, app: str) -> None:
        self.directories.append(directory)
        for entry in self._entries(directory):
            if entry.name == "index.md":
                continue
            key = entry.stem if entry.is_file() else entry.name
            type_name = self.schema.type_for_key(collection["types"], key)
            shape = self.schema.types[type_name]["shape"] if type_name else None
            if shape == "file" and entry.is_file() and entry.suffix == ".md":
                self._read(entry, type_name, key, app, None, None)
            elif shape == "folder" and entry.is_dir():
                self._walk_concept(entry, type_name, app)
            else:
                self._problem("layout.unknown-path", entry, f"not a concept of collection {collection['dir']}/")

    def _walk_concept(self, folder: Path, type_name: str, app: str) -> None:
        self.directories.append(folder)
        spec = self.schema.types[type_name]
        overview = folder / "overview.md"
        if not overview.is_file():
            self._problem("layout.missing-file", overview, f"{type_name} folder needs overview.md")
            return
        concept = self._read(overview, type_name, folder.name, app, folder, None)
        if spec.get("log", True) and not (folder / "log.md").is_file():
            self._problem("layout.missing-file", folder / "log.md", f"{type_name} folder needs log.md")
        if spec.get("content_files"):
            return  # any other file or folder is content of the concept; nothing below needs an index
        extra = {entry["name"] for entry in spec.get("extra_files", [])}
        for name in sorted(extra):
            if not (folder / name).is_file():
                self._problem("layout.missing-file", folder / name, f"{type_name} folder needs {name}")
        owned_types = self.schema.owned_types(type_name)
        other: list[Path] = []
        for entry in self._entries(folder):
            if entry.is_dir():
                self._problem("layout.unknown-path", entry, "a concept folder holds files only")
            elif entry.name in RESERVED:
                continue
            elif entry.suffix == ".md":
                owned_type = self.schema.type_for_key(owned_types, entry.stem)
                if owned_type is None:
                    self._problem("layout.unknown-path", entry, f"a {type_name} folder cannot own this file")
                else:
                    self._read(entry, owned_type, entry.stem, app, None, concept)
            elif entry.name not in extra:
                other.append(entry)
        self._check_other_files(folder, other)

    def _check_other_files(self, folder: Path, other: list[Path]) -> None:
        """A file that is not Markdown may sit in a folder only when the schema
        declares it; a document's images and originals belong in a Reference."""
        for entry in other:
            self._problem("layout.non-markdown", entry, "non-Markdown file is not declared here; put a document's files in a Reference folder")
