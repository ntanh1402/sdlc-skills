"""Base class for rule tests: a fresh fixture bundle per test."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from wikilib import validate
from wikilib.bundle import Finding

from . import fixture


class RuleTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = fixture.make_bundle(Path(self._tmp.name) / "bundle")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def edit(self, rel: str, old: str, new: str) -> None:
        fixture.edit(self.root, rel, old, new)

    def write(self, rel: str, text: str) -> None:
        fixture.write(self.root, rel, text)

    def remove(self, rel: str) -> None:
        fixture.remove(self.root, rel)

    def findings(self, include_generated: bool = False) -> list[Finding]:
        """Findings for the bundle. Tests edit authored files without re-running
        sync, so staleness of generated content is hidden unless asked for."""
        found = validate.run(self.root)
        if include_generated:
            return found
        return [item for item in found if item.rule != "generated.stale"]

    def assertClean(self) -> None:
        self.assertEqual([(item.rule, item.path, item.message) for item in self.findings()], [])

    def assertRule(self, rule: str, path: str | None = None) -> None:
        """Exactly this rule fires (possibly several times), optionally on this path."""
        found = self.findings()
        rules = {item.rule for item in found}
        self.assertEqual(rules, {rule}, [(item.rule, item.path, item.message) for item in found])
        if path is not None:
            self.assertIn(path, {item.path for item in found})

    def assertReported(self, rule: str, path: str) -> None:
        """This rule fires on this path; other findings may accompany it."""
        found = self.findings()
        self.assertIn((rule, path), {(item.rule, item.path) for item in found}, [(item.rule, item.path, item.message) for item in found])
