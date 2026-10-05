import unittest

from wikilib.schema import Schema

HEADING_KEYS = {
    "name", "presence", "origin", "allow_none", "none_statuses", "nested", "links", "mermaid",
    "requirements", "table", "generated",
}
FIELD_KINDS = {
    "string", "enum", "boolean", "integer", "uri", "timestamp", "date",
    "actor_stamp", "actor_stamps", "sources", "string_list",
}


class SchemaFileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = Schema.load()

    def test_versions(self):
        self.assertEqual(self.schema.version, "1")
        self.assertEqual(self.schema.okf_version, "0.2")

    def test_every_collection_type_exists(self):
        for collection in self.schema.collections:
            for name in collection["types"]:
                self.assertIn(name, self.schema.types)
                self.assertEqual(self.schema.types[name]["place"], {"kind": "collection", "dir": collection["dir"]})

    def test_every_owned_type_names_its_owner(self):
        for name, spec in self.schema.types.items():
            for owned in spec.get("owns", []):
                self.assertIn(name, self.schema.types[owned]["place"]["owners"], f"{name} owns {owned}")

    def test_every_link_target_is_a_known_type(self):
        known = set(self.schema.types) | {"Requirement"}
        for name in self.schema.types:
            for path, links in self.schema.link_headings(name):
                for target in self.schema.targets(links):
                    self.assertIn(target, known, f"{name} {path}")
                if "qualifier" in links:
                    self.assertIn(links["qualifier"]["set"], self.schema.qualifiers)

    def test_every_generated_source_heading_exists(self):
        for name, spec in self.schema.types.items():
            for heading in spec.get("headings", []):
                for source in heading.get("generated", {}).get("sources", []):
                    self.assertIsNotNone(
                        self.schema.heading(source["type"], source["heading"]),
                        f"{name} # {heading['name']} mirrors a missing heading",
                    )

    def test_heading_and_field_specs_use_known_keys(self):
        def walk(entries):
            for entry in entries:
                self.assertLessEqual(set(entry), HEADING_KEYS, entry["name"])
                self.assertIn(entry["presence"], {"required", "optional", "conditional"})
                walk(entry.get("nested", []))

        for name in self.schema.types:
            walk(self.schema.headings(name))
            for field, spec in self.schema.fields(name).items():
                self.assertIn(spec["kind"], FIELD_KINDS, f"{name}.{field}")
                if spec["kind"] == "enum":
                    self.assertTrue(spec["values"], f"{name}.{field}")

    def test_design_types_share_one_status_set_and_pending_heading(self):
        for name in self.schema.design_types:
            self.assertEqual(
                self.schema.types[name]["statuses"],
                ["Planned", "Active", "Modifying", "Removing", "Deprecated"],
            )
            self.assertEqual(self.schema.headings(name)[-1]["name"], "Pending changes")

    def test_design_token_expands(self):
        links = self.schema.heading("Task", ["Planned scope"])["links"]
        self.assertEqual(self.schema.targets(links), self.schema.design_types)

    def test_endpoint_response_requires_status_codes(self):
        response = self.schema.heading("Endpoint", ["Response"])
        self.assertEqual(response["nested"], [{"name": "Status codes", "presence": "required"}])


class LookupTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = Schema.load()

    def test_type_for_key_uses_prefix(self):
        datastores = self.schema.collection("datastores")["types"]
        self.assertEqual(self.schema.type_for_key(datastores, "CACHE-session"), "Cache")
        self.assertEqual(self.schema.type_for_key(datastores, "DB-shop"), "Database")
        self.assertIsNone(self.schema.type_for_key(datastores, "QUEUE-x"))

    def test_type_for_key_falls_back_to_the_prefixless_type(self):
        owned = self.schema.owned_types("Feature")
        self.assertEqual(self.schema.type_for_key(owned, "TASK-pay-001"), "Task")
        self.assertEqual(self.schema.type_for_key(owned, "prd"), "Reference")

    def test_type_for_key_uses_fixed_filenames(self):
        owned = self.schema.owned_types("Application")
        self.assertEqual(self.schema.type_for_key(owned, "glossary"), "Glossary")
        self.assertEqual(self.schema.type_for_key(owned, "architecture-overview"), "Reference")
        self.assertEqual(self.schema.type_for_key(self.schema.owned_types("TestSuite"), "test-plan"), "Reference")
        self.assertIsNone(self.schema.type_for_key(self.schema.owned_types("Service"), "notes"))

    def test_fields_merge_common_type_and_status(self):
        fields = self.schema.fields("Service")
        self.assertTrue(fields["resource"]["required"])
        self.assertTrue(fields["generated"]["required"])
        self.assertEqual(fields["status"]["values"][1], "Active")
        self.assertNotIn("status", self.schema.fields("TestCase"))

    def test_key_pattern(self):
        self.assertEqual(self.schema.key_pattern("ChangeRequest"), "^CR-[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertEqual(self.schema.key_pattern("ArchitectureDecision"), "^ADR-[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertEqual(self.schema.key_pattern("Task"), "^TASK-[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertEqual(self.schema.key_pattern("Service"), "^SVC-[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertIsNone(self.schema.key_pattern("Reference"))

    def test_nested_heading_lookup(self):
        spec = self.schema.heading("ChangeRequest", ["Delta", "Target delta"])
        self.assertEqual(spec["links"]["qualifier"], {"set": "change", "required": True})
        self.assertIsNone(self.schema.heading("ChangeRequest", ["Delta", "Nope"]))


if __name__ == "__main__":
    unittest.main()
