# Reading the project wiki to close a Task

This file says how `sdlc-close-task` finds the project's wiki repository and
reads the Task, its parent, the other Tasks of the parent, and the Design
files in its scope.

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
at `READ` (`write-protocol.md`, section 3).

## 3. Find your way around

The wiki in `wiki/` holds one folder per Application. In each, every concept is
one file or one folder named by its key, for example
`wiki/shop/features/FEAT-coupons/TASK-coupon-api.md`.

- **Find the Task.**
  `git ls-tree -r --name-only "$DEFAULT" -- wiki | grep '/TASK-<name>.md$'`.
- **Forward.** Follow the relative links in the Task's `# Planned scope` to
  read each Design file it covers, and read the parent's `overview.md` and the
  other `TASK-*.md` files in the same folder.
- **Not live yet.** Each Design file in scope has a `# Pending changes`
  section listing the Features and ChangeRequests whose work on that concept
  is not live yet.

## 4. The schema

What a type's file must contain, which headings the tool writes, and what each
status means are defined in the schema pages of the wiki's own tool copy:
`.wiki-llm/schema/schema.md` ("Pending changes") and
`.wiki-llm/schema/<type>.md` for each type (`task.md`, `feature.md`,
`change-request.md`, and each Design type in the Task's scope). Read the page
of a type before you rely on a heading or a status. Never guess them from
memory.

Two statuses matter to this skill:

- A Feature is `Draft`, then `ReqApproved`, then `Approved`, then `InDev`,
  `Released`, `Deprecated`.
- A ChangeRequest is `Proposed`, then `ReqApproved`, then `Approved`, then
  `Implemented`; or `Rejected`.

While the parent is `Draft`, `Proposed` or `ReqApproved`, closing a Task
leaves the Design files' `# Pending changes` entries and the parent's status
as they are until the parent is approved.
