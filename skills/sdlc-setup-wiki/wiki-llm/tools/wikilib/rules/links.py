"""Links: every internal link, anchor and relative resource resolves inside the bundle."""

from __future__ import annotations

from pathlib import Path

from .. import frontmatter, markdown
from ..bundle import SCHEME_RE, Bundle, Finding

ORDER = 50


def _inside(bundle: Bundle, path: Path) -> bool:
    return path == bundle.root or bundle.root in path.parents


def check(bundle: Bundle) -> list[Finding]:
    findings: list[Finding] = []
    anchor_cache: dict[Path, set[str]] = {}

    def anchors(path: Path) -> set[str]:
        if path not in anchor_cache:
            _, body = frontmatter.split(bundle.text(path))
            anchor_cache[path] = markdown.anchors(body)
        return anchor_cache[path]

    def check_target(source: Path, target: str, rule: str) -> None:
        rel = bundle.rel(source)
        path, anchor = bundle.resolve(source, target)
        if path is None:
            return
        if not _inside(bundle, path):
            findings.append(Finding("links.outside-bundle", rel, f"{target} leaves the bundle"))
        elif path.is_dir():
            findings.append(Finding("links.folder-link", rel, f"{target} is a folder; link its overview.md or index.md"))
        elif not path.is_file():
            findings.append(Finding(rule, rel, f"{target} does not exist"))
        elif anchor and path.suffix == ".md" and anchor.lower() not in anchors(path):
            findings.append(Finding("links.anchor", rel, f"{target}: no heading produces the anchor #{anchor}"))

    for path in bundle.markdown_files():
        _, body = frontmatter.split(bundle.text(path))
        for _, target in markdown.links(body, images=True):
            check_target(path, target, "links.unresolved")

    for concept in bundle.concepts:
        resources = [concept.meta.get("resource")]
        sources = concept.meta.get("sources")
        if isinstance(sources, list):
            resources.extend(entry.get("resource") for entry in sources if isinstance(entry, dict))
        for resource in resources:
            if isinstance(resource, str) and resource and not SCHEME_RE.match(resource):
                check_target(concept.path, resource, "links.resource")
    return findings
