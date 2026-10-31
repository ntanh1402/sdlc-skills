# Agent-neutral skills replace the Claude plugin

Sub-project 2 delivered the schema, the tool and the skills as one Claude Code plugin (`.claude-plugin/`, a marketplace, and `.claude/settings.json` in each Wiki repository). The owner wants the skills to work with any AI agent that reads skill folders, not only Claude Code. We therefore drop the plugin and publish a Release from this repository instead.
- A user installs its skills once into their agent's skills folder, with `install-skills.sh --agent <name> [--link]` or a third-party skill installer.
- `sdlc-wiki-setup` carries its own copy of the tool and installs it into each Wiki repository as the Tool copy.
- The setup skill links the folder the agent works in, the Workspace, to that Wiki repository by writing a note into the Workspace's agent instruction file.

## Considered Options

- **Keep the Claude plugin.** It works only in Claude Code.
- **Copy the working skills into each Wiki repository.** The skills would then always match the Tool copy, but no folder inside a repository is read by every agent, and every skill would exist in two places.
- **Keep a per-user config file listing the Wiki repositories.** It is extra state outside any repository that goes stale. The note in the Workspace's `AGENTS.md` or `CLAUDE.md` is already read by the agent.

## Consequences

- `.claude-plugin/` is removed, and `init` stops writing `.claude/settings.json`. **Release** and **Release version** replace Plugin and Plugin version. `copy check --plugin <dir>` becomes `--source <dir>`.
- `skills/sdlc-wiki-setup/wiki-llm/` holds a release copy of the tool:
  - its contents are `schema/`, `tools/` without tests, no sample, and `manifest.json`;
  - a release script makes it with `copy install`;
  - a test fails when it differs from the top-level `wiki-llm/`, which stays the only place the tool is edited.
- Each skill that runs the wiki's tool or depends on the schema carries a one-line `RELEASE` file, so a skill installed on its own still knows its version. `sdlc-doc-to-md` does not carry one. Before writing, such a skill compares its `RELEASE` with the Wiki repository's `.wiki-llm/manifest.json`:
  - if the wiki is older, it tells the user to run `sdlc-wiki-setup`;
  - if the wiki is newer, it tells the user to update their installed skills.
- `sdlc-wiki-setup` is started in a Workspace and given the path of a Wiki repository.
  - It creates the Wiki repository, upgrades it, or leaves it unchanged.
  - Then it runs a new tool command, `link`, which writes a marked `<!-- sdlc-skills:start -->` … `<!-- sdlc-skills:end -->` note into each `AGENTS.md` and `CLAUDE.md` that exists, or into a new `AGENTS.md` when neither does.
  - The note's path is relative when the two folders share a parent, otherwise absolute with a warning. A Workspace may be the Wiki repository itself.
- A working skill finds the Wiki repository from the current folder first, then from the Workspace note. If neither exists, it stops and tells the user to run `sdlc-wiki-setup` in that folder. Only setup ever takes a path from the user.
- No `SKILL.md` names a feature, command or folder that only one agent has, such as `/plugin`, Claude's "base directory" or `.claude/` paths. A skill finds files by paths relative to its own `SKILL.md`.
- A skill fix reaches a user when they update their installed skills. It reaches a Wiki repository only when the upgrade Draft that `sdlc-wiki-setup` prepares is merged.
