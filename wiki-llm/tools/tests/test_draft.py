"""Drafts: a branch wiki/<key> in a worktree .worktrees/<key>/, written,
finished, shown, committed and pushed by the tool."""

import contextlib
import unittest

from wikilib import frontmatter

from . import fixture
from .gitrepo import GitTest, commit_all, git
from .test_cli import run

TABLE = "pay/datastores/DB-main/TBL-payments.md"
TABLE_LOG = "pay/datastores/DB-main/log.md"
FEATURE = "pay/features/FEAT-pay/overview.md"
ACTOR = "sdlc-test/model-1"
NEW_ENTRY = "* **Update**: Added a column.\n"


class DraftTest(GitTest):
    def tool(self, *argv, cwd=None):
        with contextlib.chdir(cwd or self.repo):
            return run(*argv)

    def start(self, key="coupons"):
        code, result = self.tool("draft", "start", key)
        self.assertEqual(code, 0, result)
        return self.repo / result["worktree"]

    def bundle(self, worktree):
        return worktree / "wiki"

    def edit_table(self, worktree, row="| `amount` | integer | yes | cents |", log=True):
        root = self.bundle(worktree)
        fixture.edit(root, TABLE, "| `id` | uuid | yes | key |", "| `id` | uuid | yes | key |\n" + row)
        if log:
            fixture.edit(root, TABLE_LOG, "## 2026-09-01\n", "## 2026-09-30\n\n" + NEW_ENTRY + "\n## 2026-09-01\n")

    def finish(self, worktree, *extra):
        return self.tool("draft", "finish", "--by", ACTOR, *extra, cwd=worktree)

    def meta(self, worktree, rel):
        return frontmatter.parse(fixture.read(self.bundle(worktree), rel))[0]


class StartTest(DraftTest):
    def test_start_creates_a_branch_and_a_worktree(self):
        code, result = self.tool("draft", "start", "coupons")
        self.assertEqual((code, result), (0, {"ok": True, "branch": "wiki/coupons", "worktree": ".worktrees/coupons", "base": "main"}))
        self.assertTrue((self.repo / ".worktrees/coupons/wiki/index.md").is_file())
        self.assertEqual(git(self.repo / ".worktrees/coupons", "branch", "--show-current"), "wiki/coupons")

    def test_start_refuses_an_existing_branch(self):
        self.start()
        git(self.repo, "worktree", "remove", ".worktrees/coupons")
        code, result = self.tool("draft", "start", "coupons")
        self.assertEqual(code, 1)
        self.assertIn("use draft resume", result["error"])

    def test_start_refuses_a_branch_that_exists_only_on_the_remote(self):
        self.add_remote()
        other = self.clone("bob")
        git(other, "switch", "-q", "-c", "wiki/coupons")
        git(other, "push", "-q", "origin", "wiki/coupons")
        code, result = self.tool("draft", "start", "coupons")
        self.assertEqual(code, 1)
        self.assertIn("use draft resume", result["error"])

    def test_branch_option_names_another_branch(self):
        code, result = self.tool("draft", "start", "coupons", "--branch", "wiki/coupons-2")
        self.assertEqual((code, result["branch"]), (0, "wiki/coupons-2"))

    def test_outside_a_git_repository(self):
        outside = self.tmp / "plain"
        outside.mkdir()
        code, result = self.tool("draft", "start", "x", cwd=outside)
        self.assertEqual(code, 2)
        self.assertIn("not a git repository", result["error"])

    def test_commands_inside_a_worktree_act_on_its_bundle(self):
        worktree = self.start()
        fixture.edit(self.bundle(worktree), TABLE, "status: Active", "status: Gone")
        self.assertEqual(self.tool("validate", cwd=worktree / "wiki" / "pay")[0], 1)
        self.assertEqual(self.tool("validate")[0], 0)


