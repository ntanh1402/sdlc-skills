# Each skill owns its reference files

Until 2026-10-31, `release.py` copied five generic files from `skill-shared/` (`flow.md`, `read-protocol.md`, `write-protocol.md`, `code-checks.md`, `paste-format.md`) into each skill's `references/`, and generated each `agents/openai.yaml` from `skill-shared/openai.json`. Skills differ in their flow (full, group by group, short, code worktree), draft key, cross-file edits and tool commands. The shared files therefore carried exceptions for some skills, and several `SKILL.md` files had to override them. The owner decided to delete `skill-shared/`: each skill folder holds its own `references/*.md` and `agents/openai.yaml`, written for that skill alone.

## Considered Options

- **Keep one shared copy per reference file.** One edit reaches every skill, but every skill reads rules that are not its own, plus the overrides that cancel them.
- **Move the flow into each `SKILL.md`.** No extra file would be needed, but the larger skills would pass the 500-line limit.

## Consequences

- A fault in a rule that several skills share is fixed in every skill's copy that has the rule; `grep -rn` over `skills/*/references/` finds them. No test keeps the copies identical, because they are meant to differ.
- `release.py` only writes `RELEASE` files and rebuilds the tool copy in `skills/sdlc-setup-wiki/wiki-llm/`.
- `test_release.py` checks that each skill holds the reference files its `SKILL.md` names and a valid `agents/openai.yaml`.
- This departs from the writing-for-agents advice to keep shared reference material in one external file. Here a skill is installed on its own, so it cannot read a file outside its folder.
