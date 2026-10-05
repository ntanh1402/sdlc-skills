"""Generated content: indexes and generated sections equal what sync writes."""

from __future__ import annotations

from .. import sync
from ..bundle import Bundle, Finding

ORDER = 90


def check(bundle: Bundle) -> list[Finding]:
    rendered, unstable, _ = sync.plan(bundle)
    findings = [
        Finding("generated.stale", bundle.rel(path), "generated content is out of date; run: wiki_llm.py sync")
        for path in sync.stale(bundle, rendered)
    ]
    findings.extend(
        Finding(
            "generated.unstable",
            bundle.rel(path),
            "sync cannot settle the tool-written sections of this file, so it leaves the file alone; keep each tool-written heading once",
        )
        for path in unstable
    )
    return findings
