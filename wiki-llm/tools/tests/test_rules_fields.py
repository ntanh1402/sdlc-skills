from .support import RuleTest

SERVICE = "pay/services/SVC-pay/overview.md"
PRD = "pay/features/FEAT-pay/prd.md"


class FieldsTest(RuleTest):
    def test_syntax_error_is_reported(self):
        self.edit(SERVICE, "description: Takes payments.", "description: Takes: payments.")
        self.assertRule("frontmatter.syntax", SERVICE)

    def test_file_without_frontmatter_is_reported_not_crashed(self):
        self.write(SERVICE, "# Pay Service\n\nNo frontmatter here.\n")
        self.assertReported("frontmatter.syntax", SERVICE)
        self.assertReported("frontmatter.missing-field", SERVICE)

    def test_empty_file_is_reported_not_crashed(self):
        self.write("pay/datastores/DB-main/TBL-payments.md", "")
        self.assertReported("frontmatter.syntax", "pay/datastores/DB-main/TBL-payments.md")

    def test_missing_required_type_field(self):
        self.edit(SERVICE, "serviceType: api\n", "")
        self.assertRule("frontmatter.missing-field", SERVICE)

    def test_missing_required_common_field(self):
        self.edit(SERVICE, "generated: { by: human:alice, at: 2026-09-01T09:00:00Z }\n", "")
        self.assertRule("frontmatter.missing-field", SERVICE)

    def test_missing_status_on_lifecycle_type(self):
        self.edit("pay/datastores/DB-main/overview.md", "status: Active\n", "")
        self.assertRule("frontmatter.missing-field", "pay/datastores/DB-main/overview.md")

    def test_undeclared_field(self):
        self.edit(SERVICE, "serviceType: api", "serviceType: api\nrepoUrl: https://example.com/x")
        self.assertRule("frontmatter.unknown-field", SERVICE)

    def test_removed_v1_fields_are_undeclared(self):
        self.edit(SERVICE, "serviceType: api", "serviceType: api\norigin: human")
        self.assertRule("frontmatter.unknown-field", SERVICE)

    def test_status_on_document_type_is_undeclared(self):
        self.edit("pay/tests/TS-pay/TC-pay-ok.md", "risk: high", "risk: high\nstatus: Draft")
        self.assertRule("frontmatter.unknown-field", "pay/tests/TS-pay/TC-pay-ok.md")

    def test_enum_value(self):
        self.edit(SERVICE, "serviceType: api", "serviceType: daemon")
        self.assertRule("frontmatter.bad-value", SERVICE)

    def test_status_value(self):
        self.edit(SERVICE, "status: Active", "status: Stable")
        self.assertRule("frontmatter.bad-value", SERVICE)

    def test_boolean_integer_timestamp_and_date_kinds(self):
        self.edit(SERVICE, "serviceType: api", "serviceType: api\nport: eighty")
        self.edit("pay/datastores/DB-main/TBL-payments.md", "tableName: payments", "tableName: payments\npii: maybe")
        self.edit("pay/tests/TS-pay/TC-pay-ok.md", "risk: high", "risk: high\nstale_after: yesterday")
        self.edit("pay/decisions/ADR-002.md", "decisionDate: 2026-08-20", "decisionDate: 20 Aug")
        found = {(item.rule, item.path) for item in self.findings()}
        self.assertEqual(
            found,
            {
                ("frontmatter.bad-value", SERVICE),
                ("frontmatter.bad-value", "pay/datastores/DB-main/TBL-payments.md"),
                ("frontmatter.bad-value", "pay/tests/TS-pay/TC-pay-ok.md"),
                ("frontmatter.bad-value", "pay/decisions/ADR-002.md"),
            },
        )

    def test_generated_needs_a_known_actor_form(self):
        self.edit(SERVICE, "by: human:alice", "by: alice")
        self.assertRule("frontmatter.bad-value", SERVICE)

    def test_generated_needs_an_offset_timestamp(self):
        self.edit(SERVICE, "at: 2026-09-01T09:00:00Z", "at: 2026-09-01")
        self.assertRule("frontmatter.bad-value", SERVICE)

    def test_agent_actor_and_verified_list_are_accepted(self):
        self.edit(
            SERVICE,
            "generated: { by: human:alice, at: 2026-09-01T09:00:00Z }",
            "generated: { by: sdlc-import/1.0.0, at: 2026-09-01T09:00:00+07:00 }\n"
            "verified:\n  - { by: process:nightly, at: 2026-09-02T02:00:00Z }\n  - { by: human:bob, at: 2026-09-03T09:00:00Z }",
        )
        self.assertClean()

    def test_source_needs_a_resource(self):
        self.edit("pay/features/FEAT-pay/overview.md", "    resource: prd.md\n", "")
        self.assertRule("frontmatter.bad-value", "pay/features/FEAT-pay/overview.md")

    def test_tags_must_be_a_list(self):
        self.edit(SERVICE, "serviceType: api", "serviceType: api\ntags: payments")
        self.assertRule("frontmatter.bad-value", SERVICE)

    def test_reference_needs_human_verification(self):
        self.edit(PRD, "verified: { by: human:bob, at: 2026-09-02T09:00:00Z }\n", "")
        self.assertRule("frontmatter.reference-unverified", PRD)

    def test_reference_verified_only_by_a_process_is_rejected(self):
        self.edit(PRD, "by: human:bob", "by: process:nightly")
        self.assertRule("frontmatter.reference-unverified", PRD)

    def test_stale_concept_is_a_warning_not_an_error(self):
        self.edit(SERVICE, "serviceType: api", "serviceType: api\nstale_after: 2020-01-01T00:00:00Z")
        found = self.findings()
        self.assertEqual([(item.rule, item.severity) for item in found], [("stale.expired", "warning")])

    def test_impossible_stale_after_date_is_reported_not_crashed(self):
        self.edit(SERVICE, "serviceType: api", "serviceType: api\nstale_after: 2026-13-45T00:00:00Z")
        self.assertRule("frontmatter.bad-value", SERVICE)

    def test_future_stale_after_is_silent(self):
        self.edit(SERVICE, "serviceType: api", "serviceType: api\nstale_after: 2999-01-01T00:00:00Z")
        self.assertClean()