class FinishTest(DraftTest):
    def test_finish_stamps_authored_changes_only(self):
        worktree = self.start()
        self.edit_table(worktree)
        code, result = self.finish(worktree)
        self.assertEqual(code, 0, result)
        self.assertTrue(result["ok"])
        self.assertEqual(result["stamped"], [TABLE])
        self.assertEqual(result["missing_logs"], [])
        self.assertEqual(self.meta(worktree, TABLE)["generated"]["by"], ACTOR)
        self.assertEqual(self.meta(worktree, "pay/services/SVC-pay/overview.md")["generated"]["by"], "human:alice")

    def test_change_confined_to_generated_sections_is_not_stamped(self):
        worktree = self.start()
        root = self.bundle(worktree)
        fixture.edit(root, "pay/services/SVC-pay/overview.md", "# Writes\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md)\n\n", "")
        fixture.edit(root, "pay/services/SVC-pay/log.md", "## 2026-09-01\n", "## 2026-09-30\n\n* **Update**: Stopped writing.\n\n## 2026-09-01\n")
        self.assertEqual(self.tool("sync", cwd=worktree)[1]["written"], [TABLE])
        code, result = self.finish(worktree)
        self.assertEqual(code, 0, result)
        self.assertEqual(result["stamped"], ["pay/services/SVC-pay/overview.md"])
        self.assertEqual(result["missing_logs"], [])
        self.assertEqual(self.meta(worktree, TABLE)["generated"]["by"], "human:alice")

    def test_content_file_change_stamps_its_reference_and_needs_its_log(self):
        worktree = self.start()
        root = self.bundle(worktree)
        fixture.edit(root, "pay/references/REF-pay-prd/prd.md", "Shoppers pay for orders.", "Shoppers pay for orders in one step.")
        fixture.write(root, "pay/references/REF-pay-prd/images/flow.png", "a new picture\n")
        code, result = self.finish(worktree, "--verified-by", "human:bob")
        self.assertEqual((code, result["missing_logs"]), (1, ["pay/references/REF-pay-prd/log.md"]), result)
        fixture.edit(root, "pay/references/REF-pay-prd/log.md", "## 2026-09-01\n", "## 2026-09-30\n\n* **Update**: PRD wording.\n\n## 2026-09-01\n")
        code, result = self.finish(worktree, "--verified-by", "human:bob")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["stamped"], ["pay/references/REF-pay-prd/overview.md"])
        self.assertEqual(self.meta(worktree, "pay/references/REF-pay-prd/overview.md")["verified"]["by"], "human:bob")

    def test_references_edit_is_not_stamped_and_needs_no_log(self):
        worktree = self.start()
        root = self.bundle(worktree)
        fixture.edit(root, "pay/features/FEAT-pay/TASK-pay-002.md", "the refund rules.", "the refund rules and their limits.")
        code, result = self.finish(worktree)
        self.assertEqual(code, 0, result)
        self.assertEqual((result["stamped"], result["missing_logs"]), ([], []))

    def test_missing_log_entry_is_reported(self):
        worktree = self.start()
        self.edit_table(worktree, log=False)
        code, result = self.finish(worktree)
        self.assertEqual(code, 1)
        self.assertFalse(result["ok"])
        self.assertEqual(result["missing_logs"], [TABLE_LOG])

    def test_verified_from_before_the_draft_is_removed(self):
        fixture.edit(self.root, TABLE, fixture.G, fixture.G + "\n" + fixture.V)
        commit_all(self.repo, "verify the table")
        worktree = self.start()
        self.edit_table(worktree)
        self.finish(worktree)
        self.assertNotIn("verified", self.meta(worktree, TABLE))

    def test_verified_set_within_the_draft_is_kept(self):
        worktree = self.start()
        self.assertEqual(self.tool("verify", f"wiki/{TABLE}", cwd=worktree)[0], 0)
        self.edit_table(worktree)
        self.finish(worktree)
        self.assertEqual(self.meta(worktree, TABLE)["verified"]["by"], "human:alice")

    def test_verified_set_on_a_new_file_within_the_draft_is_kept(self):
        worktree = self.start()
        root = self.bundle(worktree)
        fixture.write(root, "pay/decisions/ADR-charge-later.md", fixture.FILES["pay/decisions/ADR-002.md"]
                      .replace("Charge through the bank operation", "Charge later").replace("\n# Supersedes\n\n* [ADR-001](ADR-001.md)", ""))
        self.assertEqual(self.tool("verify", "wiki/pay/decisions/ADR-charge-later.md", cwd=worktree)[0], 0)
        code, result = self.finish(worktree)
        self.assertEqual(code, 0, result)
        self.assertEqual(self.meta(worktree, "pay/decisions/ADR-charge-later.md")["verified"]["by"], "human:alice")

    def test_verified_by_stamps_a_human(self):
        worktree = self.start()
        self.edit_table(worktree)
        self.finish(worktree, "--verified-by", "human:bob")
        self.assertEqual(self.meta(worktree, TABLE)["verified"]["by"], "human:bob")

    def test_verified_by_without_a_value_takes_the_git_email(self):
        worktree = self.start()
        self.edit_table(worktree)
        code, result = self.finish(worktree, "--verified-by")
        self.assertEqual(code, 0, result)
        self.assertEqual(self.meta(worktree, TABLE)["verified"]["by"], "human:alice")

    def test_verified_by_without_a_value_needs_a_git_email(self):
        worktree = self.start()
        self.edit_table(worktree)
        git(worktree, "config", "user.email", "")
        code, result = self.finish(worktree, "--verified-by")
        self.assertEqual(code, 2)
        self.assertIn("user.email", result["error"])
        self.assertNotIn("generated: { by: sdlc-test", fixture.read(self.bundle(worktree), TABLE))

    def test_deleted_concept_folder_needs_no_log_entry(self):
        worktree = self.start()
        root = self.bundle(worktree)
        fixture.edit(root, "pay/services/SVC-pay/overview.md", "* [IDX-payments](../../datastores/IDX-payments/overview.md) — read — search.\n", "")
        fixture.edit(root, "pay/services/SVC-pay/log.md", "## 2026-09-01\n", "## 2026-09-30\n\n* **Update**: Dropped search.\n\n## 2026-09-01\n")
        for name in ("overview.md", "log.md", "index.md"):
            (root / "pay/datastores/IDX-payments" / name).unlink()
        (root / "pay/datastores/IDX-payments").rmdir()
        code, result = self.finish(worktree)
        self.assertEqual((code, result["missing_logs"]), (0, []), result)

    def test_finish_reports_validation_errors(self):
        worktree = self.start()
        self.edit_table(worktree)
        fixture.edit(self.bundle(worktree), TABLE, "status: Active", "status: Gone")
        code, result = self.finish(worktree)
        self.assertEqual(code, 1)
        self.assertEqual([item["rule"] for item in result["validate"]["errors"]], ["frontmatter.bad-value"])

    def test_actor_must_be_an_actor(self):
        worktree = self.start()
        code, result = self.tool("draft", "finish", "--by", "someone", cwd=worktree)
        self.assertEqual(code, 2)
        self.assertIn("--by", result["error"])

    def test_finish_runs_only_inside_a_worktree(self):
        code, result = self.finish(self.repo)
        self.assertEqual(code, 2)
        self.assertIn("draft worktree", result["error"])


