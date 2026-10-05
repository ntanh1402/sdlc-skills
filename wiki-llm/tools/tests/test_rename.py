"""rename: a concept or Requirement and every reference to it, refused once merged."""

import re
import tempfile
import unittest
from pathlib import Path

from wikilib import validate

from . import fixture
from .gitrepo import GitTest, commit_all, git
from .test_cli import run

CHANGE = "pay/change-requests/CR-1/overview.md"
FEATURE = "pay/features/FEAT-pay/overview.md"
ADR = fixture.page(
    f"type: ArchitectureDecision\ntitle: Charge later\ndescription: Charge on capture.\n"
    f"status: Accepted\nownerTeam: payments\ndecisionDate: 2026-09-20\n{fixture.G}",
    "# Charge later\n\n# Context\n\nText.\n\n# Decision\n\nText.\n\n# Alternatives\n\nText.\n\n"
    "# Consequences\n\nText.\n\n# Affected concepts\n\n* [SVC-pay](../services/SVC-pay/overview.md)",
)


def problems(root: Path) -> list[tuple[str, str]]:
    return [(item.rule, item.path) for item in validate.run(root) if item.severity == "error"]


def mentions(root: Path, key: str) -> list[str]:
    pattern = re.compile(rf"(?<![A-Za-z0-9_-]){re.escape(key)}(?![A-Za-z0-9_-])", re.IGNORECASE)
    return sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*.md")
        if pattern.search(path.read_text(encoding="utf-8"))
    )


class RenameConceptTest(GitTest):
    def rename(self, *argv):
        return run("--root", str(self.root), "rename", *argv)

    def add_decision(self):
        fixture.write(self.root, "pay/decisions/ADR-charge-later.md", ADR)
        fixture.edit(self.root, FEATURE, "* [ADR-002](../../decisions/ADR-002.md)",
                     "* [ADR-002](../../decisions/ADR-002.md)\n* [ADR-charge-later](../../decisions/ADR-charge-later.md)")

    def test_key_on_the_default_branch_is_refused(self):
        code, result = self.rename("CR-1", "CR-coupons")
        self.assertEqual(code, 1)
        self.assertIn("CR-1 is on main", result["error"])
        self.assertTrue((self.root / "pay/change-requests/CR-1").is_dir())

    def test_allow_merged_moves_the_folder_and_rewrites_every_reference(self):
        code, result = self.rename("CR-1", "CR-coupons", "--allow-merged")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["moved"], {"from": "pay/change-requests/CR-1", "to": "pay/change-requests/CR-coupons"})
        self.assertIn("pay/services/SVC-pay/EP-pay-create.md", result["rewritten"])
        self.assertEqual(mentions(self.root, "CR-1"), [])
        self.assertEqual(problems(self.root), [])

    def test_new_concept_in_a_draft_is_renamed(self):
        self.add_decision()
        code, result = self.rename("ADR-charge-later", "ADR-charge-on-capture")
        self.assertEqual(code, 0, result)
        self.assertIn("[ADR-charge-on-capture](../../decisions/ADR-charge-on-capture.md)", fixture.read(self.root, FEATURE))
        self.assertTrue((self.root / "pay/decisions/ADR-charge-on-capture.md").is_file())
        self.assertEqual(problems(self.root), [])

    def test_new_key_already_in_the_bundle_is_refused(self):
        self.add_decision()
        code, result = self.rename("ADR-charge-later", "ADR-002")
        self.assertEqual(code, 1)
        self.assertIn("already exists", result["error"])

    def test_new_key_only_on_the_default_branch_is_refused(self):
        fixture.write(self.root, "pay/decisions/ADR-charge-later.md", ADR)
        commit_all(self.repo, "add a decision")
        git(self.repo, "switch", "-q", "-c", "wiki/other", "HEAD~1")
        self.assertFalse((self.root / "pay/decisions/ADR-charge-later.md").exists())
        fixture.write(self.root, "pay/decisions/ADR-charge-sooner.md", ADR)
        code, result = self.rename("ADR-charge-sooner", "ADR-charge-later", "--allow-merged")
        self.assertEqual(code, 1)
        self.assertIn("already exists in this draft or on main", result["error"])

    def test_new_key_must_fit_the_type(self):
        for new in ("CR-Coupons", "ADR-coupons"):
            code, result = self.rename("CR-1", new, "--allow-merged")
            self.assertEqual(code, 1, new)
            self.assertIn("is not a ChangeRequest key", result["error"])

    def test_unknown_key(self):
        code, result = self.rename("CR-nothing", "CR-something")
        self.assertEqual((code, result["error"]), (1, "no concept or requirement has the key CR-nothing"))

    def test_fixed_keys_cannot_be_renamed(self):
        code, result = self.rename("pay", "payments", "--allow-merged")
        self.assertEqual(code, 1)
        self.assertIn("fixed key", result["error"])


class RenameRequirementTest(GitTest):
    def rename(self, *argv):
        return run("--root", str(self.root), "rename", *argv)

    def test_requirement_on_the_default_branch_is_refused(self):
        code, result = self.rename("REQ-pay-1", "REQ-pay-take-payment")
        self.assertEqual(code, 1)
        self.assertIn("REQ-pay-1 is on main", result["error"])

    def test_headings_anchors_and_mentions_are_rewritten(self):
        code, result = self.rename("REQ-pay-1", "REQ-pay-take-payment", "--allow-merged")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["kind"], "requirement")
        self.assertIn("### REQ-pay-take-payment", fixture.read(self.root, FEATURE))
        self.assertIn(
            "[REQ-pay-take-payment](../../features/FEAT-pay/overview.md#req-pay-take-payment)",
            fixture.read(self.root, "pay/tests/TS-pay/TC-pay-ok.md"),
        )
        self.assertEqual(mentions(self.root, "REQ-pay-1"), [])
        self.assertEqual(problems(self.root), [])

    def test_new_name_must_belong_to_the_feature(self):
        code, result = self.rename("REQ-pay-1", "REQ-cart-take-payment", "--allow-merged")
        self.assertEqual(code, 1)
        self.assertIn("must be REQ-pay-<name>", result["error"])

    def test_change_option_renames_inside_one_change_request(self):
        second = "pay/change-requests/CR-gift-cards/overview.md"
        fixture.write(self.root, second, fixture.FILES[CHANGE].replace("Accept coupons", "Accept gift cards"))
        fixture.write(self.root, "pay/change-requests/CR-gift-cards/log.md", fixture.LOG)
        self.assertIn(("ids.requirement-collision", second), problems(self.root))
        code, result = self.rename("REQ-pay-2", "REQ-pay-gift-card", "--change", "CR-gift-cards")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["rewritten"], [second])
        self.assertIn("### REQ-pay-2", fixture.read(self.root, CHANGE))
        self.assertIn("### REQ-pay-gift-card", fixture.read(self.root, second))
        self.assertIn("(#req-pay-gift-card)", fixture.read(self.root, second))
        self.assertNotIn("ids.requirement-collision", {rule for rule, _ in problems(self.root)})


class RenameOutsideGitTest(unittest.TestCase):
    def test_a_bundle_outside_git_has_no_merged_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture.make_bundle(Path(tmp) / "bundle")
            code, result = run("--root", str(root), "rename", "CR-1", "CR-coupons")
            self.assertEqual(code, 0, result)
            self.assertEqual(problems(root), [])


if __name__ == "__main__":
    unittest.main()
