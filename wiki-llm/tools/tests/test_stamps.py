"""Editing provenance fields and log entries in place."""

import unittest

from wikilib import frontmatter, stamps
from wikilib.schema import Schema

DOC = "---\ntype: Table\ntitle: payments\ngenerated: { by: human:alice, at: 2026-09-01T09:00:00Z }\n---\n\n# payments\n"
LIST = "---\ntype: Table\nverified:\n  - { by: human:a, at: 2026-09-01T09:00:00Z }\n  - { by: human:b, at: 2026-09-02T09:00:00Z }\ntitle: x\n---\n\n# x\n"
A = {"by": "human:carol", "at": "2026-10-01T10:00:00Z"}


class SetFieldTest(unittest.TestCase):
    def test_replaces_a_one_line_field_in_place(self):
        text = frontmatter.set_field(DOC, "generated", "{ by: skill/model, at: 2026-10-01T10:00:00Z }")
        self.assertIn("title: payments\ngenerated: { by: skill/model, at: 2026-10-01T10:00:00Z }\n---", text)

    def test_replaces_a_block_list_with_its_items(self):
        text = frontmatter.set_field(LIST, "verified", "{ by: human:c, at: 2026-10-01T10:00:00Z }")
        self.assertEqual(text, "---\ntype: Table\nverified: { by: human:c, at: 2026-10-01T10:00:00Z }\ntitle: x\n---\n\n# x\n")

    def test_removes_a_field(self):
        text = frontmatter.set_field(LIST, "verified", None)
        self.assertEqual(text, "---\ntype: Table\ntitle: x\n---\n\n# x\n")

    def test_adds_a_missing_field_at_the_end(self):
        text = frontmatter.set_field(DOC, "verified", "{ by: human:c, at: 2026-10-01T10:00:00Z }")
        self.assertTrue(text.startswith("---\ntype: Table\ntitle: payments\ngenerated: { by: human:alice, at: 2026-09-01T09:00:00Z }\nverified: "))

    def test_keeps_a_byte_order_mark(self):
        self.assertTrue(frontmatter.set_field("﻿" + DOC, "verified", None).startswith("﻿---\n"))


class VerifiedTest(unittest.TestCase):
    def test_first_stamp_is_a_mapping(self):
        text = stamps.add_verified(DOC, A)
        self.assertEqual(frontmatter.parse(text)[0]["verified"], A)

    def test_second_stamp_turns_the_mapping_into_a_list(self):
        text = stamps.add_verified(stamps.add_verified(DOC, {"by": "human:a", "at": "2026-09-01T09:00:00Z"}), A)
        meta, _, errors = frontmatter.parse(text)
        self.assertEqual(errors, [])
        self.assertEqual(meta["verified"], [{"by": "human:a", "at": "2026-09-01T09:00:00Z"}, A])


class AuthoredViewTest(unittest.TestCase):
    schema = Schema.load()

    def test_generated_sections_and_provenance_are_left_out(self):
        before = DOC + "\n# Schema\n\ntable\n\n# Used by\n\n* [SVC-a](a.md)\n"
        after = frontmatter.set_field(before, "generated", "{ by: x/y, at: 2026-10-01T10:00:00Z }").replace("SVC-a", "SVC-b")
        after = stamps.add_verified(after, A)
        self.assertEqual(stamps.authored_view(before, self.schema), stamps.authored_view(after, self.schema))

    def test_authored_text_counts(self):
        before = DOC + "\n# Schema\n\ntable\n"
        self.assertNotEqual(stamps.authored_view(before, self.schema), stamps.authored_view(before.replace("table", "rows"), self.schema))


LOG = "# Change log\n\n## 2026-09-01\n\n* **Creation**: Created.\n"


class LogTest(unittest.TestCase):
    def test_entries_are_date_and_text(self):
        self.assertEqual(stamps.log_entries(LOG), {("2026-09-01", "**Creation**: Created.")})

    def test_new_date_goes_first(self):
        text = stamps.add_log_entry(LOG, "2026-10-01", "**Verification**: Confirmed by human:bob.")
        self.assertEqual(
            text,
            "# Change log\n\n## 2026-10-01\n\n* **Verification**: Confirmed by human:bob.\n\n"
            "## 2026-09-01\n\n* **Creation**: Created.\n",
        )

    def test_a_date_between_two_others_goes_in_date_order(self):
        log = "# Change log\n\n## 2026-10-03\n\n* **Import**: Imported.\n\n## 2026-09-01\n\n* **Creation**: Created.\n"
        text = stamps.add_log_entry(log, "2026-10-02", "**Verification**: Confirmed by human:bob.")
        self.assertEqual(
            text,
            "# Change log\n\n## 2026-10-03\n\n* **Import**: Imported.\n\n"
            "## 2026-10-02\n\n* **Verification**: Confirmed by human:bob.\n\n"
            "## 2026-09-01\n\n* **Creation**: Created.\n",
        )

    def test_a_date_older_than_every_entry_goes_last(self):
        text = stamps.add_log_entry(LOG, "2026-08-01", "**Verification**: Confirmed by human:bob.")
        self.assertEqual(text, LOG + "\n## 2026-08-01\n\n* **Verification**: Confirmed by human:bob.\n")

    def test_existing_date_gets_another_bullet(self):
        text = stamps.add_log_entry(LOG, "2026-09-01", "**Verification**: Confirmed by human:bob.")
        self.assertEqual(text, LOG + "* **Verification**: Confirmed by human:bob.\n")

    def test_byte_order_mark_is_kept(self):
        self.assertTrue(stamps.add_log_entry("﻿" + LOG, "2026-10-01", "x").startswith("﻿# Change log\n\n## 2026-10-01"))


if __name__ == "__main__":
    unittest.main()