class UnverifiedTest(DraftTest):
    """finish --verified-by confirms every changed file except those --unverified names."""

    CHANNEL = "pay/channels/CHAN-pay-events/overview.md"
    CHANNEL_LOG = "pay/channels/CHAN-pay-events/log.md"

    def two_changes(self):
        worktree = self.start()
        self.edit_table(worktree)
        root = self.bundle(worktree)
        fixture.edit(root, self.CHANNEL, "# Overview\n\nPayment events.", "# Overview\n\nPayment events, one per charge.")
        fixture.edit(root, self.CHANNEL_LOG, "## 2026-09-01\n", "## 2026-09-30\n\n* **Update**: Said when.\n\n## 2026-09-01\n")
        return worktree

    def untouched(self, worktree):
        self.assertNotIn("generated: { by: sdlc-test", fixture.read(self.bundle(worktree), TABLE))

    def test_a_named_file_is_stamped_but_not_confirmed(self):
        worktree = self.two_changes()
        code, result = self.finish(worktree, "--verified-by", "--unverified", f"wiki/{TABLE}")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["unverified"], [TABLE])
        self.assertEqual(self.meta(worktree, TABLE)["generated"]["by"], ACTOR)
        self.assertNotIn("verified", self.meta(worktree, TABLE))
        self.assertEqual(self.meta(worktree, self.CHANNEL)["verified"]["by"], "human:alice")

    def test_a_folder_names_every_changed_file_under_it(self):
        worktree = self.two_changes()
        code, result = self.finish(worktree, "--verified-by", "human:bob", "--unverified", "wiki/pay/channels/CHAN-pay-events")
        self.assertEqual((code, result["unverified"]), (0, [self.CHANNEL]), result)
        self.assertNotIn("verified", self.meta(worktree, self.CHANNEL))
        self.assertEqual(self.meta(worktree, TABLE)["verified"]["by"], "human:bob")

    def test_several_paths_are_taken_from_the_current_directory(self):
        worktree = self.two_changes()
        code, result = self.tool(
            "draft", "finish", "--by", ACTOR, "--unverified", "datastores/DB-main/TBL-payments.md", "channels", "--verified-by",
            cwd=worktree / "wiki" / "pay",
        )
        self.assertEqual((code, result["unverified"]), (0, [self.CHANNEL, TABLE]), result)
        self.assertNotIn("verified", self.meta(worktree, TABLE))
        self.assertNotIn("verified", self.meta(worktree, self.CHANNEL))

    def test_an_earlier_confirmation_of_a_named_file_is_removed(self):
        fixture.edit(self.root, TABLE, fixture.G, fixture.G + "\n" + fixture.V)
        commit_all(self.repo, "verify the table")
        worktree = self.two_changes()
        self.finish(worktree, "--verified-by", "--unverified", f"wiki/{TABLE}")
        self.assertNotIn("verified", self.meta(worktree, TABLE))

    def test_unverified_needs_verified_by(self):
        worktree = self.two_changes()
        code, result = self.finish(worktree, "--unverified", f"wiki/{TABLE}")
        self.assertEqual(code, 2)
        self.assertIn("--verified-by", result["error"])
        self.untouched(worktree)

    def test_a_path_the_draft_did_not_change_is_refused(self):
        worktree = self.two_changes()
        for path in ("wiki/pay/services/SVC-pay/overview.md", "wiki/pay/externals", "wiki/pay/nope.md", "wiki/pay/datastores/DB-main/index.md"):
            code, result = self.finish(worktree, "--verified-by", "--unverified", f"wiki/{TABLE}", path)
            self.assertEqual(code, 2, path)
            self.assertIn(path, result["error"])
        self.untouched(worktree)

    def test_an_unverified_reference_fails_validation(self):
        worktree = self.start()
        root = self.bundle(worktree)
        fixture.edit(root, "pay/references/REF-pay-prd/prd.md", "Shoppers pay for orders.", "Shoppers pay for orders in one step.")
        fixture.edit(root, "pay/references/REF-pay-prd/log.md", "## 2026-09-01\n", "## 2026-09-30\n\n* **Update**: PRD wording.\n\n## 2026-09-01\n")
        code, result = self.finish(worktree, "--verified-by", "--unverified", "wiki/pay/references/REF-pay-prd")
        self.assertEqual(code, 1)
        self.assertEqual([item["rule"] for item in result["validate"]["errors"]], ["frontmatter.reference-unverified"])


