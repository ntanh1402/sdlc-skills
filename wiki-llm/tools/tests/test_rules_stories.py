"""User stories: sentence, criteria, trace, Functional, place, Affects; Task # Stories."""

from wikilib import sync

from . import fixture
from .support import RuleTest

STORY = "pay/features/FEAT-pay/STORY-pay-checkout.md"
CHANGE_STORY = "pay/change-requests/CR-1/STORY-pay-coupon.md"
FEATURE = "pay/features/FEAT-pay/overview.md"
TASK = "pay/features/FEAT-pay/TASK-pay-001.md"
CHANGE_TASK = "pay/change-requests/CR-1/TASK-pay-003.md"
CRITERION = (
    "1. **Given** a cart, **when** the shopper pays, **then** the order is placed.\n"
    "   ([REQ-pay-1](overview.md#req-pay-1))"
)
SECOND_REQ = "### REQ-pay-refund\n\n**Should** — A shopper gets a refund. Functional. Verified by test.\n\n# Architecture"


class StoryTest(RuleTest):
    def test_fixture_stories_are_clean(self):
        self.assertClean()

    def test_story_sentence_needs_its_three_parts(self):
        self.edit(STORY, "As a **shopper**, I want to pay for my order, so that it is placed.", "Shoppers pay.")
        self.assertRule("story.sentence", STORY)

    def test_story_sentence_accepts_as_an(self):
        self.edit(STORY, "As a **shopper**", "As an **adult shopper**")
        self.assertClean()

    def test_criteria_must_be_a_numbered_list(self):
        self.edit(STORY, "1. **Given**", "* **Given**")
        self.assertReported("story.criteria", STORY)

    def test_criteria_hold_nothing_but_the_list(self):
        self.edit(STORY, "# Acceptance criteria\n\n", "# Acceptance criteria\n\nThese must hold.\n\n")
        self.assertRule("story.criteria", STORY)

    def test_criterion_needs_given_when_then(self):
        self.edit(STORY, "**when** the shopper pays, ", "")
        self.assertRule("story.criteria", STORY)

    def test_criterion_must_link_a_requirement(self):
        self.edit(STORY, "\n   ([REQ-pay-1](overview.md#req-pay-1))", "")
        found = {(item.rule, item.path) for item in self.findings()}
        self.assertEqual(found, {("story.criteria", STORY), ("story.trace", STORY)})

    def test_criterion_may_continue_after_a_blank_line_item(self):
        self.edit(FEATURE, "# Architecture", SECOND_REQ)
        self.edit(
            STORY,
            CRITERION,
            CRITERION + "\n\n2. Given a paid order, when it is refunded, then the shopper gets the money back.\n"
            "   ([REQ-pay-refund](overview.md#req-pay-refund))",
        )
        self.edit(STORY, "* [REQ-pay-1](overview.md#req-pay-1)", "* [REQ-pay-1](overview.md#req-pay-1)\n* [REQ-pay-refund](overview.md#req-pay-refund)")
        self.assertClean()

    def test_criterion_links_a_requirement_the_story_does_not_list(self):
        self.edit(FEATURE, "# Architecture", SECOND_REQ)
        self.edit(STORY, "([REQ-pay-1](overview.md#req-pay-1))", "([REQ-pay-1](overview.md#req-pay-1), [REQ-pay-refund](overview.md#req-pay-refund))")
        self.assertRule("story.trace", STORY)

    def test_listed_requirement_no_criterion_links(self):
        self.edit(FEATURE, "# Architecture", SECOND_REQ)
        self.edit(STORY, "* [REQ-pay-1](overview.md#req-pay-1)", "* [REQ-pay-1](overview.md#req-pay-1)\n* [REQ-pay-refund](overview.md#req-pay-refund)")
        self.assertRule("story.trace", STORY)

    def test_story_needs_a_functional_requirement(self):
        self.edit(FEATURE, "Functional. Verified by test.", "Nonfunctional. Verified by test.")
        self.assertRule("story.functional", STORY)

    def test_functional_is_not_judged_when_the_type_is_broken(self):
        self.edit(FEATURE, "Functional. Verified by test.", "Verified by test.")
        self.assertRule("content.requirement", FEATURE)

    def test_change_request_story_links_the_change_requests_copy(self):
        self.edit(
            CHANGE_STORY,
            "REQ-pay-2](overview.md#req-pay-2)",
            "REQ-pay-1](../../features/FEAT-pay/overview.md#req-pay-1)",
        )
        self.assertRule("story.requirement-place", CHANGE_STORY)

    def test_feature_story_may_not_link_another_folder(self):
        self.edit(
            STORY,
            "REQ-pay-1](overview.md#req-pay-1)",
            "REQ-pay-2](../../change-requests/CR-1/overview.md#req-pay-2)",
        )
        self.assertRule("story.requirement-place", STORY)

    def test_affects_only_in_a_change_request(self):
        self.write(
            "pay/features/FEAT-pay/STORY-pay-again.md",
            fixture.FILES[STORY].replace("# Requirements", "# Requirements")
            + "\n# Affects\n\n* [STORY-pay-checkout](STORY-pay-checkout.md)\n",
        )
        self.assertRule("story.affects", "pay/features/FEAT-pay/STORY-pay-again.md")

    def test_affects_names_a_story_of_the_changed_feature(self):
        self.write("pay/change-requests/CR-1/STORY-pay-other.md", fixture.FILES[CHANGE_STORY].replace("# Affects\n\n* [STORY-pay-checkout](../../features/FEAT-pay/STORY-pay-checkout.md) — paying now takes a coupon.", ""))
        self.edit(CHANGE_STORY, "../../features/FEAT-pay/STORY-pay-checkout.md", "STORY-pay-other.md")
        self.edit(CHANGE_TASK, "* [STORY-pay-coupon](STORY-pay-coupon.md)", "* [STORY-pay-coupon](STORY-pay-coupon.md)\n* [STORY-pay-other](STORY-pay-other.md)")
        self.assertRule("story.affects", CHANGE_STORY)

    def test_task_links_only_stories_of_its_folder(self):
        self.edit(CHANGE_TASK, "* [STORY-pay-coupon](STORY-pay-coupon.md)", "* [STORY-pay-coupon](STORY-pay-coupon.md)\n* [STORY-pay-checkout](../../features/FEAT-pay/STORY-pay-checkout.md)")
        self.assertRule("task.stories-place", CHANGE_TASK)

    def test_task_stories_link_only_stories(self):
        self.edit(TASK, "* [STORY-pay-checkout](STORY-pay-checkout.md)", "* [TASK-pay-002](TASK-pay-002.md)")
        self.assertReported("relationships.target-type", TASK)

    def test_story_key_carries_the_feature_name(self):
        text = fixture.read(self.root, STORY)
        self.remove(STORY)
        self.write("pay/features/FEAT-pay/STORY-checkout.md", text)
        self.edit(TASK, "STORY-pay-checkout](STORY-pay-checkout.md)", "STORY-checkout](STORY-checkout.md)")
        self.edit(CHANGE_STORY, "[STORY-pay-checkout](../../features/FEAT-pay/STORY-pay-checkout.md)", "[STORY-checkout](../../features/FEAT-pay/STORY-checkout.md)")
        sync.write(self.root)
        self.assertRule("ids.story-format", "pay/features/FEAT-pay/STORY-checkout.md")

    def test_change_request_story_key_carries_the_changed_feature_name(self):
        text = fixture.read(self.root, CHANGE_STORY)
        self.remove(CHANGE_STORY)
        self.write("pay/change-requests/CR-1/STORY-coupon.md", text)
        self.edit(CHANGE_TASK, "STORY-pay-coupon](STORY-pay-coupon.md)", "STORY-coupon](STORY-coupon.md)")
        sync.write(self.root)
        self.assertRule("ids.story-format", "pay/change-requests/CR-1/STORY-coupon.md")

    def test_story_has_no_status(self):
        self.edit(STORY, "priority: P1", "priority: P1\nstatus: Todo")
        self.assertReported("frontmatter.unknown-field", STORY)


class ChangedByTest(RuleTest):
    def test_sync_mirrors_affects_on_the_feature_story(self):
        text = fixture.read(self.root, STORY)
        self.assertIn("# Changed by\n\n* [Pay with a coupon](../../change-requests/CR-1/STORY-pay-coupon.md)\n", text)

    def test_changed_by_is_left_out_when_nothing_affects_the_story(self):
        self.edit(CHANGE_STORY, "\n\n# Affects\n\n* [STORY-pay-checkout](../../features/FEAT-pay/STORY-pay-checkout.md) — paying now takes a coupon.", "")
        sync.write(self.root)
        self.assertNotIn("# Changed by", fixture.read(self.root, STORY))
        self.assertClean()
