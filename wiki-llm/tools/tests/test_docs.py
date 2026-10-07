import tempfile
import unittest
from pathlib import Path

from wikilib import docs
from wikilib.schema import Schema

PAGE = "# {title}\n\nHand-written introduction.\n\n" + docs.START + "\nold table\n" + docs.END + "\n\n## Rules\n\nHand-written rules.\n"


class DocsTest(unittest.TestCase):
    def setUp(self):
        self.schema = Schema.load()
        self._tmp = tempfile.TemporaryDirectory()
        self.directory = Path(self._tmp.name)
        for name, spec in self.schema.types.items():
            (self.directory / spec["page"]).write_text(PAGE.format(title=name), encoding="utf-8")
        (self.directory / docs.CATALOG_PAGE).write_text(PAGE.format(title="Schema"), encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def page(self, name):
        return (self.directory / name).read_text(encoding="utf-8")

    def test_write_fills_every_page_and_keeps_prose(self):
        changed = docs.write(self.schema, self.directory)
        self.assertEqual(len(changed), len(self.schema.types) + 1)
        text = self.page("service.md")
        self.assertTrue(text.startswith("# Service\n\nHand-written introduction.\n\n"))
        self.assertTrue(text.endswith("\n\n## Rules\n\nHand-written rules.\n"))
        self.assertNotIn("old table", text)

    def test_write_is_idempotent(self):
        docs.write(self.schema, self.directory)
        self.assertEqual(docs.write(self.schema, self.directory), [])
        self.assertEqual(docs.stale(self.schema, self.directory), [])

    def test_hand_edit_inside_the_block_is_stale(self):
        docs.write(self.schema, self.directory)
        path = self.directory / "service.md"
        path.write_text(path.read_text(encoding="utf-8").replace("`serviceType`", "`kind`"), encoding="utf-8")
        self.assertEqual(docs.stale(self.schema, self.directory), [path])

    def test_page_without_markers_is_stale_and_left_alone(self):
        path = self.directory / "task.md"
        path.write_text("# Task\n\nNo markers.\n", encoding="utf-8")
        self.assertNotIn(path, docs.write(self.schema, self.directory))
        self.assertIn(path, docs.stale(self.schema, self.directory))
        self.assertEqual(path.read_text(encoding="utf-8"), "# Task\n\nNo markers.\n")

    def test_missing_page_is_stale(self):
        (self.directory / "task.md").unlink()
        self.assertIn(self.directory / "task.md", docs.stale(self.schema, self.directory))

    def test_type_block_lists_fields_from_the_schema(self):
        block = docs.type_block(self.schema, "Service")
        self.assertIn("| Status | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |", block)
        self.assertIn("| `serviceType` | yes | lower-case words joined by `-`; common: `api`, `worker`, `cron`, `consumer`, `gateway` |", block)
        self.assertIn("| `resource` | yes | URL or bundle path |", block)
        self.assertIn("| `generated` | yes | `{ by, at }` |", block)
        self.assertLess(block.index("`status`"), block.index("`serviceType`"))
        self.assertLess(block.index("`healthcheckPath`"), block.index("`generated`"))

    def test_type_block_lists_headings_links_and_qualifiers(self):
        block = docs.type_block(self.schema, "Service")
        self.assertIn("| `# <title>` | required; first heading | author |  |  |  |", block)
        self.assertIn("| `# Uses` | optional | author | Cache, BlobStore, SearchIndex (any number) | `read`, `write`, `rw` (required) |  |", block)
        self.assertIn("| `# Depends on` | optional | author | ExternalService (any number) | `critical` (optional) |  |", block)
        self.assertIn("| `# Pending changes` | conditional | author | Feature, ChangeRequest (1 or more) | `new`, `modified`, `removed` (required) |  |", block)
        self.assertLess(block.index("`# References`"), block.index("`# Pending changes`"))

    def test_every_type_may_link_references_before_its_tool_sections(self):
        row = "| `# References` | optional | author | Reference (any number) |  |  |"
        for name in self.schema.types:
            self.assertIn(row, docs.type_block(self.schema, name), name)
        feature = docs.type_block(self.schema, "Feature")
        self.assertLess(feature.index("`# References`"), feature.index("`# Change history`"))

    def test_type_block_shows_nested_and_generated_headings(self):
        change = docs.type_block(self.schema, "ChangeRequest")
        self.assertIn("| `# Changes` | required | author | Feature (exactly 1) |  |  |", change)
        self.assertIn("| `## Target delta` | required | author | any Design type (1 or more) | `new`, `modified`, `removed` (required) |  |", change)
        table = docs.type_block(self.schema, "Table")
        self.assertIn("| `# Used by` | always | tool | mirrors Service `# Reads`, Service `# Writes` |  |  |", table)
        decision = docs.type_block(self.schema, "ArchitectureDecision")
        self.assertIn("| `# Superseded by` | when not empty | tool | mirrors ArchitectureDecision `# Supersedes` |  |  |", decision)

    def test_type_block_states_the_content_a_heading_needs(self):
        self.assertIn("| Heading | Presence | Written by | Links to | Qualifier | Content |", docs.type_block(self.schema, "Glossary"))
        glossary = docs.type_block(self.schema, "Glossary")
        self.assertIn("| `# Terms` | required; may be `None` | author |  |  | table with columns `Term`, `Definition` |", glossary)
        self.assertIn("| `# Roles` | required; may be `None` | author |  |  | table with columns `Role`, `Description` |", glossary)
        feature = docs.type_block(self.schema, "Feature")
        self.assertIn("| `# Requirements` | required | author |  |  | 1 or more `### REQ-*` entries |", feature)
        self.assertIn("| `## High-level architecture` | required | author |  |  | Mermaid `flowchart` diagram |", feature)
        self.assertIn("| `## Runtime sequences` | required | author |  |  | Mermaid `sequenceDiagram` diagram |", feature)
        self.assertIn("| `# Architecture` | required; may be `None` | author |  |  | `None` only while status is `Draft` or `ReqApproved` |", feature)
        change = docs.type_block(self.schema, "ChangeRequest")
        self.assertIn("| `# Requirements` | required | author |  |  | any number of `### REQ-*` entries |", change)
        self.assertIn("| `# Delta` | required; may be `None` | author |  |  | `None` only while status is `Proposed` or `ReqApproved` or `Rejected` |", change)
        case = docs.type_block(self.schema, "TestCase")
        self.assertIn("| `# Steps` | required | author |  |  | table with columns `Step`, `Action`, `Expected result`, `Validation` |", case)
        endpoint = docs.type_block(self.schema, "Endpoint")
        self.assertIn("| `# Flowchart` | required | author |  |  | Mermaid `flowchart` diagram |", endpoint)
        self.assertIn("| `# Sequence diagram` | required | author |  |  | Mermaid `sequenceDiagram` diagram |", endpoint)

    def test_content_cell_joins_several_rules(self):
        spec = {"name": "Parts", "presence": "required", "table": ["A", "B"], "mermaid": "flowchart", "none_statuses": ["Draft"]}
        row = docs._heading_rows(self.schema, [spec], 1)[0]
        self.assertEqual(row[-1], "table with columns `A`, `B`; Mermaid `flowchart` diagram; `None` only while status is `Draft`")

    def test_links_cell_shows_every_minimum_and_maximum(self):
        def cell(links):
            return docs._heading_rows(self.schema, [{"name": "Owner", "presence": "optional", "links": {"targets": ["Service"], **links}}], 1)[0][3]

        self.assertEqual(cell({"min": 0}), "Service (any number)")
        self.assertEqual(cell({"min": 2}), "Service (2 or more)")
        self.assertEqual(cell({"min": 1, "max": 1}), "Service (exactly 1)")
        self.assertEqual(cell({"min": 0, "max": 1}), "Service (0 to 1)")

    def test_document_types_and_fixed_titles(self):
        self.assertIn("| Status | None; this type has no `status` field |", docs.type_block(self.schema, "TestCase"))
        convention = docs.type_block(self.schema, "Convention")
        self.assertIn("Any other headings are allowed.", convention)
        reference = docs.type_block(self.schema, "Reference")
        self.assertIn("| Status | `Active`, `Deprecated` |", reference)
        self.assertIn("| Shape | Folder with `index.md`, `overview.md`, `log.md`, and any content files and folders |", reference)
        self.assertIn("| `verified` | yes, by a `human:` actor | `{ by, at }`, or a list of them |", reference)
        self.assertIn("| `# Contents` | required; may be `None` | author |  |  |  |", reference)
        self.assertIn("| `# Referenced by` | always | tool | mirrors any type `# References` |  |  |", reference)
        self.assertNotIn("Any other headings are allowed.", reference)
        channel = docs.type_block(self.schema, "MessageChannel")
        self.assertIn("| `# Overview` | required; first heading | author |  |  |  |", channel)
        self.assertIn("| `## Dead letter` | required | author |  |  |  |", channel)
        self.assertIn("| Shape | Folder with `index.md`, `overview.md`, `log.md`, `payload.example.json` |", channel)
        self.assertIn("| Shape | Folder with `index.md`, `overview.md` |", docs.type_block(self.schema, "Application"))

    def test_catalog_lists_every_type_once_with_design_types_and_qualifiers(self):
        block = docs.catalog_block(self.schema)
        for name, spec in self.schema.types.items():
            self.assertEqual(block.count(f"| {name} | ["), 1, name)
            self.assertIn(f"]({spec['page']})", block)
        self.assertIn("**Design types:** Service, WebFrontend,", block)
        self.assertIn("| change | `new`, `modified`, `removed` |", block)

    def test_broken_links(self):
        (self.directory / "service.md").write_text(
            "[ok](task.md) [gone](nope.md) [web](https://example.com) [anchor](#rules) [frag](task.md#x)\n\n```md\n[code](fenced.md)\n```\n",
            encoding="utf-8",
        )
        (self.directory / "okf-spec.md").write_text("[example](/tables/customers.md)\n", encoding="utf-8")
        self.assertEqual(docs.broken_links(self.directory), [(self.directory / "service.md", "nope.md")])


if __name__ == "__main__":
    unittest.main()
