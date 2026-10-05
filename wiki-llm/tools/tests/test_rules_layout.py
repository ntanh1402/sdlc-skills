import shutil

from wikilib import sync

from .support import RuleTest

OVERVIEW = "---\ntype: Service\ntitle: X\ndescription: X.\n---\n\n# X\n"
REFERENCE = (
    "---\ntype: Reference\ntitle: Architecture overview\ndescription: The system as built.\n"
    "generated: { by: human:alice, at: 2026-09-01T09:00:00Z }\n"
    "verified: { by: human:bob, at: 2026-09-02T09:00:00Z }\n---\n\n# Architecture overview\n\nText.\n"
)


class LayoutTest(RuleTest):
    def test_fixture_is_clean(self):
        self.assertClean()

    def test_bundle_with_windows_line_endings_is_clean(self):
        for path in self.root.rglob("*.md"):
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        self.assertClean()

    def test_file_with_a_byte_order_mark_is_clean_and_keeps_it(self):
        table = self.root / "pay/datastores/DB-main/TBL-payments.md"
        table.write_bytes(b"\xef\xbb\xbf" + table.read_bytes())
        self.assertClean()
        self.edit("pay/services/SVC-pay/overview.md", "# Writes\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md)\n\n", "")
        self.assertIn(table, sync.write(self.root))
        self.assertTrue(table.read_bytes().startswith(b"\xef\xbb\xbf---\n"))
        self.assertClean()

    def test_bundle_without_applications_is_clean(self):
        shutil.rmtree(self.root / "pay")
        self.write("index.md", '---\nokf_version: "0.2"\nschema_version: "1"\n---\n\n# Applications\n\nNone\n')
        self.assertClean()

    def test_root_index_is_required(self):
        self.remove("index.md")
        self.assertRule("layout.root-index", "index.md")

    def test_schema_version_must_match(self):
        self.edit("index.md", 'schema_version: "1"', 'schema_version: "0"')
        self.assertRule("layout.schema-version", "index.md")

    def test_unknown_collection_directory(self):
        self.write("pay/tasks/index.md", "# Tasks\n")
        self.assertRule("layout.unknown-path", "pay/tasks")

    def test_unknown_file_in_bundle_root(self):
        self.write("log.md", "# Log\n")
        self.assertRule("layout.unknown-path", "log.md")

    def test_unknown_file_in_application(self):
        self.write("pay/log.md", "# Log\n")
        self.assertRule("layout.unknown-path", "pay/log.md")

    def test_folder_with_unknown_prefix(self):
        self.write("pay/services/QUEUE-x/overview.md", OVERVIEW)
        self.assertRule("layout.unknown-path", "pay/services/QUEUE-x")

    def test_owned_file_the_owner_cannot_hold(self):
        self.write("pay/services/SVC-pay/TBL-x.md", OVERVIEW)
        self.assertRule("layout.unknown-path", "pay/services/SVC-pay/TBL-x.md")

    def test_directory_inside_a_concept_folder(self):
        self.write("pay/services/SVC-pay/EP-x/overview.md", OVERVIEW)
        self.assertRule("layout.unknown-path", "pay/services/SVC-pay/EP-x")

    def test_directory_named_like_a_markdown_file(self):
        (self.root / "pay/services/SVC-pay/notes.md").mkdir()
        self.assertRule("layout.unknown-path", "pay/services/SVC-pay/notes.md")

    def test_missing_log(self):
        self.remove("pay/services/SVC-pay/log.md")
        self.assertReported("layout.missing-file", "pay/services/SVC-pay/log.md")

    def test_missing_index(self):
        self.remove("pay/services/index.md")
        self.assertReported("layout.missing-file", "pay/services/index.md")

    def test_missing_declared_file(self):
        self.remove("pay/channels/CHAN-pay-events/payload.example.json")
        self.assertReported("layout.missing-file", "pay/channels/CHAN-pay-events/payload.example.json")

    def test_undeclared_non_markdown_file(self):
        self.write("pay/services/SVC-pay/notes.txt", "x")
        self.assertRule("layout.non-markdown", "pay/services/SVC-pay/notes.txt")

    def test_non_markdown_file_linked_from_a_reference_is_allowed(self):
        self.write("pay/features/FEAT-pay/flow.png", "x")
        self.edit("pay/features/FEAT-pay/prd.md", "Shoppers pay for orders.", "Shoppers pay. ![flow](flow.png)")
        self.assertClean()

    def test_reference_in_an_application_folder(self):
        self.write("pay/architecture-overview.md", REFERENCE)
        self.assertClean()

    def test_reference_in_a_test_suite_folder(self):
        self.write("pay/tests/TS-pay/test-plan.md", REFERENCE)
        self.assertClean()

    def test_reference_in_a_service_folder_is_refused(self):
        self.write("pay/services/SVC-pay/architecture-overview.md", REFERENCE)
        self.assertRule("layout.unknown-path", "pay/services/SVC-pay/architecture-overview.md")

    def test_reference_in_an_application_folder_needs_a_person(self):
        self.write("pay/architecture-overview.md", REFERENCE.replace("by: human:bob", "by: process:nightly"))
        self.assertRule("frontmatter.reference-unverified", "pay/architecture-overview.md")

    def test_image_in_an_application_folder_linked_from_a_reference_is_allowed(self):
        self.write("pay/system.png", "x")
        self.write("pay/architecture-overview.md", REFERENCE.replace("Text.", "![system](system.png)"))
        self.assertClean()

    def test_unlinked_non_markdown_file_in_an_application_folder(self):
        self.write("pay/system.png", "x")
        self.write("pay/architecture-overview.md", REFERENCE)
        self.assertRule("layout.non-markdown", "pay/system.png")

    def test_frontmatter_type_must_match_location(self):
        self.edit("pay/datastores/DB-main/TBL-payments.md", "type: Table", "type: Endpoint")
        self.assertReported("layout.type-location", "pay/datastores/DB-main/TBL-payments.md")

    def test_key_pattern(self):
        self.write("pay/decisions/ADR-Charge_Later.md", self.read_fixture("pay/decisions/ADR-002.md"))
        self.assertReported("layout.key", "pay/decisions/ADR-Charge_Later.md")

    def read_fixture(self, rel):
        return (self.root / rel).read_text(encoding="utf-8")


