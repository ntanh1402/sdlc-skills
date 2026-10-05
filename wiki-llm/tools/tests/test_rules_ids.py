from . import fixture
from .support import RuleTest

FEATURE = "pay/features/FEAT-pay/overview.md"
CHANGE = "pay/change-requests/CR-1/overview.md"
STORY = "pay/features/FEAT-pay/STORY-pay-checkout.md"
CHANGE_STORY = "pay/change-requests/CR-1/STORY-pay-coupon.md"


class IdsTest(RuleTest):
    def rules(self):
        return {item.rule for item in self.findings()}

    def test_task_key_reused_in_another_parent(self):
        self.write("pay/change-requests/CR-1/TASK-pay-001.md", fixture.FILES["pay/features/FEAT-pay/TASK-pay-001.md"])
        self.assertIn("ids.duplicate-key", self.rules())

    def test_reference_filenames_may_repeat_across_owners(self):
        self.write("pay/change-requests/CR-1/prd.md", fixture.FILES["pay/features/FEAT-pay/prd.md"])
        self.assertClean()

    def test_requirement_key_is_the_feature_name_and_a_name(self):
        self.edit(FEATURE, "REQ-pay-1", "REQ-pay-take-payment")
        self.edit(FEATURE, "#req-pay-1", "#req-pay-take-payment")
        fixture.edit(self.root, "pay/tests/TS-pay/TC-pay-ok.md", "REQ-pay-1](../../features/FEAT-pay/overview.md#req-pay-1)",
                     "REQ-pay-take-payment](../../features/FEAT-pay/overview.md#req-pay-take-payment)")
        fixture.edit(self.root, "pay/features/FEAT-pay/TASK-pay-001.md", "[REQ-pay-1](overview.md#req-pay-1)",
                     "[REQ-pay-take-payment](overview.md#req-pay-take-payment)")
        self.edit(STORY, "REQ-pay-1](overview.md#req-pay-1)", "REQ-pay-take-payment](overview.md#req-pay-take-payment)")
        self.assertClean()

    def test_requirement_name_must_be_lower_case_words(self):
        self.edit(FEATURE, "### REQ-pay-1", "### REQ-pay-Take_Payment")
        self.assertIn("ids.requirement-format", self.rules())

    def test_requirement_id_must_carry_the_feature_slug(self):
        self.edit(FEATURE, "### REQ-pay-1", "### REQ-1")
        self.assertIn("ids.requirement-format", self.rules())

    def test_requirement_id_of_another_feature_is_rejected(self):
        self.edit(FEATURE, "### REQ-pay-1", "### REQ-cart-1")
        self.assertIn("ids.requirement-format", self.rules())

    def test_change_request_requirement_uses_the_changed_feature_slug(self):
        self.edit(CHANGE, "### REQ-pay-2", "### REQ-coupons-1")
        self.assertIn("ids.requirement-format", self.rules())

    def test_change_request_may_reuse_a_feature_requirement_id(self):
        self.edit(CHANGE, "REQ-pay-2", "REQ-pay-1")
        self.edit(CHANGE, "#req-pay-2", "#req-pay-1")
        self.edit(CHANGE_STORY, "REQ-pay-2](overview.md#req-pay-2)", "REQ-pay-1](overview.md#req-pay-1)")
        self.assertClean()

    def test_duplicate_requirement_id_in_one_file(self):
        self.edit(
            FEATURE,
            "# Architecture",
            "### REQ-pay-1\n\n**Must** — A second thing. Functional. Verified by test.\n\n# Architecture",
        )
        self.assertRule("ids.requirement-duplicate", FEATURE)


class RequirementCollisionTest(RuleTest):
    SECOND = "pay/change-requests/CR-gift-cards/overview.md"

    def add_second_change(self, status="Approved", requirement="REQ-pay-2"):
        text = fixture.FILES[CHANGE].replace("status: Approved", f"status: {status}")
        text = text.replace("Accept coupons", "Accept gift cards").replace("REQ-pay-2", requirement)
        text = text.replace("#req-pay-2", "#" + requirement.lower())
        self.write(self.SECOND, text)
        self.write("pay/change-requests/CR-gift-cards/log.md", fixture.LOG)

    def collisions(self):
        return [(item.path, item.message) for item in self.findings() if item.rule == "ids.requirement-collision"]

    def test_two_open_changes_adding_the_same_requirement(self):
        self.add_second_change()
        found = self.collisions()
        self.assertEqual({path for path, _ in found}, {CHANGE, self.SECOND})
        self.assertIn("REQ-pay-2", found[0][1])
        self.assertIn("rename", found[0][1])

    def test_two_open_changes_modifying_a_feature_requirement(self):
        self.edit(CHANGE, "REQ-pay-2", "REQ-pay-1")
        self.edit(CHANGE, "#req-pay-2", "#req-pay-1")
        self.add_second_change(requirement="REQ-pay-1")
        self.assertEqual(self.collisions(), [])

    def test_a_closed_change_does_not_collide(self):
        for status in ("Implemented", "Rejected"):
            self.add_second_change(status=status)
            self.assertEqual(self.collisions(), [], status)

    def test_undesigned_changes_collide_too(self):
        for status in ("Proposed", "ReqApproved"):
            self.add_second_change(status=status)
            self.assertEqual({path for path, _ in self.collisions()}, {CHANGE, self.SECOND}, status)

    def test_different_new_requirements_do_not_collide(self):
        self.add_second_change(requirement="REQ-pay-gift-card")
        self.assertEqual(self.collisions(), [])
