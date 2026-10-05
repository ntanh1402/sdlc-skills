import shutil

from wikilib import sync

from . import fixture
from .support import RuleTest

TABLE = "pay/datastores/DB-main/TBL-payments.md"
SERVICE = "pay/services/SVC-pay/overview.md"
CHANNEL = "pay/channels/CHAN-pay-events/overview.md"
FEATURE = "pay/features/FEAT-pay/overview.md"


class ApplySectionTest(RuleTest):
    ORDER = ["Schema", "Indexes", "Used by", "Pending changes"]

    def test_inserts_before_the_next_declared_heading(self):
        body = "\n# payments\n\n# Schema\n\ntable\n\n# Pending changes\n\n* x\n"
        result = sync.apply_section(body, "Used by", ["* a"], self.ORDER)
        self.assertEqual(result, "\n# payments\n\n# Schema\n\ntable\n\n# Used by\n\n* a\n\n# Pending changes\n\n* x\n")

    def test_appends_when_no_later_heading_exists(self):
        result = sync.apply_section("\n# payments\n\n# Schema\n\ntable\n", "Used by", ["* a"], self.ORDER)
        self.assertEqual(result, "\n# payments\n\n# Schema\n\ntable\n\n# Used by\n\n* a\n")

    def test_replaces_existing_content(self):
        body = "\n# payments\n\n# Used by\n\n* old — with a hand-written note\n\nStray prose.\n\n# Pending changes\n\n* x\n"
        result = sync.apply_section(body, "Used by", ["* new"], self.ORDER)
        self.assertEqual(result, "\n# payments\n\n# Used by\n\n* new\n\n# Pending changes\n\n* x\n")

    def test_none_content_removes_the_section(self):
        body = "\n# payments\n\n# Used by\n\n* old\n\n# Pending changes\n\n* x\n"
        self.assertEqual(sync.apply_section(body, "Used by", None, self.ORDER), "\n# payments\n\n# Pending changes\n\n* x\n")

    def test_heading_inside_a_fence_is_not_a_boundary(self):
        body = "\n# payments\n\n# Schema\n\n```sql\n# Used by\n```\n"
        result = sync.apply_section(body, "Used by", ["* a"], self.ORDER)
        self.assertTrue(result.endswith("```\n\n# Used by\n\n* a\n"))


