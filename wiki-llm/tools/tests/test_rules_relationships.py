from .support import RuleTest

SERVICE = "pay/services/SVC-pay/overview.md"
TASK = "pay/features/FEAT-pay/TASK-pay-001.md"
CASE = "pay/tests/TS-pay/TC-pay-ok.md"
CHANGE = "pay/change-requests/CR-1/overview.md"
SUBSCRIPTION = "pay/services/SVC-pay/SUB-pay-events.md"
ADR = "pay/decisions/ADR-002.md"
READS = "# Reads\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md)"


class RelationshipsTest(RuleTest):
    def rules(self):
        return {item.rule for item in self.findings()}

    def test_illegal_target_under_service_reads(self):
        self.edit(
            SERVICE,
            "# Reads\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md)",
            "# Reads\n\n* [CACHE-pay](../../datastores/CACHE-pay/overview.md)",
        )
        self.assertRule("relationships.target-type", SERVICE)

    def test_task_scope_rejects_a_non_design_target(self):
        """The old validator let Tasks scope anything; this is one of the defects it missed."""
        self.edit(
            TASK,
            "* [TBL-payments](../../datastores/DB-main/TBL-payments.md) — new — the table.",
            "* [FEAT-pay](overview.md) — new — the feature.",
        )
        self.assertIn("relationships.target-type", self.rules())

    def test_task_scope_accepts_every_design_type(self):
        self.edit(
            "pay/features/FEAT-pay/TASK-pay-001.md",
            "* [TBL-payments](../../datastores/DB-main/TBL-payments.md) — new — the table.",
            "* [OP-charge](../../externals/EXT-bank/OP-charge.md) — modified — a.\n"
            "* [CACHE-pay](../../datastores/CACHE-pay/overview.md) — modified — b.\n"
            "* [WEB-shop](../../frontends/WEB-shop/overview.md) — modified — c.",
        )
        self.assertNotIn("relationships.target-type", self.rules())

    def test_test_case_coverage_rejects_an_illegal_target(self):
        """The second defect the old validator missed."""
        self.edit(CASE, "* [EP-pay-create](../../services/SVC-pay/EP-pay-create.md)", "* [TS-pay](overview.md)")
        self.assertRule("relationships.target-type", CASE)

    def test_test_case_may_cover_only_a_design_concept(self):
        self.edit(CASE, "* [REQ-pay-1](../../features/FEAT-pay/overview.md#req-pay-1)\n", "")
        self.assertClean()

    def test_test_case_may_cover_a_decision(self):
        self.edit(CASE, "* [EP-pay-create](../../services/SVC-pay/EP-pay-create.md)", "* [ADR-002](../../decisions/ADR-002.md)")
        self.assertClean()

    def test_requirement_anchor_may_be_written_in_upper_case(self):
        """Links resolve anchors without regard to case; so does the Requirement test."""
        self.edit(CASE, "overview.md#req-pay-1)", "overview.md#REQ-pay-1)")
        self.assertClean()

    def test_feature_link_without_requirement_anchor_is_not_a_requirement(self):
        self.edit(CASE, "overview.md#req-pay-1)", "overview.md)")
        self.assertRule("relationships.target-type", CASE)

    def test_decision_may_affect_a_feature(self):
        self.assertClean()

    def test_decision_may_not_affect_a_task(self):
        self.edit(ADR, "* [FEAT-pay](../features/FEAT-pay/overview.md)", "* [TASK-pay-001](../features/FEAT-pay/TASK-pay-001.md)")
        self.assertRule("relationships.target-type", ADR)

    def test_list_item_without_link(self):
        self.edit(SERVICE, "# Reads\n\n", "# Reads\n\n* the payments table\n")
        self.assertRule("relationships.target-type", SERVICE)

    def test_external_url_is_not_a_relationship_target(self):
        self.edit(SERVICE, "# Reads\n\n", "# Reads\n\n* [docs](https://example.com/docs)\n")
        self.assertRule("relationships.target-type", SERVICE)

    def test_prose_none_is_accepted_where_minimum_is_zero(self):
        self.edit(SERVICE, "# Reads\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md)", "# Reads\n\nNone.")
        self.assertNotIn("relationships.cardinality", self.rules())

    def test_minimum_links(self):
        self.edit(SUBSCRIPTION, "* [CHAN-pay-events](../../channels/CHAN-pay-events/overview.md)", "None.")
        self.assertRule("relationships.cardinality", SUBSCRIPTION)

    def test_maximum_links(self):
        self.edit(
            CHANGE,
            "* [FEAT-pay](../../features/FEAT-pay/overview.md)\n\n# Reason",
            "* [FEAT-pay](../../features/FEAT-pay/overview.md)\n* [FEAT-pay again](../../features/FEAT-pay/overview.md)\n\n# Reason",
        )
        self.assertIn("relationships.cardinality", self.rules())

    def test_duplicate_target(self):
        self.edit(
            SERVICE,
            "# Reads\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md)",
            "# Reads\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md)\n* [payments](../../datastores/DB-main/TBL-payments.md)",
        )
        self.assertRule("relationships.duplicate", SERVICE)

    def test_required_qualifier_missing(self):
        self.edit(SERVICE, "— rw — idempotency keys.", "— idempotency keys.")
        self.assertRule("relationships.qualifier", SERVICE)

    def test_required_qualifier_outside_its_set(self):
        self.edit(TASK, "— new — the table.", "— created — the table.")
        self.assertIn("relationships.qualifier", self.rules())

    def test_optional_qualifier_may_be_absent(self):
        self.edit(SERVICE, "— critical — the payment rail.", "— the payment rail.")
        self.assertClean()

    def test_nested_relationship_heading_is_checked(self):
        self.edit(
            "pay/features/FEAT-pay/overview.md",
            "* [SVC-pay](../../services/SVC-pay/overview.md) — takes the payment.",
            "* [TBL-payments](../../datastores/DB-main/TBL-payments.md) — not a service.",
        )
        self.assertRule("relationships.target-type", "pay/features/FEAT-pay/overview.md")

    def scope_links(self, name):
        self.edit(
            TASK,
            "* [TBL-payments](../../datastores/DB-main/TBL-payments.md) — new — the table.",
            f"* [DB-main](../../datastores/DB-main/{name}) — new — the table.",
        )

    def test_index_is_not_a_relationship_target(self):
        self.scope_links("index.md")
        self.assertRule("relationships.target-type", TASK)

    def test_log_is_not_a_relationship_target(self):
        self.scope_links("log.md")
        self.assertRule("relationships.target-type", TASK)

    def test_numbered_item_is_not_a_relationship(self):
        self.edit(SERVICE, READS, "# Reads\n\n1. [TBL-payments](../../datastores/DB-main/TBL-payments.md)")
        self.assertRule("relationships.unparsed", SERVICE)

    def test_plus_bullet_is_not_a_relationship(self):
        self.edit(SERVICE, READS, "# Reads\n\n+ [TBL-payments](../../datastores/DB-main/TBL-payments.md)")
        self.assertRule("relationships.unparsed", SERVICE)

    def test_indented_bullet_is_not_a_relationship(self):
        self.edit(SERVICE, READS, "# Reads\n\n  * [TBL-payments](../../datastores/DB-main/TBL-payments.md)")
        self.assertRule("relationships.unparsed", SERVICE)

    def test_bullet_nested_under_a_relationship_is_not_a_relationship(self):
        self.edit(SERVICE, READS, READS + "\n  * [CACHE-pay](../../datastores/CACHE-pay/overview.md)")
        self.assertRule("relationships.unparsed", SERVICE)

    def test_paragraph_that_starts_with_a_link_and_a_dash_is_not_a_relationship(self):
        self.edit(SERVICE, READS, "# Reads\n\n[TBL-payments](../../datastores/DB-main/TBL-payments.md) — the payments.")
        self.assertRule("relationships.unparsed", SERVICE)

    def test_checkbox_under_a_relationship_is_not_a_relationship(self):
        self.edit(SERVICE, READS, READS + "\n  * [ ] confirm the index\n\n1. [x] reviewed")
        self.assertClean()

    def test_unparsed_message_says_how_to_write_the_item(self):
        self.edit(SERVICE, READS, "# Reads\n\n1. [TBL-payments](../../datastores/DB-main/TBL-payments.md)")
        messages = [item.message for item in self.findings() if item.rule == "relationships.unparsed"]
        self.assertEqual(len(messages), 1)
        self.assertIn("top-level `*` list item", messages[0])

    def test_prose_with_an_inline_link_is_not_a_relationship(self):
        self.edit(
            SERVICE,
            READS,
            "# Reads\n\nEvery read goes through [the payments table](../../datastores/DB-main/TBL-payments.md).\n\n"
            "[The table](../../datastores/DB-main/TBL-payments.md) is read on each request, as is\n"
            "[the cache](../../datastores/CACHE-pay/overview.md) — a wrapped line, not a new paragraph.\n\n"
            "* [TBL-payments](../../datastores/DB-main/TBL-payments.md) — the table, see\n"
            "  [the cache](../../datastores/CACHE-pay/overview.md) — for hot keys.",
        )
        self.assertClean()

    def test_numbered_list_outside_a_relationship_heading_is_legal(self):
        self.edit(
            "pay/services/SVC-pay/EP-pay-create.md",
            "1. Charge.",
            "1. [Charge](../../externals/EXT-bank/OP-charge.md) — through the bank.",
        )
        self.assertClean()