class DiffTest(DraftTest):
    def test_diff_separates_authored_files_from_tool_written_ones(self):
        worktree = self.start()
        root = self.bundle(worktree)
        fixture.edit(root, "pay/datastores/DB-main/overview.md", "description: Relational store.", "description: The main store.")
        fixture.edit(root, "pay/datastores/DB-main/log.md", "## 2026-09-01\n", "## 2026-09-30\n\n* **Update**: Described.\n\n## 2026-09-01\n")
        self.assertEqual(self.finish(worktree)[0], 0)
        code, result = self.tool("draft", "diff", cwd=worktree)
        self.assertEqual(code, 0)
        files = {item["path"]: (item["status"], item["authored"]) for item in result["files"]}
        self.assertEqual(files["wiki/pay/datastores/DB-main/overview.md"], ("M", True))
        self.assertEqual(files["wiki/pay/datastores/index.md"], ("M", False))
        self.assertIn("The main store.", result["diff"])
        self.assertEqual(result["base"], "main")

    def test_new_files_are_in_the_diff(self):
        worktree = self.start()
        fixture.write(self.bundle(worktree), "pay/decisions/ADR-charge-later.md", "x\n")
        code, result = self.tool("draft", "diff", cwd=worktree)
        self.assertIn(("wiki/pay/decisions/ADR-charge-later.md", "A", True), [(f["path"], f["status"], f["authored"]) for f in result["files"]])
        self.assertIn("+x", result["diff"])


