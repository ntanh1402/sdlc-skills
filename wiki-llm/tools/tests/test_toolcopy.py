"""init and the Tool copy: install, check against its manifest and a release."""

import contextlib
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from wikilib import toolcopy
from wikilib.schema import SCHEMA_DIR

from .test_cli import run

def fake_source(where: Path, version: str, schema_version: str | None = None) -> Path:
    """A tool folder (schema/ and RELEASE) of another release."""
    where.mkdir(parents=True)
    (where / "RELEASE").write_text(version + "\n", encoding="utf-8")
    shutil.copytree(SCHEMA_DIR, where / "schema")
    if schema_version:
        path = where / "schema/schema.json"
        path.write_text(path.read_text(encoding="utf-8").replace('"schema_version": "1"', f'"schema_version": "{schema_version}"'), encoding="utf-8")
    return where


class CopyTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.repo = self.tmp / "acme-wiki"
        self.repo.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def install(self):
        code, result = run("copy", "install", str(self.repo))
        self.assertEqual(code, 0, result)
        return result

    def check(self, *argv):
        with contextlib.chdir(self.repo):
            return run("copy", "check", *argv)

    def test_install_writes_schema_tools_and_manifest(self):
        result = self.install()
        copy = self.repo / ".wiki-llm"
        manifest = json.loads((copy / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["release_version"], toolcopy.release_version())
        self.assertNotIn("plugin_version", manifest)
        self.assertEqual(result["release_version"], toolcopy.release_version())
        self.assertEqual(manifest["schema_version"], "1")
        self.assertIn("schema/schema.json", manifest["files"])
        self.assertIn("tools/wiki_llm.py", manifest["files"])
        self.assertIn("tools/wikilib/draft.py", manifest["files"])
        self.assertFalse(any(path.startswith("tools/tests/") or "__pycache__" in path for path in manifest["files"]))
        self.assertEqual(result["files"], len(manifest["files"]))

    def test_installed_copy_runs_and_reports_its_own_version(self):
        self.install()
        out = subprocess.run(
            ["python3", str(self.repo / ".wiki-llm/tools/wiki_llm.py"), "copy", "check"],
            cwd=self.repo, capture_output=True, text=True,
        )
        result = json.loads(out.stdout)
        self.assertEqual((out.returncode, result["status"]), (0, "current"), out.stderr)

    def test_check_matching_copy(self):
        self.install()
        code, result = self.check()
        self.assertEqual((code, result["status"], result["added"], result["missing"], result["changed"]), (0, "current", [], [], []))

    def test_python_caches_are_not_edits(self):
        self.install()
        (self.repo / ".wiki-llm/tools/wikilib/__pycache__").mkdir()
        (self.repo / ".wiki-llm/tools/wikilib/__pycache__/draft.cpython-314.pyc").write_bytes(b"x")
        self.assertEqual(self.check()[1]["status"], "current")

    def test_check_reports_edited_copy(self):
        self.install()
        (self.repo / ".wiki-llm/tools/wikilib/draft.py").write_text("edited\n", encoding="utf-8")
        (self.repo / ".wiki-llm/schema/task.md").unlink()
        (self.repo / ".wiki-llm/tools/extra.py").write_text("x\n", encoding="utf-8")
        (self.repo / ".wiki-llm/tools/tests").mkdir()
        (self.repo / ".wiki-llm/tools/tests/test_x.py").write_text("x\n", encoding="utf-8")
        (self.repo / ".wiki-llm/notes.md").write_text("x\n", encoding="utf-8")
        code, result = self.check()
        self.assertEqual(code, 1)
        self.assertEqual(result["status"], "edited")
        self.assertEqual(result["changed"], ["tools/wikilib/draft.py"])
        self.assertEqual(result["missing"], ["schema/task.md"])
        self.assertEqual(result["added"], ["notes.md", "tools/extra.py", "tools/tests/test_x.py"])
        self.assertEqual(result["message"], "the tool copy was edited by hand: run sdlc-setup-wiki to restore it")

    def test_check_is_found_from_a_subdirectory(self):
        self.install()
        (self.repo / "wiki").mkdir()
        with contextlib.chdir(self.repo / "wiki"):
            self.assertEqual(run("copy", "check")[0], 0)

    def test_no_copy(self):
        code, result = self.check()
        self.assertEqual(code, 2)
        self.assertIn("no tool copy", result["error"])

    def test_older_release_must_be_upgraded(self):
        self.install()
        major = toolcopy.release_version().split(".")[0]
        for version in ("99.0.0", f"{major}.99.0"):
            source = fake_source(self.tmp / f"source-{version}", version)
            code, result = self.check("--source", str(source))
            self.assertEqual((code, result["status"]), (1, "older"), version)
            self.assertEqual(result["message"], "the wiki is older than these skills: run sdlc-setup-wiki to upgrade it")
            self.assertEqual(result["source"], {"release_version": version, "schema_version": "1"})

    def test_other_schema_version_must_be_upgraded(self):
        self.install()
        source = fake_source(self.tmp / "source", toolcopy.release_version(), schema_version="3")
        self.assertEqual(self.check("--source", str(source))[1]["status"], "older")

    def test_newer_copy_needs_newer_skills(self):
        self.install()
        source = fake_source(self.tmp / "source", "0.9.0")
        code, result = self.check("--source", str(source))
        self.assertEqual((code, result["status"]), (1, "newer"))
        self.assertEqual(result["message"], "the wiki was set up by a newer release: update your installed sdlc-skills")

    def test_a_source_without_release_uses_its_manifest(self):
        self.install()
        other = self.tmp / "other"
        other.mkdir()
        code, _ = run("copy", "install", str(other))
        self.assertEqual(code, 0)
        code, result = self.check("--source", str(other / ".wiki-llm"))
        self.assertEqual((code, result["status"]), (0, "current"), result)

    def test_not_a_source_folder(self):
        self.install()
        code, result = self.check("--source", str(self.tmp))
        self.assertEqual(code, 2)
        self.assertIn("not a tool folder", result["error"])

    def test_release_option_compares_the_release_only(self):
        self.install()
        version = toolcopy.release_version()
        code, result = self.check("--release", version)
        self.assertEqual((code, result["status"]), (0, "current"), result)
        self.assertEqual(result["source"], {"release_version": version, "schema_version": None})
        self.assertEqual(self.check("--release", "99.0.0")[1]["status"], "older")
        self.assertEqual(self.check("--release", "0.1.0")[1]["status"], "newer")

    def test_a_patch_difference_is_current(self):
        self.install()
        major, minor = toolcopy.release_version().split(".")[:2]
        code, result = self.check("--release", f"{major}.{minor}.99")
        self.assertEqual((code, result["status"]), (0, "current"), result)
        source = fake_source(self.tmp / "source", f"{major}.{minor}.99")
        self.assertEqual(self.check("--source", str(source))[1]["status"], "current")

    def test_a_newer_patch_in_the_wiki_is_current(self):
        self.install()
        major, minor = toolcopy.release_version().split(".")[:2]
        manifest = self.repo / ".wiki-llm/manifest.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["release_version"] = f"{major}.{minor}.99"
        manifest.write_text(json.dumps(data), encoding="utf-8")
        code, result = self.check("--release", f"{major}.{minor}.0")
        self.assertEqual((code, result["status"]), (0, "current"), result)

    def test_release_option_must_be_a_version(self):
        self.install()
        code, result = self.check("--release", "two")
        self.assertEqual(code, 2)
        self.assertIn("not a version", result["error"])

    def test_source_and_release_are_exclusive(self):
        self.install()
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            self.check("--release", "2.0.0", "--source", str(self.tmp))

    def test_check_takes_the_repository_as_an_argument(self):
        self.install()
        code, result = run("copy", "check", str(self.repo))
        self.assertEqual((code, result["status"]), (0, "current"))

    def test_a_copy_does_not_install_over_itself(self):
        self.install()
        out = subprocess.run(
            ["python3", str(self.repo / ".wiki-llm/tools/wiki_llm.py"), "copy", "install", str(self.repo)],
            cwd=self.repo, capture_output=True, text=True,
        )
        self.assertEqual(out.returncode, 2, out.stderr)
        self.assertEqual(self.check()[1]["status"], "current")

    def test_damaged_manifest(self):
        self.install()
        (self.repo / ".wiki-llm/manifest.json").write_text("{}", encoding="utf-8")
        code, result = self.check()
        self.assertEqual(code, 2)
        self.assertIn("damaged", result["error"])

    def test_install_replaces_an_edited_copy(self):
        self.install()
        (self.repo / ".wiki-llm/tools/extra.py").write_text("x\n", encoding="utf-8")
        self.install()
        self.assertEqual(self.check()[1]["status"], "current")


class InitTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name) / "acme-wiki"

    def tearDown(self):
        self._tmp.cleanup()

    def init(self, *extra):
        return run("init", str(self.repo), "--app", "shop", "--title", "Shop: the store", "--owner-team", "web", *extra)

    def test_init_writes_a_valid_wiki_repository(self):
        code, result = self.init()
        self.assertEqual(code, 0, result)
        self.assertTrue(result["validate"]["ok"])
        for path in ("README.md", ".gitignore", ".wiki-llm/manifest.json",
                     "wiki/index.md", "wiki/shop/overview.md", "wiki/shop/index.md"):
            self.assertTrue((self.repo / path).is_file(), path)
        self.assertIn(".worktrees/", (self.repo / ".gitignore").read_text(encoding="utf-8").split("\n"))
        self.assertEqual(run("--root", str(self.repo / "wiki"), "validate")[0], 0)
        overview = (self.repo / "wiki/shop/overview.md").read_text(encoding="utf-8")
        self.assertIn('title: "Shop: the store"', overview)
        self.assertIn("# Architecture\n\nNone", overview)

    def test_init_writes_nothing_for_one_agent(self):
        code, result = self.init()
        self.assertEqual(code, 0, result)
        self.assertFalse((self.repo / ".claude").exists())
        readme = (self.repo / "README.md").read_text(encoding="utf-8")
        self.assertIn("sdlc-skills", readme)
        self.assertNotIn("plugin", readme.lower())
        overview = (self.repo / "wiki/shop/overview.md").read_text(encoding="utf-8")
        self.assertIn(f"by: wiki-llm/{toolcopy.release_version()}", overview)

    def test_init_keeps_existing_files(self):
        self.repo.mkdir(parents=True)
        (self.repo / "README.md").write_text("# Mine\n", encoding="utf-8")
        (self.repo / ".gitignore").write_text("node_modules/", encoding="utf-8")
        code, result = self.init()
        self.assertEqual(code, 0, result)
        self.assertEqual((self.repo / "README.md").read_text(encoding="utf-8"), "# Mine\n")
        self.assertEqual((self.repo / ".gitignore").read_text(encoding="utf-8"), "node_modules/\n.worktrees/\n__pycache__/\n")
        self.assertIn("README.md", result["kept"])

    def test_bad_title_stops_init_before_any_write(self):
        code, result = run("init", str(self.repo), "--app", "shop", "--title", 'Say "hi"', "--owner-team", "web")
        self.assertEqual(code, 2)
        self.assertFalse(self.repo.exists())

    def test_init_refuses_an_existing_wiki(self):
        self.init()
        code, result = self.init()
        self.assertEqual(code, 1)
        self.assertIn("exists", result["error"])

    def test_application_key_must_be_a_name(self):
        code, result = run("init", str(self.repo), "--app", "Shop", "--title", "Shop", "--owner-team", "web")
        self.assertEqual(code, 2)
        self.assertIn("--app", result["error"])

    def test_init_does_not_touch_git(self):
        self.init()
        self.assertFalse((self.repo / ".git").exists())


class AppAddTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name) / "acme-wiki"
        code, result = run("init", str(self.repo), "--app", "shop", "--title", "Shop", "--owner-team", "web")
        self.assertEqual(code, 0, result)

    def tearDown(self):
        self._tmp.cleanup()

    def add(self, key="billing", title="Billing: invoices", team="finance"):
        with contextlib.chdir(self.repo / "wiki"):
            return run("app", "add", "--key", key, "--title", title, "--owner-team", team)

    def test_adds_an_application(self):
        code, result = self.add()
        self.assertEqual(code, 0, result)
        self.assertTrue(result["validate"]["ok"])
        self.assertIn("wiki/billing/overview.md", result["written"])
        self.assertIn("wiki/index.md", result["written"])
        overview = (self.repo / "wiki/billing/overview.md").read_text(encoding="utf-8")
        self.assertIn('title: "Billing: invoices"', overview)
        self.assertIn("ownerTeam: finance", overview)
        self.assertIn(f"by: wiki-llm/{toolcopy.release_version()}", overview)
        self.assertIn("# Architecture\n\nNone", overview)
        self.assertIn("billing", (self.repo / "wiki/index.md").read_text(encoding="utf-8"))
        self.assertEqual(run("--root", str(self.repo / "wiki"), "validate")[0], 0)

    def test_refuses_an_existing_application(self):
        code, result = self.add(key="shop")
        self.assertEqual(code, 1)
        self.assertIn("exists", result["error"])

    def test_key_must_be_a_name(self):
        code, result = self.add(key="Billing")
        self.assertEqual(code, 2)
        self.assertIn("--key", result["error"])
        self.assertFalse((self.repo / "wiki/Billing").exists())

    def test_bad_title_writes_nothing(self):
        code, result = self.add(title='Say "hi"')
        self.assertEqual(code, 2)
        self.assertFalse((self.repo / "wiki/billing").exists())


if __name__ == "__main__":
    unittest.main()
