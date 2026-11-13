"""Spec versions: designBasedOn, basedOn on Tasks, stories and TestGroups; outdated."""

from wikilib import sync

from . import fixture
from .support import RuleTest
from .test_cli import run

FEATURE = "pay/features/FEAT-pay/overview.md"
CHANGE = "pay/change-requests/CR-1/overview.md"
TODO_TASK = "pay/features/FEAT-pay/TASK-pay-002.md"
DONE_TASK = "pay/features/FEAT-pay/TASK-pay-001.md"
STORY = "pay/features/FEAT-pay/STORY-pay-checkout.md"
GROUP = "pay/tests/TS-pay/STORY-pay-checkout/overview.md"
FEATURE_VERSION = "version: 1\nversionDate: 2026-08-15\ndesignBasedOn: { version: 1, at: 2026-08-15 }"
FEATURE_BASIS = "basedOn: { version: 1, at: 2026-08-15 }"


class BasisTest(RuleTest):
    def new_version(self, design: bool = True) -> None:
        """FEAT-pay is revised before approval and moves to version 2; its design follows only when `design`."""
        basis = "2, at: 2026-09-10" if design else "1, at: 2026-08-15"
        self.edit(FEATURE, "status: InDev", "status: Draft")
        self.edit(FEATURE, FEATURE_VERSION, f"version: 2\nversionDate: 2026-09-10\ndesignBasedOn: {{ version: {basis} }}")

    def outdated_paths(self) -> set[str]:
        return {item.path for item in self.findings() if item.rule == "basis.outdated"}

    def test_fixture_versions_are_clean(self):
        self.assertClean()

    def test_feature_needs_a_version(self):
        self.edit(FEATURE, "version: 1\n", "")
        self.assertRule("frontmatter.missing-field", FEATURE)

    def test_version_counts_from_one(self):
        self.edit(FEATURE, "version: 1\n", "version: 0\n")
        self.assertReported("basis.version", FEATURE)

    def test_written_design_needs_design_based_on(self):
        self.edit(FEATURE, "\ndesignBasedOn: { version: 1, at: 2026-08-15 }", "")
        self.assertRule("basis.design", FEATURE)

    def test_design_based_on_needs_a_written_design(self):
        self.edit(CHANGE, "status: Approved", "status: Proposed")
        text = fixture.read(self.root, CHANGE)
        start = text.index("# Delta")
        end = text.index("# References") if "# References" in text else len(text)
        fixture.write(self.root, CHANGE, text[:start] + "# Delta\n\nNone — pending architecture\n\n" + text[end:])
        self.assertReported("basis.design", CHANGE)

    def test_basis_shape(self):
        self.edit(TODO_TASK, FEATURE_BASIS, "basedOn: { version: one, at: 2026-08-15 }")
        self.assertRule("frontmatter.bad-value", TODO_TASK)

    def test_task_needs_based_on(self):
        self.edit(TODO_TASK, "\n" + FEATURE_BASIS, "")
        self.assertRule("frontmatter.missing-field", TODO_TASK)

    def test_basis_cannot_be_ahead(self):
        self.edit(TODO_TASK, FEATURE_BASIS, "basedOn: { version: 2, at: 2026-08-15 }")
        self.assertRule("basis.ahead", TODO_TASK)

    def test_current_basis_carries_the_version_date(self):
        self.edit(STORY, FEATURE_BASIS, "basedOn: { version: 1, at: 2026-08-16 }")
        self.assertRule("basis.date", STORY)

    def test_approved_target_needs_a_current_design(self):
        self.edit(CHANGE, "version: 1\nversionDate: 2026-08-20", "version: 2\nversionDate: 2026-09-01")
        self.assertReported("basis.approved", CHANGE)

    def test_a_new_version_reports_what_was_written_from_the_old_one(self):
        self.new_version()
        self.assertEqual(self.outdated_paths(), {DONE_TASK, TODO_TASK, STORY, GROUP})
        self.assertEqual({item.severity for item in self.findings() if item.rule == "basis.outdated"}, {"warning"})

    def test_an_old_design_is_outdated(self):
        self.new_version(design=False)
        self.assertIn(FEATURE, self.outdated_paths())

    def test_a_done_task_from_an_older_version_is_outdated_until_checked(self):
        self.new_version()
        self.assertIn(DONE_TASK, self.outdated_paths())
        self.edit(DONE_TASK, FEATURE_BASIS, "basedOn: { version: 2, at: 2026-09-10 }")
        self.assertNotIn(DONE_TASK, self.outdated_paths())

    def test_an_approved_target_has_no_outdated_task(self):
        self.new_version()
        self.edit(FEATURE, "status: Draft", "status: InDev")
        self.assertReported("basis.approved-task", DONE_TASK)
        self.assertReported("basis.approved-task", TODO_TASK)
        self.assertEqual(self.outdated_paths(), {STORY, GROUP})
        for path in (DONE_TASK, TODO_TASK):
            self.edit(path, FEATURE_BASIS, "basedOn: { version: 2, at: 2026-09-10 }")
        self.assertNotIn("basis.approved-task", {item.rule for item in self.findings()})

    def test_outdated_command(self):
        self.assertEqual(
            run("--root", str(self.root), "outdated", "--feature", "FEAT-pay"),
            (0, {"ok": True, "subject": "FEAT-pay", "version": 1, "versionDate": "2026-08-15", "outdated": []}),
        )
        self.new_version()
        code, result = run("--root", str(self.root), "outdated", "--feature", "FEAT-pay")
        self.assertEqual(code, 1)
        self.assertEqual(
            result["outdated"],
            [
                {"path": STORY, "type": "UserStory", "field": "basedOn", "version": 1, "at": "2026-08-15"},
                {"path": DONE_TASK, "type": "Task", "field": "basedOn", "version": 1, "at": "2026-08-15"},
                {"path": TODO_TASK, "type": "Task", "field": "basedOn", "version": 1, "at": "2026-08-15"},
                {"path": GROUP, "type": "TestGroup", "field": "basedOn", "version": 1, "at": "2026-08-15"},
            ],
        )
