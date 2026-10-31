# Reading the project wiki for a code review

This file says how `sdlc-review-code` finds the project's wiki repository and
reads its contracts and Tasks on the default branch.

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

Below, `WIKI` is the wiki repository's folder:

```bash
cd "$WIKI"
```

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
- In the review report, always name the wiki branch and short commit hash you
  read (`git rev-parse --short "$DEFAULT"`).

## 3. Find your way around

The wiki in `wiki/` holds one folder per Application. In each, every concept is
one file or one folder named by its key, for example
`wiki/shop/services/SVC-orders/EP-refund.md`.

- **Start from the indexes.** `wiki/index.md` lists Applications;
  `wiki/<app>/index.md` lists what an Application has. Every `index.md` is
  written by the tool.
- **Forward.** A link is a relative path. Follow it.
- **Backward.** Open the target and read its tool-written section: a Table's
  `# Used by`, a Channel's `# Publishers` and `# Subscribers`, a Feature's
  `# Change history`. For anything else, search for the key:
  `grep -rl "SVC-orders" wiki/ --include='*.md'`.
- **References.** Follow the `# References` section of the Task and of every
  Design concept you read, and read each entry's note. Read a Reference's
  `overview.md` first; open a content file or `resource` only when needed. A
  Reference is context, never a contract (`code-checks.md`).
- **Not live yet (`# Pending changes`).** A Design file with a
  `# Pending changes` section holds the **target**: what the system will be
  once the pending work is built. Review the code against the target, using
  the ownership rules of `SKILL.md` section 3.
- **History.** Read the concept folder's `log.md`, then `git log -p` on the
  folder.

## 4. The schema

What a type's file must contain, which headings the tool writes, and what each
status means are defined in the schema pages of the wiki's own tool copy:
`.wiki-llm/schema/schema.md` for the common rules and
`.wiki-llm/schema/<type>.md` for each type, for example
`.wiki-llm/schema/endpoint.md` or `.wiki-llm/schema/task.md`. Read the page of
a type before you rely on a heading or a status. Never guess them from memory.