class SyncTest(RuleTest):
    def text(self, rel):
        return fixture.read(self.root, rel)

    def test_fixture_is_in_sync(self):
        self.assertEqual(sync.write(self.root), [])

    def test_indexes_list_a_reference_in_an_application_and_a_suite(self):
        reference = (
            "---\ntype: Reference\ntitle: Test plan\ndescription: The manual cases.\n"
            "generated: { by: human:alice, at: 2026-09-01T09:00:00Z }\n"
            "verified: { by: human:bob, at: 2026-09-02T09:00:00Z }\n---\n\n# Test plan\n"
        )
        self.write("pay/test-plan.md", reference)
        self.write("pay/tests/TS-pay/test-plan.md", reference)
        sync.write(self.root)
        self.assertIn("* [Test plan](test-plan.md) - The manual cases.", self.text("pay/index.md"))
        self.assertIn("# Source documents\n\n* [Test plan](test-plan.md) - The manual cases.", self.text("pay/tests/TS-pay/index.md"))

    def test_sync_is_idempotent(self):
        self.edit(SERVICE, "# Reads\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md)\n\n", "")
        self.assertNotEqual(sync.write(self.root), [])
        self.assertEqual(sync.write(self.root), [])

    def test_sync_on_a_bundle_with_errors_keeps_authored_text(self):
        self.write(TABLE, "# payments\n\nFrontmatter was lost.\n\n# Schema\n\nA table.\n")
        self.edit(SERVICE, "status: Active", "status: Bogus")
        sync.write(self.root)
        text = self.text(TABLE)
        self.assertTrue(text.startswith("# payments\n\nFrontmatter was lost.\n\n# Schema\n\nA table.\n"))
        self.assertIn("# Used by\n\n* [Pay Service](../../services/SVC-pay/overview.md) — rw\n", text)
        self.assertEqual(sync.write(self.root), [])

    def test_sync_on_a_bundle_without_applications(self):
        shutil.rmtree(self.root / "pay")
        sync.write(self.root)
        self.assertTrue(self.text("index.md").endswith("# Applications\n\nNone\n"))

    def test_table_used_by_merges_read_and_write(self):
        self.assertIn("# Used by\n\n* [Pay Service](../../services/SVC-pay/overview.md) — rw\n", self.text(TABLE))

    def test_table_used_by_follows_the_service(self):
        self.edit(SERVICE, "# Writes\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md)\n\n", "")
        sync.write(self.root)
        self.assertIn("* [Pay Service](../../services/SVC-pay/overview.md) — read\n", self.text(TABLE))

    def test_used_by_takes_the_qualifier_from_uses(self):
        self.assertIn("* [Pay Service](../../services/SVC-pay/overview.md) — write\n", self.text("pay/datastores/BLOB-receipts/overview.md"))

    def test_empty_reverse_view_says_none(self):
        self.edit(SERVICE, "* [IDX-payments](../../datastores/IDX-payments/overview.md) — read — search.\n", "")
        sync.write(self.root)
        self.assertTrue(self.text("pay/datastores/IDX-payments/overview.md").endswith("# Used by\n\nNone\n"))

    def test_channel_publishers_and_subscribers(self):
        text = self.text(CHANNEL)
        self.assertIn("# Publishers\n\n* [Pay Service](../../services/SVC-pay/overview.md)\n", text)
        self.assertIn("# Subscribers\n\n* [On payment event](../../services/SVC-pay/SUB-pay-events.md)\n", text)

    def test_feature_change_history(self):
        self.assertIn("# Change history\n\n* [Accept coupons](../../change-requests/CR-1/overview.md)\n", self.text(FEATURE))

    def test_superseded_by_is_written_only_when_needed(self):
        self.assertIn("# Superseded by\n\n* [Charge through the bank operation](ADR-002.md)\n", self.text("pay/decisions/ADR-001.md"))
        self.assertNotIn("# Superseded by", self.text("pay/decisions/ADR-002.md"))

    def test_generated_section_keeps_its_place_before_pending_changes(self):
        fixture.edit(self.root, TABLE, "status: Active", "status: Modifying")
        fixture.edit(self.root, TABLE, "# Used by", "# Pending changes\n\n* [CR-1](../../change-requests/CR-1/overview.md) — modified — x.\n\n# Used by")
        text = self.text(TABLE)
        self.write(TABLE, text[: text.index("# Used by")].rstrip("\n") + "\n")
        sync.write(self.root)
        text = self.text(TABLE)
        self.assertLess(text.index("# Used by"), text.index("# Pending changes"))

    def test_root_index(self):
        self.assertEqual(
            self.text("index.md"),
            '---\nokf_version: "0.2"\nschema_version: "1"\n---\n\n# Applications\n\n* [Pay](pay/overview.md) - Payment platform.\n',
        )

    def test_application_index_lists_own_files_and_present_collections(self):
        text = self.text("pay/index.md")
        self.assertTrue(text.startswith("# Pay\n\n* [Overview](overview.md) - Payment platform.\n* [Conventions](conventions.md) - How we build.\n"))
        self.assertIn("# Collections\n\n* [Features](features/index.md) - ", text)
        self.assertLess(text.index("features/index.md"), text.index("decisions/index.md"))

    def test_collection_index_is_sorted_by_key(self):
        self.assertEqual(
            self.text("pay/datastores/index.md"),
            "# Datastores\n\n"
            "* [Receipts](BLOB-receipts/overview.md) - Receipt PDFs.\n"
            "* [Pay Cache](CACHE-pay/overview.md) - Idempotency keys.\n"
            "* [Main Database](DB-main/overview.md) - Relational store.\n"
            "* [Payment Search](IDX-payments/overview.md) - Search payments.\n",
        )

    def test_file_collection_index(self):
        self.assertIn("* [Charge synchronously](ADR-001.md) - Charge during the request.\n", self.text("pay/decisions/index.md"))

    def test_concept_index_groups_owned_files(self):
        self.assertEqual(
            self.text("pay/services/SVC-pay/index.md"),
            "# Pay Service\n\n* [Overview](overview.md) - Takes payments.\n\n"
            "# Endpoints\n\n* [Create payment](EP-pay-create.md) - POST /payments.\n* [Refund payment](EP-pay-refund.md) - POST /refunds.\n\n"
            "# Subscriptions\n\n* [On payment event](SUB-pay-events.md) - Sends a receipt.\n\n"
            "# History\n\n* [Change log](log.md) - History of Pay Service.\n",
        )

    def test_concept_index_lists_declared_extra_files(self):
        self.assertIn("# Files\n\n* [payload.example.json](payload.example.json) - Example message: key, headers, body.\n", self.text("pay/channels/CHAN-pay-events/index.md"))