class EncodingTest(RuleTest):
    """A file that is not UTF-8 is named by validate and never written by sync."""

    TABLE = "pay/datastores/DB-main/TBL-payments.md"
    SERVICE = "pay/services/SVC-pay/overview.md"

    def corrupt(self, rel):
        path = self.root / rel
        path.write_bytes(path.read_bytes() + b"\ncaf\xe9\n")
        return path.read_bytes()

    def test_concept_file_is_reported_and_left_alone_by_sync(self):
        self.edit(self.SERVICE, "# Writes\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md)\n\n", "")
        before = self.corrupt(self.TABLE)
        self.assertNotIn(self.root / self.TABLE, sync.write(self.root))
        self.assertEqual((self.root / self.TABLE).read_bytes(), before)
        self.assertReported("layout.encoding", self.TABLE)

    def test_source_of_a_generated_section_is_reported(self):
        self.corrupt(self.SERVICE)
        self.assertRule("layout.encoding", self.SERVICE)

    def test_log_is_reported(self):
        self.corrupt("pay/services/SVC-pay/log.md")
        self.assertRule("layout.encoding", "pay/services/SVC-pay/log.md")

    def test_index_is_reported_and_left_alone_by_sync(self):
        before = self.corrupt("pay/services/index.md")
        self.assertEqual(sync.write(self.root), [])
        self.assertEqual((self.root / "pay/services/index.md").read_bytes(), before)
        self.assertRule("layout.encoding", "pay/services/index.md")

    def test_root_index_is_reported(self):
        self.corrupt("index.md")
        self.assertRule("layout.encoding", "index.md")
