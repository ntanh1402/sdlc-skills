# sdlc-setup-wiki

Create a project wiki, upgrade it, link a folder to it, or add an Application.
[Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | Tech lead (anyone who sets up or upgrades the project) |
| **Use when** | You start a project wiki; link another folder to an existing wiki; add an Application; or another skill says the wiki is older than the skills, was edited by hand, cannot be found, or has no such Application |
| **Needs first** | Nothing |
| **Say** | "Set up the project wiki at ../shop-wiki", "Add application billing to the wiki", "Upgrade the wiki" |
| **You get** | A wiki repository with `wiki/` and a tool copy `.wiki-llm/`, plus a note in your workspace's `AGENTS.md` (and `CLAUDE.md`) that tells the other skills where the wiki is |
| **Next** | Push a new wiki repository to your git host. Run the skill again from every other folder that should use the same wiki |

## What the skill does

1. Asks where the wiki is (a path, for example `../shop-wiki`) unless the
   workspace note already says.
2. Checks the wiki's tool copy and picks one of four jobs: **create**,
   **upgrade**, **link only**, or **add an application**.
3. Shows what it will write and asks for approval.
4. Writes it, either as the first commit on `main` (a brand-new wiki) or as a
   draft branch for a pull request (anything else).
5. Writes the note into the workspace's `AGENTS.md` and `CLAUDE.md`.

It does nothing before you approve, never edits `.wiki-llm/` by hand, never
pushes to `main` of a repository that already has commits, and never opens a
pull request.

## What you do

- Give the Application key (lower-case words joined by `-`, for example
  `shop`), its title, and the owner team when asked.
- Approve what will be written, then approve the change set.
- Merge the pull request, or push the new wiki repository.
- Commit the note in `AGENTS.md` / `CLAUDE.md` if your teammates should share
  it.

## Scenarios

| What happens | What the skill does | What you do |
|---|---|---|
| **A new project.** The wiki folder does not exist, is not a git repository, or has no commits | Asks for the Application key, title and owner team. Creates `README.md`, `.gitignore` lines, `.wiki-llm/`, `wiki/index.md` and `wiki/<app>/overview.md`, and commits them as the first commit on `main` | Approve, then push `main` to a new remote |
| **The wiki already has commits** and has no tool copy | Writes the skeleton on a draft branch `wiki/setup` | Merge the pull request |
| **The workspace is the wiki repository itself** | Puts the workspace note through a draft too, because the note belongs in that repository | Merge the pull request |
| **Another folder should use the same wiki** and the wiki is up to date | Only writes the note into that folder's `AGENTS.md` / `CLAUDE.md`. If the note is already there it says "already linked" | Commit the note if teammates should share it |
| **You updated the skills** and the wiki is older | Shows the old and new release, and whether the schema version changes. Writes the new tool copy on `wiki/setup-<version>`; if the schema changes it also migrates the wiki files | Approve, then merge the pull request |
| **Someone edited `.wiki-llm/` by hand** | Lists the added, missing and changed files and says they will be replaced | Check the list. If a change was deliberate, stop and talk to the person who made it. Otherwise approve |
| **The wiki was set up by a newer release** than your skills | Refuses and writes nothing | Update your skills (`git pull`, run `install-skills.sh`), then run again |
| **An earlier upgrade branch still exists.** Its pull request is merged or closed | Discards the old branch and starts again | Approve |
| **An earlier upgrade's pull request is still open** | Stops | Finish that pull request first |
| **No migration exists** for the schema jump | Tells you the wiki cannot be upgraded with this release and discards its draft | Ask the maintainers of the skills for a release that migrates your wiki |
| **Add an Application.** The wiki is current | Asks for key, title and owner team. Writes `wiki/<key>/overview.md` and the indexes on `wiki/app-<key>` | Approve, merge the pull request |
| **The Application key already exists** | Says so, offers another key, starts nothing | Give a different key |
| **Add an Application, but the wiki is not current** | Upgrades first | Merge the upgrade, then ask again |
| **The wiki's own checks fail** after writing (a new tool can report problems the old one did not) | Shows the errors, discards the draft and stops. It does not repair wiki content | Fix the reported content by hand (see the [runbook](../runbook.md)), then run again |
| **The repository has no default branch** (`main`, `master`, or a remote default) | Tells you it needs one, and stops | Create one |
| **You reject the change set** | Discards the draft | Nothing |

## Not this skill

| Request | Use |
|---|---|
| Writing requirements, design, tasks or tests | The skills in [the flow](user-guide.md#the-flow) |
| Fixing wiki content | [sdlc-edit-wiki](sdlc-edit-wiki.md), or the lifecycle skill that owns it |
