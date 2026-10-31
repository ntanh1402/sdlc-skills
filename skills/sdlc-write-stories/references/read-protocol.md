# Reading the project wiki

This file says how `sdlc-write-stories` finds the project's wiki repository
and reads the target's Requirements, PRD, stories and Tasks.

## 1. Find the wiki repository

A wiki repository is a git repository with the wiki in `wiki/` and a copy of
the checking tool in `.wiki-llm/`. Find it in this order:

1. **The current folder.** If the current folder, or a folder above it, holds
   both `.wiki-llm/manifest.json` and `wiki/index.md`, that folder is the wiki
   repository.
2. **The workspace note.** Otherwise look in your instructions for the note
   between `<!-- sdlc-skills:start -->` and `<!-- sdlc-skills:end -->`. It names the
   wiki repository's path, relative to the file that holds the note, and the
   command that runs its tool.
3. **Neither.** Stop and tell the user: "No project wiki is linked to this
   folder. Run sdlc-setup-wiki in this folder first." Never ask the user for a
   path; only sdlc-setup-wiki takes one.

Below, `WIKI` is the wiki repository's folder and `T` is its tool, run from
inside `WIKI` or from inside the draft worktree:

```bash
cd "$WIKI"
T="python3 .wiki-llm/tools/wiki_llm.py"
```

The tool prints JSON. Exit 0 is success, 1 a failed check or a refusal, 2 a
usage or environment problem.

## 2. Read the default branch

The default branch is the only source of truth. Find it and bring it up to
date:

```bash
git fetch --quiet origin 2>/dev/null
DEFAULT=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD \
  || { git show-ref --verify --quiet refs/heads/main && echo main; } \
  || echo master)
```

This is the same rule the tool uses: the remote's default branch, else a
local `main`, else `master`.

- If the checkout is on `$DEFAULT` and `git status -sb` does not say it is
  behind, read the files directly.
- Otherwise read the default branch without switching the checkout:
  `git show "$DEFAULT:wiki/<path>"` for a file and
  `git grep -l "<text>" "$DEFAULT" -- wiki/` for a search.

Once the draft worktree is started, read the input inside the draft worktree
at `READ` (`write-protocol.md`, section 4).

## 3. Find your way around

The wiki in `wiki/` holds one folder per Application. In each, every concept is
one file or one folder named by its key, for example
`wiki/shop/features/FEAT-checkout/overview.md`.

- **Start from the indexes.** `wiki/index.md` lists Applications;
  `wiki/<app>/index.md` lists what an Application has;
  `wiki/<app>/features/index.md` has one line per Feature. Every `index.md` is
  written by the tool.
- **Forward.** A link is a relative path. Follow it.
- **Backward.** Open the target and read its tool-written section: a Feature
  story's `# Changed by`, a Feature's `# Change history`. For anything else,
  search for the key: `grep -rl "STORY-checkout" wiki/ --include='*.md'`.
- **References.** Follow the `# References` section of the target Feature or
  ChangeRequest (its PRD is linked there) and scan
  `wiki/<app>/references/index.md` for References about the subject. Read a
  Reference's `overview.md` first, then open its content file (`prd.md` or
  `change-prd.md`) for the actors and goals. A Reference is context: it never
  overrides a Requirement.
- **Coverage and outdated.** `$T coverage stories --feature FEAT-x` (or
  `--change CR-x`) lists Functional Requirements that are not **Wont** and that
  no story lists. `$T outdated --feature FEAT-x` (or `--change CR-x`) lists
  stories written from an older version of the spec.
- **History.** Read the concept folder's `log.md`, then `git log -p` on the
  folder's `overview.md` to compare Requirements across versions.

## 4. The schema

What a type's file must contain, which headings the tool writes, and what each
status means are defined in the schema pages of the wiki's own tool copy:
`.wiki-llm/schema/schema.md` for the common rules and
`.wiki-llm/schema/<type>.md` for each type, for example
`.wiki-llm/schema/user-story.md`. Read the page of a type before you rely on a
heading or a status. Never guess them from memory.

Two statuses matter to this skill:

- A Feature is `Draft`, then `ReqApproved`, then `Approved`, then `InDev`,
  `Released`, `Deprecated`.
- A ChangeRequest is `Proposed`, then `ReqApproved`, then `Approved`, then
  `Implemented`; or `Rejected`.

`Draft`, `Proposed` and `ReqApproved` are not gates: user stories may be
written while the Requirements are still a draft, and each story records the
spec `version` it was written from in `basedOn`.
