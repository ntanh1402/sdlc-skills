from .support import RuleTest

SERVICE = "pay/services/SVC-pay/overview.md"
FEATURE = "pay/features/FEAT-pay/overview.md"
CHANGE = "pay/change-requests/CR-1/overview.md"
CHANNEL = "pay/channels/CHAN-pay-events/overview.md"
ENDPOINT = "pay/services/SVC-pay/EP-pay-create.md"


class HeadingsTest(RuleTest):
    def test_title_must_match_frontmatter(self):
        self.edit(SERVICE, "# Pay Service\n", "# Payments\n")
        self.assertRule("headings.title", SERVICE)

    def test_channel_title_is_fixed(self):
        self.edit(CHANNEL, "# Overview\n", "# pay.events\n")
        self.assertRule("headings.title", CHANNEL)

    def test_channel_overview_needs_dead_letter(self):
        self.edit(CHANNEL, "## Dead letter\n", "## Retries\n")
        self.assertRule("headings.missing", CHANNEL)

    def test_reference_body_is_free(self):
        self.write(
            "pay/features/FEAT-pay/prd.md",
            "---\ntype: Reference\ntitle: Pay PRD\ndescription: Approved.\n"
            "generated: { by: human:alice, at: 2026-09-01T09:00:00Z }\n"
            "verified: { by: human:bob, at: 2026-09-02T09:00:00Z }\n---\n\nNo heading at all.\n\n# Anything\n\n# Goes\n",
        )
        self.assertClean()

    def test_convention_headings_are_free_but_title_is_checked(self):
        self.edit("pay/conventions.md", "# Definition of done", "# Whatever we like")
        self.assertClean()
        self.edit("pay/conventions.md", "# Conventions\n", "# Rules\n")
        self.assertRule("headings.title", "pay/conventions.md")

    def test_missing_required_heading(self):
        self.edit(ENDPOINT, "# Behavior\n\n1. Charge.\n\n", "")
        self.assertRule("headings.missing", ENDPOINT)

    def test_undeclared_top_level_heading(self):
        self.edit(SERVICE, "# Publishes", "# Endpoints\n\nNone.\n\n# Publishes")
        self.assertRule("headings.unknown", SERVICE)

    def test_removed_v1_headings_are_undeclared(self):
        self.edit(FEATURE, "# Requirements", "# Source documents\n\nNone.\n\n# Requirements")
        self.assertRule("headings.unknown", FEATURE)

    def test_heading_order(self):
        self.edit(SERVICE, "# Reads\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md)\n\n", "")
        self.edit(SERVICE, "# Depends on", "# Reads\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md)\n\n# Depends on")
        self.assertRule("headings.order", SERVICE)

    def test_duplicate_heading(self):
        self.edit(ENDPOINT, "# Behavior\n", "# Request\n\nAgain.\n\n# Behavior\n")
        found = {item.rule for item in self.findings()}
        self.assertIn("headings.duplicate", found)

    def test_heading_inside_a_code_fence_is_ignored(self):
        self.edit(ENDPOINT, "1. Charge.", "1. Charge.\n\n```yaml\n# Not a heading\n```")
        self.assertClean()

    def test_missing_nested_heading(self):
        self.edit(FEATURE, "## Traceability", "## Mapping")
        self.assertRule("headings.missing", FEATURE)

    def test_nested_order(self):
        self.edit(FEATURE, "## Context and constraints\n\nText.\n\n", "")
        self.edit(FEATURE, "## Traceability", "## Context and constraints\n\nText.\n\n## Traceability")
        self.assertRule("headings.order", FEATURE)

    def test_optional_nested_heading_may_be_absent(self):
        self.edit(
            FEATURE,
            "## Frontends\n\n* [WEB-shop](../../frontends/WEB-shop/overview.md)\n* [MB-shop](../../frontends/MB-shop/overview.md)\n\n",
            "",
        )
        self.assertClean()

    def test_approved_change_request_needs_a_delta(self):
        text = (self.root / CHANGE).read_text(encoding="utf-8")
        start = text.index("# Delta")
        self.write(CHANGE, text[:start] + "# Delta\n\nNone — pending architecture\n")
        self.assertIn("headings.none-not-allowed", {item.rule for item in self.findings()})

    def test_req_approved_change_request_may_have_no_delta(self):
        text = (self.root / CHANGE).read_text(encoding="utf-8")
        start = text.index("# Delta")
        self.write(CHANGE, text[:start].replace("status: Approved", "status: ReqApproved") + "# Delta\n\nNone — pending architecture\n")
        self.assertNotIn("headings.none-not-allowed", {item.rule for item in self.findings()})

    def feature_without_architecture(self, status):
        text = (self.root / FEATURE).read_text(encoding="utf-8")
        start = text.index("# Architecture")
        end = text.find("\n# ", start + 1)
        rest = "" if end == -1 else text[end:]
        self.write(FEATURE, text[:start].replace("status: InDev", f"status: {status}") + "# Architecture\n\nNone\n" + rest)
        return {item.rule for item in self.findings()}

    def test_feature_architecture_may_be_none_before_design(self):
        for status in ("Draft", "ReqApproved"):
            rules = self.feature_without_architecture(status)
            self.assertNotIn("headings.missing", rules, status)
            self.assertNotIn("headings.none-not-allowed", rules, status)

    def test_designed_feature_needs_an_architecture(self):
        for status in ("Approved", "InDev", "Released", "Deprecated"):
            self.assertIn("headings.none-not-allowed", self.feature_without_architecture(status), status)

    def test_proposed_change_request_may_have_no_delta(self):
        text = (self.root / CHANGE).read_text(encoding="utf-8")
        start = text.index("# Delta")
        self.write(CHANGE, text[:start].replace("status: Approved", "status: Proposed") + "# Delta\n\nNone — pending architecture\n")
        self.assertNotIn("headings.none-not-allowed", {item.rule for item in self.findings()})
