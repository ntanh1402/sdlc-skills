"""TestSuites: case ids, story groups and their criteria, steps without wiki keys,
bold validations, open questions."""

from wikilib import sync

from . import fixture
from .support import RuleTest

SUITE = "pay/tests/TS-pay/overview.md"
GROUP = "pay/tests/TS-pay/STORY-pay-checkout/overview.md"
CASE = "pay/tests/TS-pay/STORY-pay-checkout/TC-1-pay-ok.md"
STORY = "pay/features/FEAT-pay/STORY-pay-checkout.md"
STEP = "| 1 | Pay | Paid | Row **status** |"


class TestSuiteRulesTest(RuleTest):
    def copy_case(self, rel: str) -> None:
        text = (self.root / CASE).read_text(encoding="utf-8")
        self.write(rel, fixture.general_case(text) if "/GENERAL/" in rel else text)
        sync.write(self.root)

    def severities(self) -> dict[str, set[str]]:
        found: dict[str, set[str]] = {}
        for item in self.findings():
            found.setdefault(item.rule, set()).add(item.severity)
        return found

    def test_case_ids_are_unique_in_the_suite(self):
        fixture.add_general(self.root)
        self.copy_case("pay/tests/TS-pay/GENERAL/TC-1-pay-again.md")
        self.assertRule("tests.case-id", CASE)
        self.remove("pay/tests/TS-pay/GENERAL/TC-1-pay-again.md")
        self.copy_case("pay/tests/TS-pay/GENERAL/TC-2-pay-again.md")
        self.assertClean()

    def test_case_key_carries_an_id(self):
        self.copy_case("pay/tests/TS-pay/STORY-pay-checkout/TC-pay-ok.md")
        self.remove(CASE)
        self.assertIn("layout.key", {item.rule for item in self.findings()})

    def test_case_outside_a_group_folder(self):
        self.copy_case("pay/tests/TS-pay/TC-2-pay-ok.md")
        self.assertReported("layout.unknown-path", "pay/tests/TS-pay/TC-2-pay-ok.md")

    def test_group_needs_an_overview(self):
        self.write("pay/tests/TS-pay/GENERAL/TC-2-pay-ok.md", fixture.read(self.root, CASE))
        self.assertReported("layout.missing-file", "pay/tests/TS-pay/GENERAL/overview.md")

    def test_story_folder_names_a_story_of_the_target_as_a_warning(self):
        self.edit(GROUP, "STORY-pay-checkout.md", "STORY-pay-refund.md")
        (self.root / "pay/tests/TS-pay/STORY-pay-checkout").rename(self.root / "pay/tests/TS-pay/STORY-pay-refund")
        sync.write(self.root)
        found = self.severities()
        self.assertEqual(found["tests.story-folder"], {"warning"})
        self.assertEqual(found["links.unresolved"], {"warning"})  # the deleted story's links

    def test_story_group_links_its_story(self):
        self.edit(GROUP, "\n\n# Story\n\n* [STORY-pay-checkout](../../../features/FEAT-pay/STORY-pay-checkout.md)", "")
        self.assertRule("tests.group-story", GROUP)

    def test_general_group_has_no_story(self):
        fixture.add_general(self.root)
        self.edit("pay/tests/TS-pay/GENERAL/overview.md", "# Scope", "# Story\n\n* [STORY-pay-checkout](../../../features/FEAT-pay/STORY-pay-checkout.md)\n\n# Scope")
        self.assertRule("tests.group-story", "pay/tests/TS-pay/GENERAL/overview.md")

    def test_general_group_says_its_scope(self):
        fixture.add_general(self.root)
        self.edit("pay/tests/TS-pay/GENERAL/overview.md", "\n\n# Scope\n\nPaying end to end.", "")
        self.assertRule("tests.group-scope", "pay/tests/TS-pay/GENERAL/overview.md")

    def test_suite_has_no_log(self):
        self.write("pay/tests/TS-pay/log.md", fixture.LOG)
        self.assertRule("tests.suite-log", SUITE)

    def test_broken_link_to_another_story_is_an_error(self):
        self.edit(CASE, "— AC 1\n", "— AC 1\n* [STORY-pay-chekout](../../../features/FEAT-pay/STORY-pay-chekout.md)\n")
        self.assertEqual(self.severities()["links.unresolved"], {"error"})  # a typo, not the group's removed story

    def test_story_case_names_the_criteria_it_proves(self):
        self.edit(CASE, " — AC 1", "")
        self.assertRule("tests.story-ac", CASE)
        self.assertEqual(self.severities()["tests.story-ac"], {"error", "warning"})  # and AC 1 is now uncovered

    def test_criterion_that_does_not_exist_is_a_warning(self):
        self.edit(CASE, "— AC 1", "— AC 1, 4")
        self.assertRule("tests.story-ac", CASE)
        self.assertEqual(self.severities()["tests.story-ac"], {"warning"})

    def test_criterion_no_case_proves_is_a_warning(self):
        self.edit(STORY, "   ([REQ-pay-1](overview.md#req-pay-1))", "   ([REQ-pay-1](overview.md#req-pay-1))\n2. A paid order cannot be paid again.\n   ([REQ-pay-1](overview.md#req-pay-1))")
        self.assertRule("tests.story-ac", GROUP)
        self.assertEqual(self.severities()["tests.story-ac"], {"warning"})

    def test_general_case_links_no_story(self):
        self.remove("pay/tests/TS-pay/STORY-pay-checkout")
        fixture.add_general(self.root)
        self.write("pay/tests/TS-pay/GENERAL/TC-1-pay-ok.md", fixture.FILES[CASE])
        sync.write(self.root)
        self.assertRule("tests.general-story", "pay/tests/TS-pay/GENERAL/TC-1-pay-ok.md")

    def test_story_case_covers_a_requirement_of_its_story(self):
        self.edit(CASE, "* [REQ-pay-1](../../../features/FEAT-pay/overview.md#req-pay-1)\n", "")
        self.assertRule("tests.story-covers", CASE)
        self.assertEqual(self.severities()["tests.story-covers"], {"warning"})

    def test_steps_use_real_names_not_wiki_keys(self):
        self.edit(CASE, STEP, "| 1 | Pay | Paid | Row **status** in TBL-payments |")
        self.assertRule("tests.step-names", CASE)

    def test_steps_do_not_point_at_other_steps(self):
        self.edit(CASE, STEP, "| 1 | Pay. Request: see Step 1 | Paid | Row **status** |")
        self.assertRule("tests.step-names", CASE)

    def test_validation_names_what_it_checks_in_bold(self):
        self.edit(CASE, STEP, "| 1 | Pay | Paid | Row status |")
        self.assertRule("tests.validation-bold", CASE)

    def test_open_questions_keep_the_group_in_draft(self):
        question = "\n\n# Open questions\n\n1. Is a zero amount allowed? ([REQ-pay-1](../../../features/FEAT-pay/overview.md#req-pay-1))"
        self.edit(GROUP, "STORY-pay-checkout.md)", "STORY-pay-checkout.md)" + question)
        self.assertRule("tests.open-questions", GROUP)
        self.edit(GROUP, "status: Approved", "status: Draft")
        self.assertClean()

    def test_deprecated_group_has_no_open_questions(self):
        question = "\n\n# Open questions\n\n1. Is a zero amount allowed? ([REQ-pay-1](../../../features/FEAT-pay/overview.md#req-pay-1))"
        self.edit(GROUP, "STORY-pay-checkout.md)", "STORY-pay-checkout.md)" + question)
        self.edit(GROUP, "status: Approved", "status: Deprecated")
        self.assertRule("tests.open-questions", GROUP)

    def test_open_question_links_what_it_is_about(self):
        self.edit(GROUP, "status: Approved", "status: Draft")
        self.edit(GROUP, "STORY-pay-checkout.md)", "STORY-pay-checkout.md)\n\n# Open questions\n\n1. Is a zero amount allowed?")
        self.assertRule("tests.open-questions", GROUP)

    def test_suite_verifies_one_target(self):
        self.edit(SUITE, "* [FEAT-pay](../../features/FEAT-pay/overview.md)", "* [FEAT-pay](../../features/FEAT-pay/overview.md)\n* [CR-1](../../change-requests/CR-1/overview.md)")
        self.assertIn("relationships.cardinality", {item.rule for item in self.findings()})

    def test_checklist_shows_group_category_and_criteria(self):
        fixture.add_general(self.root)
        self.write("pay/tests/TS-pay/GENERAL/TC-2-pay-flow.md", fixture.general_case(fixture.FILES[CASE]).replace("testCategory: functional\n", ""))
        sync.write(self.root)
        rows = fixture.read(self.root, "pay/tests/TS-pay/checklist.csv").splitlines()
        self.assertEqual(rows[0], "No,Group,Title,Description,Category,Covers,Purpose")
        self.assertIn("1,STORY-pay-checkout,Payment succeeds,A valid payment is taken.,functional,AC 1,Prove a payment works.", rows)
        self.assertIn("2,GENERAL,Payment succeeds,A valid payment is taken.,,,Prove a payment works.", rows)
