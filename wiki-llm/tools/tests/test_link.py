"""link: the Workspace note that tells skills where the Wiki repository is."""

import os
import tempfile
import unittest
from pathlib import Path

from wikilib import link

from .test_cli import run

START, END = "<!-- sdlc-skills:start -->", "<!-- sdlc-skills:end -->"


class LinkTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name).resolve()
        self.work = self.tmp / "work"
        self.wiki = self.work / "shop-wiki"
        code, result = run("init", str(self.wiki), "--app", "shop", "--title", "Shop", "--owner-team", "web")
        self.assertEqual(code, 0, result)
        self.space = self.work / "shop-api"
        self.space.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def link(self, space=None, wiki=None):
        return run("link", str(space or self.space), str(wiki or self.wiki))

    def read(self, name, space=None):
        return ((space or self.space) / name).read_text(encoding="utf-8")

    def test_creates_agents_md_with_a_relative_path(self):
        code, result = self.link()
        self.assertEqual(code, 0, result)
        self.assertEqual((result["wiki"], result["written"], result["unchanged"], result["warnings"]),
                         ("../shop-wiki", ["AGENTS.md"], [], []))
        self.assertEqual(result["workspace"], str(self.space))
        self.assertEqual(self.read("AGENTS.md"), link.note("../shop-wiki"))
        self.assertFalse((self.space / "CLAUDE.md").exists())

    def test_the_note_text(self):
        self.assertEqual(link.note("../shop-wiki"), "\n".join([
            START,
            "## Project wiki",
            "",
            "The wiki repository of this workspace is `../shop-wiki` (relative to this file).",
            "sdlc-skills run its tool from inside that folder:",
            "`cd ../shop-wiki && python3 .wiki-llm/tools/wiki_llm.py <command>`",
            END,
        ]) + "\n")

    def test_a_path_with_spaces_is_quoted_in_the_command(self):
        self.assertIn("`cd '../my wiki' && python3", link.note("../my wiki"))

    def test_appends_to_every_existing_instruction_file(self):
        (self.space / "AGENTS.md").write_text("# Agents\n\nRules.", encoding="utf-8")
        (self.space / "CLAUDE.md").write_text("# Claude\n", encoding="utf-8")
        code, result = self.link()
        self.assertEqual(code, 0, result)
        self.assertEqual(result["written"], ["AGENTS.md", "CLAUDE.md"])
        self.assertEqual(self.read("AGENTS.md"), "# Agents\n\nRules.\n\n" + link.note("../shop-wiki"))
        self.assertEqual(self.read("CLAUDE.md"), "# Claude\n\n" + link.note("../shop-wiki"))

    def test_only_claude_md(self):
        (self.space / "CLAUDE.md").write_text("# Claude\n", encoding="utf-8")
        code, result = self.link()
        self.assertEqual(result["written"], ["CLAUDE.md"])
        self.assertFalse((self.space / "AGENTS.md").exists())

    def test_replaces_the_note_and_keeps_the_rest(self):
        (self.space / "AGENTS.md").write_text(f"# A\n\n{START}\nold\n{END}\n\n# After\n", encoding="utf-8")
        code, result = self.link()
        self.assertEqual(code, 0, result)
        self.assertEqual(self.read("AGENTS.md"), "# A\n\n" + link.note("../shop-wiki") + "\n# After\n")

    def test_second_run_changes_nothing(self):
        self.link()
        code, result = self.link()
        self.assertEqual((code, result["written"], result["unchanged"]), (0, [], ["AGENTS.md"]))

    def test_moved_wiki_replaces_the_note(self):
        self.link()
        other = self.tmp / "work" / "elsewhere"
        self.wiki.rename(other)
        code, result = self.link(wiki=other)
        self.assertEqual(result["written"], ["AGENTS.md"])
        self.assertEqual(self.read("AGENTS.md"), link.note("../elsewhere"))

    def test_broken_markers_are_refused_before_any_write(self):
        (self.space / "CLAUDE.md").write_text("# fine\n", encoding="utf-8")
        for text in (f"{START}\nno end\n", f"no start\n{END}\n", f"{START}\n{END}\n{START}\n{END}\n"):
            (self.space / "AGENTS.md").write_text(text, encoding="utf-8")
            code, result = self.link()
            self.assertEqual(code, 1, text)
            self.assertIn("AGENTS.md", result["error"])
            self.assertEqual(self.read("CLAUDE.md"), "# fine\n")

    def test_the_wiki_repository_as_its_own_workspace(self):
        code, result = self.link(space=self.wiki)
        self.assertEqual((code, result["wiki"], result["written"]), (0, ".", ["AGENTS.md"]))
        self.assertIn("`cd . && python3 .wiki-llm/tools/wiki_llm.py <command>`", self.read("AGENTS.md", self.wiki))

    def test_paths_may_be_relative_to_the_current_folder(self):
        cwd = os.getcwd()
        os.chdir(self.work)
        try:
            code, result = run("link", "shop-api", "shop-wiki")
        finally:
            os.chdir(cwd)
        self.assertEqual((code, result["wiki"]), (0, "../shop-wiki"), result)

    def test_absolute_path_when_only_the_root_is_shared(self):
        self.assertEqual(link.path_for(Path("/a/space"), Path("/b/wiki")), ("/b/wiki", True))
        self.assertEqual(link.path_for(Path("/a/space"), Path("/a/wiki")), ("../wiki", False))
        self.assertEqual(link.path_for(Path("/a/wiki"), Path("/a/wiki")), (".", False))
        self.assertEqual(link.path_for(Path("/a/wiki/docs"), Path("/a/wiki")), ("..", False))

    def test_absolute_path_carries_a_warning(self):
        warnings = link.warnings_for("/b/wiki", True)
        self.assertEqual(warnings, ["the note holds an absolute path (/b/wiki); people whose checkout is "
                                    "elsewhere must run sdlc-setup-wiki again"])
        self.assertEqual(link.warnings_for("../wiki", False), [])

    def test_not_a_wiki_repository(self):
        code, result = self.link(wiki=self.space)
        self.assertEqual(code, 2)
        self.assertIn("not a wiki repository", result["error"])
        self.assertFalse((self.space / "AGENTS.md").exists())

    def test_a_git_repository_whose_setup_is_not_merged_yet(self):
        pending = self.work / "pending-wiki"
        (pending / ".git").mkdir(parents=True)
        code, result = self.link(wiki=pending)
        self.assertEqual((code, result["written"]), (0, ["AGENTS.md"]), result)
        self.assertEqual(result["warnings"], ["../pending-wiki has no wiki on its checked-out branch yet: skills "
                                              "find it once the setup pull request is merged"])

    def test_missing_workspace(self):
        code, result = self.link(space=self.tmp / "nope")
        self.assertEqual(code, 2)
        self.assertIn("not a folder", result["error"])


if __name__ == "__main__":
    unittest.main()
