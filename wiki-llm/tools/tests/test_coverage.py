"""coverage: what a Feature or ChangeRequest has no TestCase or Task for."""

import contextlib
import io

from .support import RuleTest
from .test_cli import run

TESTCASE = "pay/tests/TS-pay/TC-pay-ok.md"
COVERS_REQ = "* [REQ-pay-1](../../features/FEAT-pay/overview.md#req-pay-1)\n"
FEATURE = "pay/features/FEAT-pay/overview.md"
SECOND_REQ = "### REQ-pay-refund\n\n**Should** — A shopper gets a refund. Functional. Verified by test.\n\n# Architecture"


class CoverageTest(RuleTest):
    def coverage(self, *argv):
        return run("--root", str(self.root), "coverage", *argv)

    def test_feature_requirements_covered_by_a_test_case(self):
        self.assertEqual(self.coverage("tests", "--feature", "FEAT-pay"), (0, {"ok": True, "subject": "FEAT-pay", "uncovered": []}))

    def test_feature_requirement_without_a_test_case(self):
        self.edit(TESTCASE, COVERS_REQ, "")
        self.assertEqual(self.coverage("tests", "--feature", "FEAT-pay"), (1, {"ok": False, "subject": "FEAT-pay", "uncovered": ["REQ-pay-1"]}))

    def test_change_requirements_without_a_test_case(self):
        self.assertEqual(self.coverage("tests", "--change", "CR-1")[1]["uncovered"], ["REQ-pay-2"])

    def test_change_requirement_covered_through_the_change_request(self):
        self.edit(TESTCASE, COVERS_REQ, COVERS_REQ + "* [REQ-pay-2](../../change-requests/CR-1/overview.md#req-pay-2)\n")
        self.assertEqual(self.coverage("tests", "--change", "CR-1")[1]["uncovered"], [])

    def test_modified_requirement_covered_through_the_feature(self):
        self.edit("pay/change-requests/CR-1/overview.md", "REQ-pay-2", "REQ-pay-1")
        self.edit("pay/change-requests/CR-1/overview.md", "#req-pay-2", "#req-pay-1")
        self.assertEqual(self.coverage("tests", "--change", "CR-1")[1]["uncovered"], [])

    def test_feature_counts_only_concepts_pending_for_it(self):
        # SVC-pay, WEB-shop and MB-shop are reused unchanged; EP-pay-create is pending for CR-1 only.
        self.assertEqual(self.coverage("tasks", "--feature", "FEAT-pay"), (0, {"ok": True, "subject": "FEAT-pay", "uncovered": []}))

    def test_feature_pending_concept_without_a_task(self):
        self.remove("pay/features/FEAT-pay/TASK-pay-002.md")
        self.assertEqual(
            self.coverage("tasks", "--feature", "FEAT-pay"),
            (1, {"ok": False, "subject": "FEAT-pay", "uncovered": ["pay/services/SVC-pay/EP-pay-refund.md"]}),
        )

    def test_change_delta_covered_by_its_tasks(self):
        self.assertEqual(self.coverage("tasks", "--change", "CR-1"), (0, {"ok": True, "subject": "CR-1", "uncovered": []}))

    def test_change_delta_without_a_task(self):
        self.remove("pay/change-requests/CR-1/TASK-pay-003.md")
        self.assertEqual(
            self.coverage("tasks", "--change", "CR-1")[1]["uncovered"],
            ["pay/services/SVC-pay/EP-pay-create.md", "pay/change-requests/CR-1/STORY-pay-coupon.md"],
        )

    def test_feature_story_without_a_task(self):
        self.edit("pay/features/FEAT-pay/TASK-pay-001.md", "# Stories\n\n* [STORY-pay-checkout](STORY-pay-checkout.md)\n\n", "")
        self.assertEqual(self.coverage("tasks", "--feature", "FEAT-pay")[1]["uncovered"], ["pay/features/FEAT-pay/STORY-pay-checkout.md"])

    def test_feature_requirements_listed_by_stories(self):
        self.assertEqual(self.coverage("stories", "--feature", "FEAT-pay"), (0, {"ok": True, "subject": "FEAT-pay", "uncovered": []}))

    def test_feature_requirement_without_a_story(self):
        self.edit(FEATURE, "# Architecture", SECOND_REQ)
        self.assertEqual(self.coverage("stories", "--feature", "FEAT-pay"), (1, {"ok": False, "subject": "FEAT-pay", "uncovered": ["REQ-pay-refund"]}))

    def test_nonfunctional_and_wont_requirements_need_no_story(self):
        self.edit(FEATURE, "# Architecture", SECOND_REQ.replace("Functional.", "Nonfunctional.").replace("REQ-pay-refund", "REQ-pay-fast"))
        self.edit(FEATURE, "# Architecture", SECOND_REQ.replace("**Should**", "**Wont**"))
        self.assertEqual(self.coverage("stories", "--feature", "FEAT-pay")[1]["uncovered"], [])

    def test_change_requirement_without_a_story(self):
        self.remove("pay/change-requests/CR-1/STORY-pay-coupon.md")
        self.assertEqual(self.coverage("stories", "--change", "CR-1")[1]["uncovered"], ["REQ-pay-2"])

    def test_feature_requirement_listed_by_a_change_request_story(self):
        # Once the ChangeRequest is applied, the Feature holds REQ-pay-2; its story stays in the ChangeRequest.
        self.edit(FEATURE, "# Architecture", "### REQ-pay-2\n\n**Should** — A shopper applies one coupon. Functional. Verified by test.\n\n# Architecture")
        self.assertEqual(self.coverage("stories", "--feature", "FEAT-pay")[1]["uncovered"], [])

    def test_unknown_subject(self):
        code, result = self.coverage("tests", "--feature", "FEAT-nothing")
        self.assertEqual(code, 2)
        self.assertEqual(result["error"], "no Feature has the key FEAT-nothing")

    def test_a_subject_is_required(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            self.coverage("tests")
