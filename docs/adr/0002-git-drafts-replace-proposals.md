# Git draft branches replace the proposal overlay

The v1 tool staged every skill write in a temporary overlay (`proposal init / stage / validate / summarize / apply`) so a rejected change left no trace. Under v2 a skill writes a Draft on its own branch in a git worktree, the tool's `draft` commands stamp, sync, validate, diff, commit and push it, and the user opens the pull request themselves; git already provides the isolation, the diff and the discard that the overlay rebuilt by hand. The three approval gates (Intent, Design, Change-set) are unchanged; approval at the Change-set gate permits the commit and push of the Draft branch, and the merge of the pull request is the change reaching the default branch.

## Consequences

- The tool owns the git steps (`draft start | resume | finish | diff | commit | discard`, `refresh`, `verify`) so they are covered by its tests, not re-described in every skill.
- Generated files (`index.md`, reverse sections) conflict between parallel pull requests; `refresh` resolves those conflicts by regenerating and stops on conflicts in authored files.