class CommitTest(DraftTest):
    def finished(self):
        worktree = self.start()
        self.edit_table(worktree)
        self.assertEqual(self.finish(worktree)[0], 0)
        return worktree

    def test_commit_without_a_remote(self):
        worktree = self.finished()
        code, result = self.tool("draft", "commit", "-m", "Add the amount column", cwd=worktree)
        self.assertEqual(code, 0, result)
        self.assertEqual((result["branch"], result["pushed"]), ("wiki/coupons", False))
        self.assertIn("wiki/coupons", result["message"])
        self.assertFalse(worktree.exists())
        self.assertEqual(git(self.repo, "log", "-1", "--format=%s", "wiki/coupons"), "Add the amount column")
        self.assertEqual(git(self.repo, "rev-parse", "wiki/coupons"), result["commit"])
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")

    def test_commit_pushes_to_the_remote(self):
        self.add_remote()
        worktree = self.finished()
        code, result = self.tool("draft", "commit", "-m", "Add the amount column", cwd=worktree)
        self.assertEqual((code, result["pushed"]), (0, True), result)
        self.assertEqual(git(self.repo, "rev-parse", "origin/wiki/coupons"), result["commit"])

    def test_commit_refused_after_an_edit_made_after_finish(self):
        worktree = self.finished()
        fixture.edit(self.bundle(worktree), TABLE, "cents", "cents, never negative")
        code, result = self.tool("draft", "commit", "-m", "x", cwd=worktree)
        self.assertEqual(code, 1)
        self.assertIn("run draft finish again", result["error"])
        self.assertTrue(worktree.exists())

    def test_commit_refused_without_finish(self):
        worktree = self.start()
        self.edit_table(worktree)
        code, result = self.tool("draft", "commit", "-m", "x", cwd=worktree)
        self.assertEqual(code, 1)
        self.assertIn("draft finish", result["error"])

    def test_commit_refused_when_finish_was_not_ok(self):
        worktree = self.start()
        self.edit_table(worktree, log=False)
        self.finish(worktree)
        code, result = self.tool("draft", "commit", "-m", "x", cwd=worktree)
        self.assertEqual(code, 1)
        self.assertIn("not ok", result["error"])

    def test_commit_refuses_files_outside_the_wiki(self):
        worktree = self.start()
        self.edit_table(worktree)
        (worktree / "notes.txt").write_text("scratch\n", encoding="utf-8")
        self.finish(worktree)
        code, result = self.tool("draft", "commit", "-m", "x", cwd=worktree)
        self.assertEqual(code, 1)
        self.assertIn("notes.txt", result["error"])

    def test_commit_takes_the_workspace_note_but_not_agent_settings(self):
        worktree = self.start()
        self.edit_table(worktree)
        (worktree / "AGENTS.md").write_text("note\n", encoding="utf-8")
        (worktree / "CLAUDE.md").write_text("note\n", encoding="utf-8")
        (worktree / ".claude").mkdir()
        (worktree / ".claude/settings.json").write_text("{}\n", encoding="utf-8")
        self.finish(worktree)
        code, result = self.tool("draft", "commit", "-m", "x", cwd=worktree)
        self.assertEqual(code, 1)
        self.assertIn(".claude/settings.json", result["error"])
        self.assertNotIn("AGENTS.md", result["error"])
        self.assertNotIn("CLAUDE.md", result["error"])


class ResumeDiscardTest(DraftTest):
    def test_resume_recreates_the_worktree_of_a_committed_draft(self):
        worktree = self.start()
        self.edit_table(worktree)
        self.finish(worktree)
        self.tool("draft", "commit", "-m", "x", cwd=worktree)
        code, result = self.tool("draft", "resume", "coupons")
        self.assertEqual((code, result["branch"]), (0, "wiki/coupons"), result)
        self.assertIn("amount", fixture.read(self.bundle(worktree), TABLE))

    def test_resume_from_the_remote_branch(self):
        self.add_remote()
        other = self.clone("bob")
        git(other, "switch", "-q", "-c", "wiki/coupons")
        fixture.edit(other / "wiki", TABLE, "key |", "key, from bob |")
        commit_all(other, "bob's draft")
        git(other, "push", "-q", "origin", "wiki/coupons")
        code, result = self.tool("draft", "resume", "coupons")
        self.assertEqual(code, 0, result)
        self.assertIn("from bob", fixture.read(self.repo / ".worktrees/coupons/wiki", TABLE))

    def test_resume_without_a_branch(self):
        code, result = self.tool("draft", "resume", "nothing")
        self.assertEqual(code, 1)
        self.assertIn("no draft branch", result["error"])

    def test_discard_removes_the_worktree_and_the_branch(self):
        worktree = self.start()
        self.edit_table(worktree)
        code, result = self.tool("draft", "discard", "coupons")
        self.assertEqual(code, 0, result)
        self.assertFalse(worktree.exists())
        self.assertEqual(git(self.repo, "branch", "--list", "wiki/coupons"), "")

    def test_discard_remote_deletes_the_pushed_branch(self):
        self.add_remote()
        worktree = self.start()
        self.edit_table(worktree)
        self.finish(worktree)
        self.tool("draft", "commit", "-m", "x", cwd=worktree)
        code, result = self.tool("draft", "discard", "coupons", "--remote")
        self.assertEqual((code, result["deleted_remote"]), (0, True), result)
        self.assertEqual(git(self.repo, "ls-remote", "--heads", "origin", "wiki/coupons"), "")


