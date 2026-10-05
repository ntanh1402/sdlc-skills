import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import wiki_llm

from . import fixture


def run(*argv: str) -> tuple[int, dict]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = wiki_llm.main(list(argv))
    return code, json.loads(buffer.getvalue())


class CliTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = fixture.make_bundle(Path(self._tmp.name) / "bundle")

    def tearDown(self):
        self._tmp.cleanup()

    def test_validate_clean_bundle(self):
        code, result = run("--root", str(self.root), "validate")
        self.assertEqual((code, result), (0, {"ok": True, "errors": [], "warnings": []}))

    def test_validate_reports_errors_and_exits_1(self):
        fixture.edit(self.root, "pay/services/SVC-pay/overview.md", "status: Active", "status: Stable")
        code, result = run("--root", str(self.root), "validate")
        self.assertEqual(code, 1)
        self.assertFalse(result["ok"])
        self.assertEqual(result["errors"][0]["rule"], "frontmatter.bad-value")
        self.assertEqual(result["errors"][0]["path"], "pay/services/SVC-pay/overview.md")

    def test_warning_alone_keeps_exit_0(self):
        fixture.edit(self.root, "pay/services/SVC-pay/overview.md", "serviceType: api", "serviceType: api\nstale_after: 2020-01-01T00:00:00Z")
        code, result = run("--root", str(self.root), "validate")
        self.assertEqual(code, 0)
        self.assertEqual([item["rule"] for item in result["warnings"]], ["stale.expired"])

    def test_sync_check_then_sync(self):
        fixture.edit(self.root, "pay/services/SVC-pay/overview.md", "description: Takes payments.", "description: Takes card payments.")
        code, result = run("--root", str(self.root), "sync", "--check")
        self.assertEqual(code, 1)
        self.assertEqual(result["stale"], ["pay/services/SVC-pay/index.md", "pay/services/index.md"])
        code, result = run("--root", str(self.root), "sync")
        self.assertEqual((code, result["written"]), (0, ["pay/services/SVC-pay/index.md", "pay/services/index.md"]))
        self.assertEqual(run("--root", str(self.root), "sync", "--check"), (0, {"ok": True, "stale": [], "skipped": []}))

    def test_sync_lists_the_files_it_skips(self):
        rel = "pay/datastores/DB-main/TBL-payments.md"
        fixture.edit(self.root, rel, "# Schema", "```sql\nopen fence\n\n# Schema")
        fixture.edit(self.root, "pay/services/SVC-pay/overview.md", "# Writes\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md)\n\n", "")
        code, result = run("--root", str(self.root), "sync", "--check")
        self.assertEqual(result["skipped"], [rel])
        code, result = run("--root", str(self.root), "sync")
        self.assertEqual(result["skipped"], [rel])

    def test_root_comes_from_the_environment(self):
        with mock.patch.dict(os.environ, {"WIKI_LLM_ROOT": str(self.root)}):
            code, _ = run("validate")
        self.assertEqual(code, 0)

    def test_explicit_root_wins_over_the_environment(self):
        with mock.patch.dict(os.environ, {"WIKI_LLM_ROOT": "/nonexistent"}):
            code, _ = run("--root", str(self.root), "validate")
        self.assertEqual(code, 0)

    def test_directory_that_is_not_a_bundle(self):
        code, result = run("--root", self._tmp.name, "validate")
        self.assertEqual(code, 2)
        self.assertIn("not a bundle", result["error"])


