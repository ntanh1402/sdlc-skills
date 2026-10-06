from .support import RuleTest

SERVICE = "pay/services/SVC-pay/overview.md"
FEATURE = "pay/features/FEAT-pay/overview.md"
LOG = "pay/services/SVC-pay/log.md"


class LinksTest(RuleTest):
    def test_missing_target(self):
        self.edit(SERVICE, "Takes payments.\n\n# Publishes", "Takes payments. See [notes](notes.md).\n\n# Publishes")
        self.assertRule("links.unresolved", SERVICE)

    def test_missing_target_in_a_log(self):
        self.edit(LOG, "Created.", "Created [the task](../../tasks/TASK-pay-001/overview.md).")
        self.assertRule("links.unresolved", LOG)

    def test_missing_image(self):
        self.edit(SERVICE, "Takes payments.\n\n# Publishes", "Takes payments. ![diagram](diagram.png)\n\n# Publishes")
        self.assertRule("links.unresolved", SERVICE)

    def test_link_that_leaves_the_bundle(self):
        """A bundle in its own repository cannot link the schema; the old sample did."""
        self.edit(SERVICE, "Takes payments.\n\n# Publishes", "Takes payments. See [the format](../../../../okf-spec.md).\n\n# Publishes")
        self.assertRule("links.outside-bundle", SERVICE)

    def test_absolute_link_resolves_from_the_bundle_root(self):
        self.edit(SERVICE, "Takes payments.\n\n# Publishes", "Takes payments. Part of [Pay](/pay/overview.md).\n\n# Publishes")
        self.assertClean()

    def test_link_to_a_folder(self):
        self.edit(SERVICE, "Takes payments.\n\n# Publishes", "Takes payments. See [the bank](../../externals/EXT-bank/).\n\n# Publishes")
        self.assertRule("links.folder-link", SERVICE)

    def test_missing_anchor(self):
        self.edit("pay/tests/TS-pay/TC-pay-ok.md", "#req-pay-1", "#req-pay-9")
        self.assertIn("links.anchor", {item.rule for item in self.findings()})

    def test_anchor_within_the_same_file(self):
        self.edit(FEATURE, "[REQ-pay-1](#req-pay-1)", "[REQ-pay-1](#req-pay-7)")
        self.assertRule("links.anchor", FEATURE)

    def test_external_and_mail_links_are_ignored(self):
        self.edit(
            SERVICE,
            "Takes payments.\n\n# Publishes",
            "Takes payments. See [docs](https://example.com/x) or [mail](mailto:a@example.com).\n\n# Publishes",
        )
        self.assertClean()

    def test_link_inside_a_code_fence_is_ignored(self):
        self.edit(SERVICE, "Takes payments.\n\n# Publishes", "Takes payments.\n\n```md\n[x](missing.md)\n```\n\n# Publishes")
        self.assertClean()

    def test_relative_source_resource_must_exist(self):
        self.edit(SERVICE, "ownerTeam: payments", "ownerTeam: payments\nsources:\n  - id: brief\n    resource: brief.md")
        self.assertRule("links.resource", SERVICE)

    def test_source_may_not_be_a_reference(self):
        for resource in ("../../references/REF-pay-prd/overview.md", "/pay/references/REF-pay-prd/prd.md"):
            with self.subTest(resource=resource):
                self.edit(FEATURE, "ownerTeam: payments", f"ownerTeam: payments\nsources:\n  - id: prd\n    resource: {resource}")
                self.assertRule("links.source-reference", FEATURE)
                self.edit(FEATURE, f"ownerTeam: payments\nsources:\n  - id: prd\n    resource: {resource}", "ownerTeam: payments")

    def test_a_reference_may_point_at_its_own_content(self):
        self.edit("pay/references/REF-pay-prd/overview.md", "status: Active", "status: Active\nresource: prd.md")
        self.assertClean()

    def test_relative_resource_must_exist(self):
        self.edit(SERVICE, "resource: https://example.com/acme/pay", "resource: ../../code/pay")
        self.assertIn("links.resource", {item.rule for item in self.findings()})
