# Self review runs in a read-only sub-agent, and sdlc-import has none

When the agent that just wrote a draft's files reads its own output for the step 6 self review, the conversation and the Design-gate draft sit in its context window, so it tends to see what it meant to write rather than what is on disk. On 2026-10-31 the owner decided that the six writing skills that generate files after one Design gate (`sdlc-write-spec`, `sdlc-write-stories`, `sdlc-design-arch`, `sdlc-plan-tasks`, `sdlc-design-tests` and `sdlc-build-task`) run their reading checks in a fresh read-only sub-agent, given only the worktree path (with `plan.md` and the written files), the upstream wiki input paths and the skill's checklist — never the conversation history. `sdlc-import` drops its self-review step and `## Self review` section altogether, because it shows and writes every file in full group by group at the Design gate, and `draft finish` validates the schema and links before the Change-set gate.

## Considered Options

- **Keep self review in the main agent.** Requires no sub-agent dispatch, but suffers from author bias because the main agent's context already holds the intended output.
- **Let the sub-agent edit files and run tool commands directly.** Give write and shell access to the sub-agent. Rejected because read-only sub-agents work across more agent runtimes, cannot accidentally break draft protocol rules or touch out-of-scope files, and leave sole write ownership of the worktree, `plan.md` and gate transitions with the main agent.

## Consequences

- In the six skills, the sub-agent checks the files by reading only and returns what it checked and its findings; the main agent runs any CLI `$T` checks (`coverage`, `outdated`, `validate`), applies fixes in the worktree in a single pass, and records `checked:` and `fixed:` under `## Self review` in `plan.md`.
- If an agent runtime cannot spawn sub-agents, the skill falls back to doing the same review directly by reading the files from disk, keeping ADR 0003's agent-neutrality rule intact.
- `sdlc-import`, `sdlc-edit-wiki` and `sdlc-close-task` have no self-review step and no `## Self review` section in `plan.md`.