class DiscoveryTest(unittest.TestCase):
    """Without --root or WIKI_LLM_ROOT the tool walks up from the current directory."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name) / "acme-wiki"
        self.root = fixture.make_bundle(self.repo / "wiki")
        self._env = mock.patch.dict(os.environ)
        self._env.start()
        os.environ.pop("WIKI_LLM_ROOT", None)

    def tearDown(self):
        self._env.stop()
        self._tmp.cleanup()

    def test_finds_the_wiki_folder_from_the_repository_root(self):
        with contextlib.chdir(self.repo):
            self.assertEqual(run("validate")[0], 0)

    def test_finds_the_bundle_from_inside_it(self):
        with contextlib.chdir(self.root / "pay" / "services" / "SVC-pay"):
            self.assertEqual(run("validate")[0], 0)

    def test_no_bundle_above_the_current_directory(self):
        empty = Path(self._tmp.name) / "empty"
        empty.mkdir()
        with contextlib.chdir(empty):
            code, result = run("validate")
        self.assertEqual(code, 2)
        self.assertEqual(result["error"], "no bundle found: run from inside a wiki repository or pass --root")

    def test_schema_version_mismatch_stops_the_command(self):
        fixture.edit(self.root, "index.md", 'schema_version: "1"', 'schema_version: "0"')
        for command in (["validate"], ["sync"], ["sync", "--check"]):
            code, result = run("--root", str(self.root), *command)
            self.assertEqual(code, 2)
            self.assertEqual(
                result["error"],
                "bundle is schema 0, this tool is schema 1: run `wiki_llm.py migrate` (sdlc-setup-wiki does this)",
            )

    def test_index_without_schema_version_is_not_a_bundle(self):
        fixture.edit(self.root, "index.md", 'schema_version: "1"\n', "")
        code, result = run("--root", str(self.root), "validate")
        self.assertEqual(code, 2)
        self.assertIn("no schema_version", result["error"])

    def test_migrate_says_no_migration_exists(self):
        fixture.edit(self.root, "index.md", 'schema_version: "1"', 'schema_version: "0"')
        code, result = run("--root", str(self.root), "migrate")
        self.assertEqual(code, 1)
        self.assertEqual(result["error"], "no migration from schema 0 to 1 is available in this version")

    def test_migrate_on_a_current_bundle_changes_nothing(self):
        code, result = run("--root", str(self.root), "migrate")
        self.assertEqual((code, result), (0, {"ok": True, "from": "1", "to": "1", "written": []}))


class DocsCommandTest(unittest.TestCase):
    """The generator is tested in test_docs.py; these pin the command's own output and exit codes."""

    def test_docs_check_clean(self):
        with mock.patch.object(wiki_llm.docs, "stale", return_value=[]), mock.patch.object(wiki_llm.docs, "broken_links", return_value=[]):
            code, result = run("docs", "--check")
        self.assertEqual((code, result), (0, {"ok": True, "stale": [], "broken_links": []}))

    def test_docs_check_reports_stale_pages_and_broken_links(self):
        stale = [Path("/x/service.md")]
        broken = [(Path("/x/schema.md"), "missing.md")]
        with mock.patch.object(wiki_llm.docs, "stale", return_value=stale), mock.patch.object(wiki_llm.docs, "broken_links", return_value=broken):
            code, result = run("docs", "--check")
        self.assertEqual((code, result), (1, {"ok": False, "stale": ["service.md"], "broken_links": ["schema.md: missing.md"]}))

    def test_docs_writes_changed_pages(self):
        pages = {Path("/x/service.md"): "text", Path("/x/table.md"): "text"}
        with mock.patch.object(wiki_llm.docs, "write", return_value=[Path("/x/service.md")]), mock.patch.object(wiki_llm.docs, "render", return_value=pages):
            code, result = run("docs")
        self.assertEqual((code, result), (0, {"ok": True, "written": ["service.md"], "missing_markers": []}))

    def test_docs_reports_pages_without_markers(self):
        pages = {Path("/x/service.md"): "text", Path("/x/table.md"): None}
        with mock.patch.object(wiki_llm.docs, "write", return_value=[]), mock.patch.object(wiki_llm.docs, "render", return_value=pages):
            code, result = run("docs")
        self.assertEqual((code, result), (1, {"ok": False, "written": [], "missing_markers": ["table.md"]}))


if __name__ == "__main__":
    unittest.main()
