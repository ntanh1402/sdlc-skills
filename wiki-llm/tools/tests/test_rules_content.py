from . import fixture
from .support import RuleTest

FEATURE = "pay/features/FEAT-pay/overview.md"
CHANGE = "pay/change-requests/CR-1/overview.md"
CASE = "pay/tests/TS-pay/TC-pay-ok.md"
CHANNEL = "pay/channels/CHAN-pay-events/overview.md"
EXAMPLE = "pay/channels/CHAN-pay-events/payload.example.json"
LOG = "pay/services/SVC-pay/log.md"
ENDPOINT = "pay/services/SVC-pay/EP-pay-create.md"


class RequirementTest(RuleTest):
    def test_feature_needs_a_requirement(self):
        self.edit(FEATURE, "### REQ-pay-1\n\n**Must** — A shopper pays for an order. Functional. Verified by test.\n\n", "None.\n\n")
        self.assertIn("content.requirement", {item.rule for item in self.findings()})

    def test_change_request_may_have_no_requirements(self):
        self.edit(CHANGE, "### REQ-pay-2\n\n**Should** — A shopper applies one coupon. Functional. Verified by test.", "None.")
        self.assertNotIn("content.requirement", {item.rule for item in self.findings()})

    def test_requirement_needs_one_priority(self):
        self.edit(FEATURE, "**Must** — A shopper", "A shopper")
        self.assertRule("content.requirement", FEATURE)

    def test_requirement_needs_one_type(self):
        self.edit(FEATURE, " Functional.", "")
        self.assertRule("content.requirement", FEATURE)

    def test_requirement_needs_one_verification_method(self):
        self.edit(FEATURE, " Verified by test.", " Verified by test. Verified by demo.")
        self.assertRule("content.requirement", FEATURE)


class TableAndDiagramTest(RuleTest):
    def test_steps_table_columns(self):
        self.edit(CASE, "| Step | Action | Expected result | Validation |", "| Step | Action | Expected |")
        self.edit(CASE, "|---|---|---|---|\n| 1 | Pay | Paid | Row exists |", "|---|---|---|\n| 1 | Pay | Paid |")
        self.assertRule("content.table", CASE)

    def test_steps_table_needs_complete_rows(self):
        self.edit(CASE, "| 1 | Pay | Paid | Row exists |", "| 1 | Pay | Paid | |")
        self.assertRule("content.table", CASE)

    def test_glossary_tables_may_be_none(self):
        self.edit("pay/glossary.md", "| Role | Description |\n|---|---|\n| shopper | A paying customer. |", "None")
        self.assertClean()

    def test_glossary_table_columns(self):
        self.edit("pay/glossary.md", "| Role | Description |", "| Role | Meaning |")
        self.assertRule("content.table", "pay/glossary.md")

    def test_feature_architecture_needs_a_flowchart(self):
        self.edit(FEATURE, "flowchart LR", "graph LR")
        self.assertRule("content.mermaid", FEATURE)

    def test_application_architecture_may_be_none(self):
        self.edit("pay/overview.md", "```mermaid\nflowchart LR\n  Web --> Svc\n```", "None")
        self.assertClean()

    def test_sequence_diagram_must_be_one(self):
        self.edit(ENDPOINT, "```mermaid\nsequenceDiagram\n    Client->>Service: Call\n    Service-->>Client: 201\n```", "See the service.")
        self.assertRule("content.mermaid", ENDPOINT)

    def test_flowchart_must_be_a_flowchart(self):
        self.edit(ENDPOINT, "flowchart TD\n    A[Request] --> B[201 Created]", "sequenceDiagram\n    A->>B: Call")
        self.assertRule("content.mermaid", ENDPOINT)


class PayloadTest(RuleTest):
    def test_invalid_json(self):
        self.write(EXAMPLE, "{not json")
        self.assertRule("content.payload", CHANNEL)

    def test_example_that_is_not_utf8(self):
        (self.root / EXAMPLE).write_bytes(b'{"key": "caf\xe9", "headers": {}, "body": {}}')
        self.assertRule("content.payload", CHANNEL)

    def test_example_headers_must_be_an_object(self):
        self.write(EXAMPLE, '{"key": "p1", "headers": ["event-type"], "body": {"paymentId": "p1"}}')
        self.assertRule("content.payload", CHANNEL)
        self.assertIn("headers must be a JSON object", " ".join(item.message for item in self.findings()))

    def test_example_body_must_be_an_object(self):
        self.write(EXAMPLE, '{"key": "p1", "headers": {"event-type": "x"}, "body": "paymentId"}')
        self.assertRule("content.payload", CHANNEL)
        self.assertIn("body must be a JSON object", " ".join(item.message for item in self.findings()))

    def test_example_needs_key_headers_and_body(self):
        self.write(EXAMPLE, '{"body": {"paymentId": "p1"}}')
        self.assertRule("content.payload", CHANNEL)

    def test_example_field_missing_from_the_table(self):
        self.write(EXAMPLE, '{"key": "p1", "headers": {"event-type": "x"}, "body": {"paymentId": "p1", "amount": 5}}')
        self.assertRule("content.payload", CHANNEL)

    def test_required_table_field_missing_from_the_example(self):
        self.write(EXAMPLE, '{"key": "p1", "headers": {}, "body": {"paymentId": "p1"}}')
        self.assertRule("content.payload", CHANNEL)

    def test_optional_table_field_may_be_absent_from_the_example(self):
        self.assertClean()


class LogTest(RuleTest):
    def test_log_may_start_with_a_byte_order_mark(self):
        self.write(LOG, "\ufeff" + fixture.LOG)
        self.assertClean()

    def test_log_needs_a_title(self):
        self.write(LOG, "## 2026-09-01\n\n* **Creation**: Created.\n")
        self.assertRule("content.log", LOG)

    def test_log_heading_must_be_a_date(self):
        self.edit(LOG, "## 2026-09-01", "## September 1st")
        self.assertRule("content.log", LOG)

    def test_log_is_newest_first(self):
        self.edit(LOG, "* **Creation**: Created.\n", "* **Creation**: Created.\n\n## 2026-09-05\n\n* **Update**: Changed.\n")
        self.assertRule("content.log", LOG)

    def test_log_date_appears_once(self):
        self.edit(LOG, "* **Creation**: Created.\n", "* **Creation**: Created.\n\n## 2026-09-01\n\n* **Update**: Changed.\n")
        self.assertRule("content.log", LOG)

    def test_log_date_needs_an_entry(self):
        self.edit(LOG, "* **Creation**: Created.\n", "Created.\n")
        self.assertRule("content.log", LOG)