class ConvergenceTest(RuleTest):
    """sync never grows a file it cannot parse, and a second run changes nothing."""

    def unchanged_after_three_runs(self, rel):
        before = (self.root / rel).read_bytes()
        for _ in range(3):
            self.assertNotIn(self.root / rel, sync.write(self.root))
            self.assertEqual((self.root / rel).read_bytes(), before)

    def test_unclosed_fence_is_left_alone_and_reported(self):
        self.edit(FEATURE, "  Web->>Svc: pay\n```\n", "  Web->>Svc: pay\n")
        self.unchanged_after_three_runs(FEATURE)
        self.assertReported("content.fence", FEATURE)

    def test_fence_closed_by_a_later_block_does_not_grow_the_file(self):
        """Without its own closing line, the first diagram runs to the end of the next one."""
        self.edit(FEATURE, "  Web --> Svc\n```\n\n## Services", "  Web --> Svc\n\n## Services")
        self.unchanged_after_three_runs(FEATURE)
        self.assertReported("headings.missing", FEATURE)

    def test_unclosed_fence_in_a_log_is_reported(self):
        self.edit("pay/services/SVC-pay/log.md", "* **Creation**: Created.\n", "* **Creation**: Created.\n\n```text\nnotes\n")
        self.assertReported("content.fence", "pay/services/SVC-pay/log.md")

    def test_tilde_line_inside_a_backtick_fence_does_not_hide_a_generated_section(self):
        self.edit(TABLE, "# Schema\n\n", "# Schema\n\n```text\n~~~\n# not a heading\n```\n\n")
        self.assertEqual(sync.write(self.root), [])
        self.assertClean()

    def test_file_that_sync_cannot_settle_is_left_alone_and_reported(self):
        adr = "pay/decisions/ADR-002.md"
        self.write(adr, self.text(adr) + "\n# Superseded by\n\nNone\n\n# Superseded by\n\nNone\n")
        self.unchanged_after_three_runs(adr)
        self.assertReported("generated.unstable", adr)

    def text(self, rel):
        return fixture.read(self.root, rel)


class GeneratedRuleTest(RuleTest):
    def stale(self):
        return {item.path for item in self.findings(include_generated=True) if item.rule == "generated.stale"}

    def test_hand_edited_index_is_stale(self):
        self.edit("pay/services/index.md", "Takes payments.", "Takes payments, by hand.")
        self.assertEqual(self.stale(), {"pay/services/index.md"})

    def test_hand_edited_reverse_view_is_stale(self):
        self.edit(TABLE, "— rw", "— rw — a note added by hand")
        self.assertEqual(self.stale(), {TABLE})

    def test_changed_source_makes_the_copy_stale(self):
        self.edit(SERVICE, "description: Takes payments.", "description: Takes card payments.")
        self.assertEqual(self.stale(), {"pay/services/index.md", "pay/services/SVC-pay/index.md"})

    def test_missing_index_is_stale(self):
        self.remove("pay/tests/index.md")
        self.assertIn("pay/tests/index.md", self.stale())
