# Reading the project wiki to build a Task

This file says how `sdlc-build-task` finds the project's wiki repository and
reads the Task, Design contracts, conventions and References on the default
branch.

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
inside `WIKI`:

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
git -C "$WIKI" fetch --quiet origin 2>/dev/null
DEFAULT=$(git -C "$WIKI" symbolic-ref --quiet --short refs/remotes/origin/HEAD \
  || { git -C "$WIKI" show-ref --verify --quiet refs/heads/main && echo main; } \
  || echo master)
```

This is the same rule the tool uses: the remote's default branch, else a
local `main`, else `master`.

- If the wiki checkout is on `$DEFAULT` and `git -C "$WIKI" status -sb` does
  not say it is behind, read the files directly.
- Otherwise read the default branch without switching the checkout:
  `git -C "$WIKI" show "$DEFAULT:wiki/<path>"` for a file and
  `git -C "$WIKI" grep -l "<text>" "$DEFAULT" -- wiki/` for a search.

## 3. Find your way around

The wiki in `wiki/` holds one folder per Application. In each, every concept is
one file or one folder named by its key, for example
`wiki/shop/features/FEAT-coupons/TASK-coupon-api.md`.

- **Start from the indexes.** `wiki/index.md` lists Applications;
  `wiki/<app>/index.md` lists what an Application has. Every `index.md` is
  written by the tool.
- **Forward.** A link is a relative path. Follow it.
- **Backward.** Open the target and read its tool-written section: a Table's
  `# Used by`, a Channel's `# Publishers` and `# Subscribers`, a Feature's
  `# Change history`. For anything else, search for the key:
  `grep -rl "SVC-orders" "$WIKI/wiki/" --include='*.md'`.
- **References.** A Reference is material a person approved to be read while
  working: a PRD, a domain page, a vendor's documentation, a code example.
  Find the ones that apply in two ways, and use both:
  - follow the `# References` section of the Task, its parent and every Design
    concept in scope, and read each entry's note: it says what to take from
    it;
  - scan `wiki/<app>/references/index.md`, one line per Reference with its
    title and description, for the ones about your scope.

  Read a Reference's `overview.md` first; open a content file or `resource`
  only when the work needs the detail. A Reference is context: it never
  overrides a Requirement, a contract or `conventions.md`, and a `Deprecated`
  one is read only to see what was replaced.
- **Outdated.** `$T outdated --feature FEAT-x` (or `--change CR-x`) lists
  Tasks written from an older version of the spec (`basedOn` older than
  `version`).
- **History.** Read the concept folder's `log.md`, then `git log -p` on the
  folder.

## 4. The schema

What a type's file must contain, which headings the tool writes, and what each
status means are defined in the schema pages of the wiki's own tool copy:
`.wiki-llm/schema/schema.md` for the common rules and
`.wiki-llm/schema/<type>.md` for each type, for example
`.wiki-llm/schema/task.md` or `.wiki-llm/schema/endpoint.md`. Read the page of
a type before you rely on a heading or a status. Never guess them from memory.

Two statuses matter to this skill:

- A Feature is `Draft`, then `ReqApproved`, then `Approved`, then `InDev`,
  `Released`, `Deprecated`.
- A ChangeRequest is `Proposed`, then `ReqApproved`, then `Approved`, then
  `Implemented`; or `Rejected`.

`Draft`, `Proposed` and `ReqApproved` are not gates: Tasks may be built while
the parent is not `Approved` yet, once the person confirms in the first round
(`SKILL.md`, section 1).
