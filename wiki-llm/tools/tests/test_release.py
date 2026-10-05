"""The Release: RELEASE files, the release copy in sdlc-setup-wiki, release.py,
and the rules every skill package follows."""

import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from wikilib import toolcopy

REPO = toolcopy.TOOL_HOME.parent
SKILLS = REPO / "skills"
SETUP = SKILLS / "sdlc-setup-wiki"
FIX = "run `python3 release.py` to refresh it"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def release_of(folder: Path) -> str:
    return (folder / "RELEASE").read_text(encoding="utf-8")


def release_module():
    spec = importlib.util.spec_from_file_location("release", REPO / "release.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReleaseTest(unittest.TestCase):
    def test_this_tool_has_a_release_version(self):
        self.assertRegex(release_of(toolcopy.TOOL_HOME), r"^\d+\.\d+\.\d+\n$")

    def test_every_skill_release_matches(self):
        files = sorted(SKILLS.glob("*/RELEASE"))
        self.assertIn(SETUP / "RELEASE", files)
        for path in files:
            self.assertEqual(path.read_text(encoding="utf-8"), release_of(toolcopy.TOOL_HOME), f"{path}: {FIX}")

    def test_release_copy_matches_the_tool(self):
        copy = SETUP / "wiki-llm"
        expected = {rel: sha(path) for rel, path in toolcopy._files(toolcopy.TOOL_HOME).items()}
        present = {rel: sha(path) for rel, path in toolcopy._copy_files(copy).items()}
        self.assertEqual(present, expected, f"the release copy in {copy} is out of date: {FIX}")
        manifest = json.loads((copy / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["files"], expected, FIX)
        self.assertEqual(manifest["release_version"], toolcopy.release_version(), FIX)
        self.assertEqual(manifest["schema_version"], json.loads(
            (toolcopy.TOOL_HOME / "schema/schema.json").read_text(encoding="utf-8"))["schema_version"], FIX)

    def test_shared_references_are_current(self):
        release = release_module()
        for name, owners in release.REFERENCES.items():
            shared = (REPO / "skill-shared" / name).read_text(encoding="utf-8")
            for skill in owners:
                if (SKILLS / skill / "SKILL.md").is_file():
                    copy = SKILLS / skill / "references" / name
                    self.assertEqual(copy.read_text(encoding="utf-8"), shared, f"{copy}: {FIX}")

    def test_every_skill_has_a_current_openai_yaml(self):
        release = release_module()
        entries = json.loads((REPO / "skill-shared/openai.json").read_text(encoding="utf-8"))
        for skill in sorted(SKILLS.glob("*/SKILL.md")):
            name = skill.parent.name
            self.assertIn(name, entries, f"add {name} to skill-shared/openai.json")
            yaml = skill.parent / "agents/openai.yaml"
            self.assertEqual(yaml.read_text(encoding="utf-8"), release.openai_yaml(entries[name]), f"{yaml}: {FIX}")

    def test_only_skills_that_check_the_wiki_carry_release(self):
        for name in ("sdlc-ask-wiki", "sdlc-convert-doc", "sdlc-review-code"):
            self.assertFalse((SKILLS / name / "RELEASE").exists(), name)

    def test_every_writer_carries_release(self):
        release = release_module()
        for name in release.WRITERS:
            if (SKILLS / name / "SKILL.md").is_file():
                self.assertTrue((SKILLS / name / "RELEASE").is_file(), f"{name} writes to the wiki: it needs a RELEASE file")

    def test_the_import_and_review_skills_get_their_references(self):
        release = release_module()
        entries = json.loads((REPO / "skill-shared/openai.json").read_text(encoding="utf-8"))
        self.assertIn("sdlc-import", release.WRITERS)
        self.assertIn("sdlc-import", release.REFERENCES["write-protocol.md"])
        self.assertIn("sdlc-import", release.REFERENCES["read-protocol.md"])
        self.assertIn("sdlc-review-code", release.REFERENCES["read-protocol.md"])
        self.assertNotIn("sdlc-review-code", release.REFERENCES["write-protocol.md"])
        for name in ("sdlc-import", "sdlc-review-code"):
            self.assertEqual(sorted(entries[name]), sorted(release.OPENAI_KEYS), name)

    def test_the_stories_skill_gets_its_references(self):
        release = release_module()
        entries = json.loads((REPO / "skill-shared/openai.json").read_text(encoding="utf-8"))
        self.assertIn("sdlc-write-stories", release.WRITERS)
        for name in ("read-protocol.md", "flow.md", "write-protocol.md", "paste-format.md"):
            self.assertIn("sdlc-write-stories", release.REFERENCES[name], name)
        self.assertIn("sdlc-ask-wiki", release.REFERENCES["paste-format.md"])
        self.assertEqual(sorted(entries["sdlc-write-stories"]), sorted(release.OPENAI_KEYS))

    def test_the_closing_skills_get_their_references(self):
        release = release_module()
        entries = json.loads((REPO / "skill-shared/openai.json").read_text(encoding="utf-8"))
        for name in ("sdlc-close-task", "sdlc-edit-wiki"):
            self.assertIn(name, release.WRITERS)
            for reference in ("read-protocol.md", "flow.md", "write-protocol.md"):
                self.assertIn(name, release.REFERENCES[reference], reference)
        for reference in ("read-protocol.md", "flow.md", "code-checks.md"):
            self.assertIn("sdlc-build-task", release.REFERENCES[reference], reference)
        self.assertNotIn("sdlc-build-task", release.REFERENCES["write-protocol.md"])
        self.assertEqual(release.REFERENCES["code-checks.md"], ("sdlc-build-task", "sdlc-review-code"))
        for name in ("sdlc-build-task", "sdlc-close-task", "sdlc-edit-wiki"):
            self.assertEqual(sorted(entries[name]), sorted(release.OPENAI_KEYS), name)

    def test_release_copy_carries_no_tests_or_sample(self):
        copy = SETUP / "wiki-llm"
        self.assertFalse((copy / "tools/tests").exists())
        self.assertFalse((copy / "sample").exists())


class ReleaseScriptTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "sdlc-skills"
        ignore = shutil.ignore_patterns("tests", "__pycache__", "sample")
        shutil.copytree(REPO / "wiki-llm", self.root / "wiki-llm", ignore=ignore)
        shutil.copy(REPO / "release.py", self.root)
        shutil.copytree(REPO / "skill-shared", self.root / "skill-shared")
        for name in ("sdlc-setup-wiki", "sdlc-write-spec", "sdlc-convert-doc", "sdlc-ask-wiki"):
            (self.root / "skills" / name).mkdir(parents=True)
            (self.root / "skills" / name / "SKILL.md").write_text("---\nname: x\n---\n", encoding="utf-8")
        for name in ("sdlc-setup-wiki", "sdlc-write-spec"):
            (self.root / "skills" / name / "RELEASE").write_text("0.0.1\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def release(self, *argv):
        out = subprocess.run(["python3", str(self.root / "release.py"), *argv], capture_output=True, text=True)
        return out.returncode, json.loads(out.stdout)

    def test_sets_every_release_and_rebuilds_the_copy(self):
        code, result = self.release("9.9.0")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["release_version"], "9.9.0")
        self.assertEqual(release_of(self.root / "wiki-llm"), "9.9.0\n")
        for name in ("sdlc-setup-wiki", "sdlc-write-spec"):
            self.assertEqual(release_of(self.root / "skills" / name), "9.9.0\n")
        for name in ("sdlc-convert-doc", "sdlc-ask-wiki"):
            self.assertFalse((self.root / "skills" / name / "RELEASE").exists())
        manifest = json.loads((self.root / "skills/sdlc-setup-wiki/wiki-llm/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["release_version"], "9.9.0")
        self.assertIn("tools/wikilib/link.py", manifest["files"])
        self.assertEqual(sorted(result["written"]), [
            "skills/sdlc-ask-wiki/agents/openai.yaml",
            "skills/sdlc-ask-wiki/references/paste-format.md",
            "skills/sdlc-ask-wiki/references/read-protocol.md",
            "skills/sdlc-convert-doc/agents/openai.yaml",
            "skills/sdlc-setup-wiki/RELEASE",
            "skills/sdlc-setup-wiki/agents/openai.yaml",
            "skills/sdlc-setup-wiki/wiki-llm/",
            "skills/sdlc-write-spec/RELEASE",
            "skills/sdlc-write-spec/agents/openai.yaml",
            "skills/sdlc-write-spec/references/flow.md",
            "skills/sdlc-write-spec/references/read-protocol.md",
            "skills/sdlc-write-spec/references/write-protocol.md",
            "wiki-llm/RELEASE",
        ])

    def test_refresh_keeps_the_version(self):
        version = release_of(self.root / "wiki-llm").strip()
        code, result = self.release()
        self.assertEqual((code, result["release_version"]), (0, version))
        self.assertEqual(release_of(self.root / "skills/sdlc-write-spec"), version + "\n")
        self.assertNotIn("wiki-llm/RELEASE", result["written"])

    def test_the_release_copy_runs_on_its_own(self):
        self.release("2.1.0")
        tool = self.root / "skills/sdlc-setup-wiki/wiki-llm/tools/wiki_llm.py"
        wiki = Path(self._tmp.name) / "acme-wiki"
        out = subprocess.run(["python3", str(tool), "init", str(wiki), "--app", "shop", "--title", "Shop",
                              "--owner-team", "web"], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        out = subprocess.run(["python3", str(tool), "copy", "check", str(wiki)], capture_output=True, text=True)
        self.assertEqual(json.loads(out.stdout)["status"], "current")
        self.assertEqual(json.loads((wiki / ".wiki-llm/manifest.json").read_text(encoding="utf-8"))["release_version"], "2.1.0")

    def test_not_a_version(self):
        code, result = self.release("two")
        self.assertEqual(code, 2)
        self.assertIn("not a version", result["error"])
        self.assertEqual(release_of(self.root / "skills/sdlc-write-spec"), "0.0.1\n")

    def test_copies_shared_references_and_writes_openai_yaml(self):
        code, result = self.release()
        self.assertEqual(code, 0, result)
        shared = self.root / "skill-shared"
        spec = self.root / "skills/sdlc-write-spec/references/write-protocol.md"
        self.assertEqual(spec.read_text(encoding="utf-8"), (shared / "write-protocol.md").read_text(encoding="utf-8"))
        self.assertFalse((self.root / "skills/sdlc-ask-wiki/references/write-protocol.md").exists())
        flow = self.root / "skills/sdlc-write-spec/references/flow.md"
        self.assertEqual(flow.read_text(encoding="utf-8"), (shared / "flow.md").read_text(encoding="utf-8"))
        self.assertFalse((self.root / "skills/sdlc-ask-wiki/references/flow.md").exists())
        self.assertFalse((self.root / "skills/sdlc-setup-wiki/references").exists())
        yaml = (self.root / "skills/sdlc-ask-wiki/agents/openai.yaml").read_text(encoding="utf-8")
        self.assertTrue(yaml.startswith('interface:\n  display_name: "SDLC Ask Wiki"\n'), yaml)
        self.assertIn('  default_prompt: "Use $sdlc-ask-wiki ', yaml)
        code, again = self.release()
        self.assertEqual(again["written"], ["skills/sdlc-setup-wiki/wiki-llm/"])

    def test_a_skill_missing_from_openai_json_stops_the_release(self):
        (self.root / "skills/sdlc-new").mkdir()
        (self.root / "skills/sdlc-new/SKILL.md").write_text("---\nname: x\n---\n", encoding="utf-8")
        code, result = self.release("2.1.0")
        self.assertEqual(code, 2)
        self.assertIn("sdlc-new", result["error"])
        self.assertEqual(release_of(self.root / "wiki-llm"), release_of(REPO / "wiki-llm"))

    def tag(self, version):
        for argv in (["init", "-q"], ["add", "-A"], ["commit", "-qm", "release"], ["tag", f"v{version}"]):
            subprocess.run(["git", "-c", "user.name=T", "-c", "user.email=t@example.com", "-c", "commit.gpgsign=false",
                            "-C", str(self.root), *argv], check=True, capture_output=True)

    def change_the_tool(self):
        link = self.root / "wiki-llm/tools/wikilib/link.py"
        link.write_text(link.read_text(encoding="utf-8") + "\n# changed\n", encoding="utf-8")

    def test_a_tool_change_after_a_tagged_release_needs_a_new_minor_version(self):
        self.release("2.1.0")
        self.tag("2.1.0")
        self.change_the_tool()
        for argv in ((), ("2.1.1",)):
            code, result = self.release(*argv)
            self.assertEqual(code, 2, result)
            self.assertIn("python3 release.py 2.2.0", result["error"])
        self.assertEqual(release_of(self.root / "wiki-llm"), "2.1.0\n")
        code, result = self.release("2.2.0")
        self.assertEqual(code, 0, result)

    def test_a_skill_only_patch_after_a_tagged_release(self):
        self.release("2.1.0")
        self.tag("2.1.0")
        code, result = self.release("2.1.1")
        self.assertEqual(code, 0, result)
        self.assertEqual(release_of(self.root / "skills/sdlc-write-spec"), "2.1.1\n")

    def test_an_untagged_release_may_still_change_the_tool(self):
        self.release("2.1.0")
        self.change_the_tool()
        code, result = self.release()
        self.assertEqual(code, 0, result)


class SkillPackageTest(unittest.TestCase):
    """The rules of ADR 0003 and the runbook's skill rules for every skill package."""

    def skill_files(self):
        for path in sorted(SKILLS.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                yield path

    def test_no_agent_specific_text(self):
        for path in self.skill_files():
            text = path.read_text(encoding="utf-8")
            for banned in (r"(?i)plugin", r"\.claude/", r"base directory", r"\brtk\b"):
                self.assertIsNone(re.search(banned, text), f"{path.relative_to(REPO)} contains {banned}")

    def test_frontmatter_has_only_name_and_description(self):
        for skill in sorted(SKILLS.glob("*/SKILL.md")):
            head = skill.read_text(encoding="utf-8").split("---")[1]
            keys = [line.split(":")[0] for line in head.strip().split("\n") if line and not line[0].isspace()]
            self.assertEqual(keys, ["name", "description"], skill)
            self.assertLess(len(skill.read_text(encoding="utf-8").split("\n")), 500, skill)

    def test_no_claude_plugin_folder(self):
        self.assertFalse((REPO / ".claude-plugin").exists())


if __name__ == "__main__":
    unittest.main()
