import unittest

from wikilib import frontmatter


def doc(block: str, body: str = "# Title\n") -> str:
    return f"---\n{block}\n---\n{body}"


class ParseTest(unittest.TestCase):
    def test_scalars_keep_their_text(self):
        meta, body, errors = frontmatter.parse(doc('type: Service\nversion: "16"\nport: 8080'))
        self.assertEqual(errors, [])
        self.assertEqual(meta, {"type": "Service", "version": "16", "port": "8080"})
        self.assertEqual(body, "# Title\n")

    def test_scalar_with_braces_inside_is_a_scalar(self):
        meta, _, errors = frontmatter.parse(doc("keyPattern: product:{product_id} | category:tree"))
        self.assertEqual(errors, [])
        self.assertEqual(meta["keyPattern"], "product:{product_id} | category:tree")

    def test_flow_list(self):
        meta, _, errors = frontmatter.parse(doc("tags: [sales, orders]"))
        self.assertEqual(errors, [])
        self.assertEqual(meta["tags"], ["sales", "orders"])

    def test_flow_mapping(self):
        meta, _, errors = frontmatter.parse(doc("generated: { by: human:ntanh, at: 2026-10-01T09:00:00Z }"))
        self.assertEqual(errors, [])
        self.assertEqual(meta["generated"], {"by": "human:ntanh", "at": "2026-10-01T09:00:00Z"})

    def test_block_list_of_flow_mappings(self):
        block = "verified:\n  - { by: human:a, at: 2026-10-01T09:00:00Z }\n  - { by: process:nightly, at: 2026-10-02T09:00:00Z }"
        meta, _, errors = frontmatter.parse(doc(block))
        self.assertEqual(errors, [])
        self.assertEqual([entry["by"] for entry in meta["verified"]], ["human:a", "process:nightly"])

    def test_block_list_of_block_mappings(self):
        block = "sources:\n  - id: openapi\n    resource: https://example.com/openapi.yaml\n    title: Orders OpenAPI\n  - resource: prd.md\nstatus: Active"
        meta, _, errors = frontmatter.parse(doc(block))
        self.assertEqual(errors, [])
        self.assertEqual(
            meta["sources"],
            [
                {"id": "openapi", "resource": "https://example.com/openapi.yaml", "title": "Orders OpenAPI"},
                {"resource": "prd.md"},
            ],
        )
        self.assertEqual(meta["status"], "Active")

    def test_windows_line_endings(self):
        text = "---\r\ntype: Service\r\ngenerated: { by: human:a, at: 2026-10-01T09:00:00Z }\r\n---\r\n# Title\r\n"
        meta, body, errors = frontmatter.parse(text)
        self.assertEqual(errors, [])
        self.assertEqual(meta["type"], "Service")
        self.assertEqual(meta["generated"]["by"], "human:a")
        self.assertIn("# Title", body)

    def test_leading_byte_order_mark_is_ignored(self):
        meta, body, errors = frontmatter.parse("\ufeff" + doc("type: Service"))
        self.assertEqual(errors, [])
        self.assertEqual(meta, {"type": "Service"})
        self.assertEqual(body, "# Title\n")

    def test_missing_block_is_an_error(self):
        meta, body, errors = frontmatter.parse("# Title\n")
        self.assertEqual(meta, {})
        self.assertEqual(body, "# Title\n")
        self.assertEqual(errors, ["missing or unterminated frontmatter block"])

    def test_unterminated_block_is_an_error(self):
        _, _, errors = frontmatter.parse("---\ntype: Service\n# Title\n")
        self.assertEqual(errors, ["missing or unterminated frontmatter block"])

    def test_unquoted_colon_space_is_rejected(self):
        _, _, errors = frontmatter.parse(doc("title: Incident: data freshness"))
        self.assertEqual(errors, ["title: value must be quoted: Incident: data freshness"])

    def test_quoted_colon_space_is_accepted(self):
        meta, _, errors = frontmatter.parse(doc('title: "Incident: data freshness"'))
        self.assertEqual(errors, [])
        self.assertEqual(meta["title"], "Incident: data freshness")

    def test_json_string_value_is_rejected(self):
        _, _, errors = frontmatter.parse(doc('columns: \'[{"name": "id"}]\'\nschema: {"a": 1'))
        self.assertIn("columns: structured data belongs in the body", errors)
        self.assertTrue(any(error.startswith("schema: value must be quoted") for error in errors))

    def test_nested_structure_is_rejected(self):
        _, _, errors = frontmatter.parse(doc("sources:\n  - id: a\n    nested:\n      deep: 1"))
        self.assertTrue(errors)

    def test_duplicate_key_is_rejected(self):
        _, _, errors = frontmatter.parse(doc("status: Active\nstatus: Planned"))
        self.assertEqual(errors, ["status: duplicate key"])

    def test_empty_value_is_rejected(self):
        _, _, errors = frontmatter.parse(doc("status:\ntype: Service"))
        self.assertEqual(errors, ["status: empty value"])


if __name__ == "__main__":
    unittest.main()
