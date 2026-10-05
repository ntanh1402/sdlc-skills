"""install-skills.sh: copy or link the skills into an agent's skills folder."""

import subprocess
import tempfile
import unittest
from pathlib import Path

from wikilib import toolcopy

REPO = toolcopy.TOOL_HOME.parent
SCRIPT = REPO / "install-skills.sh"
NAMES = sorted(path.parent.name for path in (REPO / "skills").glob("*/SKILL.md"))


def install(*argv):
    out = subprocess.run(["bash", str(SCRIPT), *argv], capture_output=True, text=True)
    return out.returncode, out.stdout + out.stderr


class InstallSkillsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.agent = Path(self._tmp.name) / "agent" / "skills"

    def tearDown(self):
        self._tmp.cleanup()

    def test_copies_every_skill_without_caches(self):
        code, output = install(str(self.agent))
        self.assertEqual(code, 0, output)
        self.assertEqual(sorted(path.name for path in self.agent.iterdir()), NAMES)
        setup = self.agent / "sdlc-setup-wiki"
        self.assertFalse(setup.is_symlink())
        self.assertTrue((setup / "SKILL.md").is_file())
        self.assertTrue((setup / "wiki-llm/tools/wiki_llm.py").is_file())
        self.assertEqual(list(setup.rglob("__pycache__")), [])
        self.assertIn("copied sdlc-setup-wiki", output)

    def test_links_with_link(self):
        code, output = install(str(self.agent), "--link")
        self.assertEqual(code, 0, output)
        setup = self.agent / "sdlc-setup-wiki"
        self.assertTrue(setup.is_symlink())
        self.assertEqual(setup.resolve(), (REPO / "skills/sdlc-setup-wiki").resolve())

    def test_a_second_install_replaces_the_first(self):
        install(str(self.agent), "--link")
        code, output = install(str(self.agent))
        self.assertEqual(code, 0, output)
        self.assertFalse((self.agent / "sdlc-setup-wiki").is_symlink())
        (self.agent / "sdlc-setup-wiki/extra.txt").write_text("x", encoding="utf-8")
        self.assertEqual(install(str(self.agent))[0], 0)
        self.assertFalse((self.agent / "sdlc-setup-wiki/extra.txt").exists())

    def test_a_folder_that_is_not_a_skill_stops_everything(self):
        (self.agent / "sdlc-setup-wiki").mkdir(parents=True)
        (self.agent / "sdlc-setup-wiki/mine.txt").write_text("x", encoding="utf-8")
        code, output = install(str(self.agent))
        self.assertEqual(code, 1)
        self.assertIn("is not an installed skill", output)
        self.assertEqual([path.name for path in self.agent.iterdir()], ["sdlc-setup-wiki"])
        self.assertTrue((self.agent / "sdlc-setup-wiki/mine.txt").exists())

    def test_usage(self):
        self.assertEqual(install()[0], 1)
        self.assertEqual(install(str(self.agent), "--copy")[0], 1)
        self.assertFalse(self.agent.exists())


if __name__ == "__main__":
    unittest.main()
