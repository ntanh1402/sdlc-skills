import tempfile
import unittest
from pathlib import Path

from wikilib.bundle import Bundle
from wikilib.schema import Schema

from . import fixture


class BundleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.root = fixture.make_bundle(Path(cls._tmp.name) / "bundle")
        cls.bundle = Bundle.load(cls.root, Schema.load())

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def concept(self, rel):
        return next(concept for concept in self.bundle.concepts if concept.rel == rel)

    def test_fixture_loads_without_layout_problems(self):
        self.assertEqual(self.bundle.problems, [])

    def test_every_type_is_present_in_the_fixture(self):
        self.assertEqual({concept.type for concept in self.bundle.concepts}, set(self.bundle.schema.types))

    def test_type_and_key_come_from_location(self):
        table = self.concept("pay/datastores/DB-main/TBL-payments.md")
        self.assertEqual((table.type, table.key, table.app), ("Table", "TBL-payments", "pay"))
        self.assertEqual(table.owner.key, "DB-main")
        service = self.concept("pay/services/SVC-pay/overview.md")
        self.assertEqual((service.type, service.key), ("Service", "SVC-pay"))
        self.assertEqual(service.folder.name, "SVC-pay")
        self.assertEqual(self.concept("pay/features/FEAT-pay/prd.md").type, "Reference")
        self.assertEqual(self.concept("pay/glossary.md").type, "Glossary")
        self.assertEqual(self.concept("pay/decisions/ADR-001.md").type, "ArchitectureDecision")

    def test_owned_lists_children(self):
        feature = self.concept("pay/features/FEAT-pay/overview.md")
        self.assertEqual([task.key for task in self.bundle.owned(feature, "Task")], ["TASK-pay-001", "TASK-pay-002"])

    def test_resolve_relative_absolute_anchor_and_external(self):
        source = self.root / "pay/services/SVC-pay/overview.md"
        self.assertEqual(
            self.bundle.resolve(source, "../../datastores/DB-main/TBL-payments.md"),
            (self.bundle.root / "pay/datastores/DB-main/TBL-payments.md", ""),
        )
        self.assertEqual(
            self.bundle.resolve(source, "/pay/overview.md#architecture"),
            (self.bundle.root / "pay/overview.md", "architecture"),
        )
        self.assertEqual(self.bundle.resolve(source, "#reads"), (source, "reads"))
        self.assertEqual(self.bundle.resolve(source, "https://example.com/x"), (None, ""))

    def test_relations_carry_target_type_and_qualifier(self):
        service = self.concept("pay/services/SVC-pay/overview.md")
        uses = self.bundle.relations(service, ["Uses"])
        self.assertEqual([(r.kind, r.qualifier) for r in uses], [("Cache", "rw"), ("BlobStore", "write"), ("SearchIndex", "read")])
        depends = self.bundle.relations(service, ["Depends on"])
        self.assertEqual([(r.kind, r.qualifier) for r in depends], [("ExternalService", "critical")])
        publishes = self.bundle.relations(service, ["Publishes"])
        self.assertEqual([(r.kind, r.qualifier) for r in publishes], [("MessageChannel", None)])

    def test_relations_in_nested_heading_and_requirement_anchor(self):
        change = self.concept("pay/change-requests/CR-1/overview.md")
        delta = self.bundle.relations(change, ["Delta", "Target delta"])
        self.assertEqual([(r.concept.key, r.qualifier) for r in delta], [("EP-pay-create", "modified")])
        case = self.concept("pay/tests/TS-pay/TC-pay-ok.md")
        self.assertEqual([r.kind for r in self.bundle.relations(case, ["Covers"])], ["Requirement", "Endpoint"])

    def test_file_that_is_not_utf8_loads_without_raising(self):
        path = self.root / "pay/features/FEAT-pay/prd.md"
        original = path.read_bytes()
        path.write_bytes(original + b"\xff\xfe caf\xe9\n")
        try:
            bundle = Bundle.load(self.root, Schema.load())
        finally:
            path.write_bytes(original)
        self.assertTrue(any(concept.rel == "pay/features/FEAT-pay/prd.md" for concept in bundle.concepts))

    def test_dot_entries_are_ignored(self):
        fixture.write(self.root, ".git/config", "x")
        fixture.write(self.root, "pay/.DS_Store", "x")
        self.assertEqual(Bundle.load(self.root, Schema.load()).problems, [])


if __name__ == "__main__":
    unittest.main()