class VerifyTest(DraftTest):
    def test_verify_stamps_the_file_and_logs_it(self):
        worktree = self.start()
        code, result = self.tool("verify", f"wiki/{TABLE}", cwd=worktree)
        self.assertEqual(code, 0, result)
        self.assertEqual(self.meta(worktree, TABLE)["verified"]["by"], "human:alice")
        self.assertEqual(self.meta(worktree, TABLE)["generated"]["by"], "human:alice")
        self.assertIn("* **Verification**: Confirmed by human:alice.", fixture.read(self.bundle(worktree), TABLE_LOG))
        self.assertEqual(result["log"], TABLE_LOG)

    def test_second_verification_makes_a_list(self):
        worktree = self.start()
        self.tool("verify", f"wiki/{TABLE}", cwd=worktree)
        self.tool("verify", f"wiki/{TABLE}", "--by", "human:bob", cwd=worktree)
        self.assertEqual([item["by"] for item in self.meta(worktree, TABLE)["verified"]], ["human:alice", "human:bob"])
        self.assertEqual(self.tool("validate", cwd=worktree)[0], 0)

    def test_by_must_be_a_human(self):
        worktree = self.start()
        code, result = self.tool("verify", f"wiki/{TABLE}", "--by", "bot/1", cwd=worktree)
        self.assertEqual(code, 2)
        self.assertIn("human:", result["error"])

    def test_verify_a_file_outside_the_bundle(self):
        worktree = self.start()
        code, result = self.tool("verify", ".gitignore", cwd=worktree)
        self.assertEqual(code, 2)
        self.assertIn("not a concept", result["error"])


CHANGE_LOG = fixture.LOG


def change(title, requirement):
    text = fixture.FILES["pay/change-requests/CR-1/overview.md"].replace("status: Approved", "status: Proposed")
    return text.replace("Accept coupons", title).replace("REQ-pay-2", requirement).replace("#req-pay-2", "#" + requirement.lower())


class RefreshTest(DraftTest):
    def merge_to_main(self, key):
        git(self.repo, "merge", "-q", "--no-ff", "-m", f"Merge {key}", f"wiki/{key}")

    def draft(self, key, write):
        worktree = self.start(key)
        write(self.bundle(worktree))
        code, result = self.finish(worktree)
        self.assertEqual(code, 0, result)
        code, result = self.tool("draft", "commit", "-m", key, cwd=worktree)
        self.assertEqual(code, 0, result)

    def add_change(self, key, title, requirement):
        def write(root):
            fixture.write(root, f"pay/change-requests/{key}/overview.md", change(title, requirement))
            fixture.write(root, f"pay/change-requests/{key}/log.md", CHANGE_LOG)
        return write

    def test_refresh_resolves_conflicts_in_tool_written_files(self):
        self.draft("gift-cards", self.add_change("CR-gift-cards", "Accept gift cards", "REQ-pay-gift-card"))
        self.draft("vouchers", self.add_change("CR-vouchers", "Accept vouchers", "REQ-pay-voucher"))
        self.merge_to_main("gift-cards")
        self.tool("draft", "resume", "vouchers")
        worktree = self.repo / ".worktrees/vouchers"
        code, result = self.tool("refresh", cwd=worktree)
        self.assertEqual(code, 0, result)
        self.assertIn("wiki/pay/change-requests/index.md", result["resolved"])
        self.assertIn("wiki/pay/features/FEAT-pay/overview.md", result["resolved"])
        self.assertTrue(result["validate"]["ok"])
        history = fixture.read(self.bundle(worktree), FEATURE)
        self.assertIn("CR-gift-cards", history)
        self.assertIn("CR-vouchers", history)
        self.assertEqual(git(worktree, "status", "--porcelain"), "")
        self.assertEqual(git(worktree, "log", "-1", "--format=%P").count(" "), 1)

    def test_refresh_aborts_on_an_authored_conflict(self):
        def amount(row):
            def write(root):
                fixture.edit(root, TABLE, "| `id` | uuid | yes | key |", "| `id` | uuid | yes | key |\n" + row)
                fixture.edit(root, TABLE_LOG, "## 2026-09-01\n", "## 2026-09-30\n\n" + NEW_ENTRY + "\n## 2026-09-01\n")
            return write

        self.draft("a", amount("| `amount` | integer | yes | cents |"))
        self.draft("b", amount("| `amount` | decimal | yes | euros |"))
        self.merge_to_main("a")
        self.tool("draft", "resume", "b")
        worktree = self.repo / ".worktrees/b"
        code, result = self.tool("refresh", cwd=worktree)
        self.assertEqual(code, 1)
        self.assertIn("a person has to resolve these", result["error"])
        self.assertIn(f"wiki/{TABLE}", result["error"])
        self.assertFalse((worktree / git(worktree, "rev-parse", "--git-dir") / "MERGE_HEAD").exists())
        self.assertEqual(git(worktree, "status", "--porcelain"), "")

    def test_refresh_with_nothing_new(self):
        self.draft("a", self.add_change("CR-a", "Accept a", "REQ-pay-a"))
        self.tool("draft", "resume", "a")
        code, result = self.tool("refresh", cwd=self.repo / ".worktrees/a")
        self.assertEqual((code, result["merged"]), (0, None), result)


