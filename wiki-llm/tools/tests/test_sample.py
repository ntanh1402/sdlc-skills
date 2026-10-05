"""Acceptance: the repository's sample bundle and schema pages are conformant."""

import shutil
import tempfile
import unittest
from pathlib import Path

from wikilib import docs, sync, validate
from wikilib.bundle import Bundle
from wikilib.schema import SCHEMA_DIR, Schema

SAMPLE = SCHEMA_DIR.parent / "sample"


class SampleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = Schema.load()
        cls.bundle = Bundle.load(SAMPLE, cls.schema)

    def test_sample_has_no_findings(self):
        found = [(item.severity, item.rule, item.path, item.message) for item in validate.run(SAMPLE)]
        self.assertEqual(found, [])

    def test_sync_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "sample"
            shutil.copytree(SAMPLE, copy)
            self.assertEqual(sync.write(copy), [])

    def test_sample_uses_every_type(self):
        self.assertEqual({concept.type for concept in self.bundle.concepts}, set(self.schema.types))

    def test_sample_shows_verified_and_unverified_agent_content(self):
        agent = [c for c in self.bundle.concepts if not str(c.meta["generated"]["by"]).startswith("human:")]
        self.assertTrue(any("verified" in concept.meta for concept in agent), "no agent-written, human-verified concept")
        self.assertTrue(any("verified" not in concept.meta for concept in agent), "no unverified agent-written concept")

    def test_sample_shows_pending_changes(self):
        pending = [c for c in self.bundle.concepts if c.status in ("Planned", "Modifying", "Removing")]
        self.assertTrue(pending)

    def test_schema_pages_are_generated_and_their_links_resolve(self):
        self.assertEqual(docs.stale(self.schema), [])
        self.assertEqual(docs.broken_links(), [])


if __name__ == "__main__":
    unittest.main()
