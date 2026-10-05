import unittest

from wikilib import markdown

BODY = """# Orders Service

Intro prose.

# Reads

* [TBL-carts](../../datastores/DB-shop/TBL-carts.md) — the cart an order is
  built from, see [carts](x.md).
* [TBL-customers](../../datastores/DB-shop/TBL-customers.md)

# Uses

* [CACHE-session](../../datastores/CACHE-session/overview.md) — rw — sessions.

# Architecture

## Services

* [SVC-cart](../SVC-cart/overview.md) — supplies the cart.

## Runtime sequences

```mermaid
sequenceDiagram
  A->>B: call
```

```yaml
# not a heading
link: [not a link](nowhere.md)
```
"""


class HeadingTest(unittest.TestCase):
    def test_headings_skip_code_fences(self):
        titles = [heading.title for heading in markdown.headings(BODY)]
        self.assertEqual(
            titles,
            ["Orders Service", "Reads", "Uses", "Architecture", "Services", "Runtime sequences"],
        )

    def test_section_ends_at_next_heading_of_same_or_higher_level(self):
        reads = markdown.section(BODY, "Reads")
        self.assertIn("TBL-carts", reads.text)
        self.assertNotIn("CACHE-session", reads.text)

    def test_nested_section_is_found_inside_its_parent(self):
        architecture = markdown.section(BODY, "Architecture")
        services = markdown.section(BODY, "Services", level=2, within=architecture)
        self.assertIn("SVC-cart", services.text)
        self.assertNotIn("sequenceDiagram", services.text)

    def test_missing_section_is_none(self):
        self.assertIsNone(markdown.section(BODY, "Writes"))


class FenceTest(unittest.TestCase):
    def titles(self, body):
        return [heading.title for heading in markdown.headings(body)]

    def test_fenced_heading_is_not_a_heading(self):
        self.assertEqual(self.titles("# Real\n\n```sh\n# not a heading\n```\n"), ["Real"])

    def test_tilde_line_inside_a_backtick_fence_is_content(self):
        self.assertEqual(self.titles("```\n~~~\n# not a heading\n```\n\n# Real\n"), ["Real"])

    def test_backtick_line_inside_a_tilde_fence_is_content(self):
        self.assertEqual(self.titles("~~~\n```\n# not a heading\n~~~\n\n# Real\n"), ["Real"])

    def test_longer_outer_fence_wraps_a_shorter_one(self):
        body = "````md\n```\n# not a heading\n```\n# still not a heading\n````\n\n# Real\n"
        self.assertEqual(self.titles(body), ["Real"])

    def test_longer_line_of_the_same_character_closes_a_fence(self):
        self.assertEqual(self.titles("```\n# not a heading\n`````\n\n# Real\n"), ["Real"])

    def test_fence_line_followed_by_text_does_not_close(self):
        self.assertEqual(self.titles("```\n```sh\n# not a heading\n```\n\n# Real\n"), ["Real"])

    def test_unclosed_fence_runs_to_the_end_and_is_named(self):
        body = "# Real\n\n```mermaid\nflowchart LR\n\n# not a heading\n"
        self.assertEqual(self.titles(body), ["Real"])
        self.assertEqual(markdown.unclosed_fence(body), "```mermaid")

    def test_closed_fences_are_not_reported(self):
        self.assertIsNone(markdown.unclosed_fence(BODY))

    def test_fence_indented_four_spaces_is_code_not_a_fence(self):
        body = "# Real\n\n    ```\n\n# Also real\n"
        self.assertEqual(self.titles(body), ["Real", "Also real"])
        self.assertIsNone(markdown.unclosed_fence(body))

    def test_fence_indented_three_spaces_is_a_fence(self):
        self.assertEqual(self.titles("# Real\n\n   ```\n# not a heading\n   ```\n"), ["Real"])


class LooseItemTest(unittest.TestCase):
    def test_numbered_and_nested_links_are_loose(self):
        text = "1. [A](a.md)\n\n  * [B](b.md) — note\n"
        self.assertEqual(markdown.loose_items(text), ["1. [A](a.md)", "* [B](b.md) — note"])

    def test_checkboxes_are_not_loose(self):
        text = "1. [ ] confirm the index\n\n  * [x] done\n  - [ ] later\n"
        self.assertEqual(markdown.loose_items(text), [])


class ItemTest(unittest.TestCase):
    def test_item_uses_first_link_and_joins_continuation_lines(self):
        first = markdown.items(markdown.section(BODY, "Reads").text)[0]
        self.assertEqual(first.label, "TBL-carts")
        self.assertEqual(first.target, "../../datastores/DB-shop/TBL-carts.md")
        self.assertEqual(first.segments, ("the cart an order is built from, see [carts](x.md).",))

    def test_item_without_note_has_no_segments(self):
        second = markdown.items(markdown.section(BODY, "Reads").text)[1]
        self.assertEqual(second.segments, ())

    def test_qualifier_is_the_first_segment(self):
        item = markdown.items(markdown.section(BODY, "Uses").text)[0]
        self.assertEqual(item.segments, ("rw", "sessions."))

    def test_item_without_link(self):
        item = markdown.items("* plain text\n")[0]
        self.assertEqual((item.label, item.target, item.segments), ("", "", ()))

    def test_prose_is_not_an_item(self):
        self.assertEqual(markdown.items("None yet.\n"), [])


class LinkTest(unittest.TestCase):
    def test_links_skip_code_fences_and_images(self):
        targets = [target for _, target in markdown.links(BODY + "\n![shot](shot.png)\n")]
        self.assertNotIn("nowhere.md", targets)
        self.assertNotIn("shot.png", targets)
        self.assertIn("x.md", targets)

    def test_links_can_include_images(self):
        targets = [target for _, target in markdown.links("![shot](shot.png) [a](a.md)", images=True)]
        self.assertEqual(targets, ["shot.png", "a.md"])

    def test_links_skip_inline_code_but_keep_code_labels(self):
        text = "Write `* [label](path)` like [`orders`](TBL-orders.md)."
        self.assertEqual(markdown.links(text), [("`orders`", "TBL-orders.md")])

    def test_slug_matches_github_anchors(self):
        self.assertEqual(markdown.slug("REQ-checkout-1"), "req-checkout-1")
        self.assertEqual(markdown.slug("Context and constraints"), "context-and-constraints")
        self.assertEqual(markdown.slug("`# Calls` rules!"), "-calls-rules")


class TableTest(unittest.TestCase):
    def test_table_returns_header_and_rows(self):
        header, rows = markdown.table("text\n\n| Step | Action |\n|---|---|\n| 1 | Go |\n| 2 | Stop |\n\nafter | x |\n")
        self.assertEqual(header, ["Step", "Action"])
        self.assertEqual(rows, [["1", "Go"], ["2", "Stop"]])

    def test_no_table(self):
        self.assertEqual(markdown.table("nothing here"), ([], []))

    def test_mermaid_kinds(self):
        self.assertEqual(markdown.mermaid_kinds(BODY), ["sequenceDiagram"])

    def test_is_none(self):
        self.assertTrue(markdown.is_none("\nNone — pending architecture\n"))
        self.assertFalse(markdown.is_none("\n* [x](y.md)\n"))


if __name__ == "__main__":
    unittest.main()