class RunPlanTest(DraftTest):
    """A skill's Run plan, <worktree>/plan.md, is never part of the Draft."""

    def exclude(self):
        return self.repo / ".git" / "info" / "exclude"

    def test_start_makes_git_ignore_the_run_plan(self):
        worktree = self.start()
        (worktree / "plan.md").write_text("# Run plan\n", encoding="utf-8")
        self.assertEqual(git(worktree, "status", "--porcelain"), "")
        self.assertIn("/plan.md", self.exclude().read_text(encoding="utf-8").splitlines())

    def test_the_rule_is_written_once(self):
        self.start("a")
        self.start("b")
        self.tool("draft", "resume", "a")
        self.assertEqual(self.exclude().read_text(encoding="utf-8").splitlines().count("/plan.md"), 1)

    def test_a_file_named_plan_inside_the_wiki_is_not_ignored(self):
        worktree = self.start()
        fixture.write(self.bundle(worktree), "pay/plan.md", "x\n")
        self.assertIn("wiki/pay/plan.md", git(worktree, "status", "--porcelain"))

    def test_finish_diff_and_commit_leave_the_run_plan_out(self):
        worktree = self.start()
        self.edit_table(worktree)
        (worktree / "plan.md").write_text("# Run plan\n", encoding="utf-8")
        code, result = self.finish(worktree)
        self.assertEqual((code, result["ok"]), (0, True), result)
        code, result = self.tool("draft", "diff", cwd=worktree)
        self.assertNotIn("plan.md", [item["path"] for item in result["files"]])
        code, result = self.tool("draft", "commit", "-m", "Add the amount column", cwd=worktree)
        self.assertEqual(code, 0, result)
        self.assertNotIn("plan.md", git(self.repo, "show", "--name-only", "--format=", "wiki/coupons").splitlines())

    def test_resume_writes_the_rule_in_a_repository_that_lacks_it(self):
        worktree = self.start()
        self.edit_table(worktree)
        self.finish(worktree)
        self.tool("draft", "commit", "-m", "x", cwd=worktree)
        self.exclude().write_text("", encoding="utf-8")
        code, result = self.tool("draft", "resume", "coupons")
        self.assertEqual(code, 0, result)
        (self.repo / result["worktree"] / "plan.md").write_text("# Run plan\n", encoding="utf-8")
        self.assertEqual(git(self.repo / result["worktree"], "status", "--porcelain"), "")

    def test_refresh_is_not_stopped_by_the_run_plan(self):
        worktree = self.start()
        self.edit_table(worktree)
        self.finish(worktree)
        self.tool("draft", "commit", "-m", "x", cwd=worktree)
        code, result = self.tool("draft", "resume", "coupons")
        worktree = self.repo / result["worktree"]
        (worktree / "plan.md").write_text("# Run plan\n", encoding="utf-8")
        code, result = self.tool("refresh", cwd=worktree)
        self.assertEqual((code, result["ok"]), (0, True), result)


if __name__ == "__main__":
    unittest.main()
