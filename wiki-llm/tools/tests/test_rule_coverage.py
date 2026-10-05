"""Every rule ID the tool can report is exercised by a test that names it."""

import re
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
RULE_RE = re.compile(r'Finding\(\s*"([a-z]+\.[a-z-]+)"')
PROBLEM_RE = re.compile(r'_problem\(\s*"([a-z]+\.[a-z-]+)"')
LITERAL_RE = re.compile(r'"((?:links|layout)\.[a-z-]+)"')


def reported_rules() -> set[str]:
    rules: set[str] = set()
    for path in sorted((TOOLS / "wikilib").rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        rules.update(RULE_RE.findall(text))
        rules.update(PROBLEM_RE.findall(text))
        rules.update(LITERAL_RE.findall(text))
    return rules


class RuleCoverageTest(unittest.TestCase):
    def test_every_rule_id_appears_in_a_test(self):
        tests = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((TOOLS / "tests").glob("test_*.py"))
            if path.name != Path(__file__).name
        )
        rules = reported_rules()
        self.assertGreaterEqual(len(rules), 35)
        missing = sorted(rule for rule in rules if f'"{rule}"' not in tests)
        self.assertEqual(missing, [], "rules with no test")


if __name__ == "__main__":
    unittest.main()
