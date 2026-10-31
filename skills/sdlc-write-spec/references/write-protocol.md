# Writing a spec draft to the project wiki

This file says how `sdlc-write-spec` drafts, checks, approves and commits its
changes to the wiki. `SKILL.md` says what to write; this file says how.

Read `read-protocol.md` and `flow.md` next to this file first.

## 1. The rules

- Every change goes into a **draft**: a branch `wiki/spec-<Key>` with its own
  worktree in `WIKI/.worktrees/spec-<Key>/`. The default branch changes only
  when the user merges the draft's pull request.
- One lifecycle step is one draft and one pull request. This step reads only
  what earlier steps merged into the default branch.
- Stop at the three **approval gates** of `flow.md`: Intent, Design and
  Change-set. No draft is started before the Intent gate is approved.
- Never merge, never open a pull request, never call a hosting service; the
  user does that.
- Edit only what a person writes. Never edit an `index.md`, a TestSuite's
  `checklist.csv` or a section the schema page marks as written by the tool;
  `draft finish` writes those.
- Never edit another step's output, except the story fix (`user-story.md`),
  the Task fix (`task.md`) and the TestCase fix (`test-case.md`) when a
  revision removes a Requirement (`SKILL.md`, section 4). When you find that a
  later step's output is out of date, name the skill to run again. Adding or
  removing a `# References` entry on a file this run writes is allowed.
- Keys are names taken from titles, never numbers: `FEAT-gift-cards`,
  `CR-gift-card-expiry`, `REQ-gift-cards-redeem-at-checkout`. A key on the
  default branch never changes. Before the pull request is merged,
  `$T rename <old> <new>` changes one.

## 2. Check the versions

This skill's folder has a file `RELEASE` next to its `SKILL.md`, holding one
line such as `1.0.0`. Compare it with the wiki's tool copy before anything
else:

```bash
cd "$WIKI" && $T copy check --release "<the line in RELEASE>"
```

| `status` | Do |
|---|---|
| `current` | Go on |
| `older` | Stop: "The wiki's tool is older than this skill. Run sdlc-setup-wiki to upgrade the wiki." |
| `newer` | Stop: "The wiki was set up by a newer release. Update your installed sdlc-skills." |
| `edited` | Stop: "The wiki's tool copy was edited by hand. Run sdlc-setup-wiki to restore it." |

## 3. The draft key

The key is `spec-<Key>`: `spec-` followed by the key of the Feature or
ChangeRequest (`spec-FEAT-coupons`, `spec-CR-gift-card-expiry`).

**First, look for a worktree.** When `WIKI/.worktrees/spec-<Key>/` exists, an
earlier run started this draft and did not commit it. Never discard it and
never start it again: a draft with no commit yet passes the "merged" test of
case 3 below, and its files and its `plan.md` exist nowhere else.

- It holds a `plan.md`: `cd` into it and resume as `flow.md`, section 5
  ("Resuming") says.
- It holds no `plan.md`: show the user `git status` in it and ask whether to
  go on from those files or to discard them.

Otherwise decide what to do after `git fetch --quiet origin 2>/dev/null`:

1. **The step's input is not on the default branch.** Stop. If
   `git branch -a --list 'wiki/*-<Key>' 'remotes/origin/wiki/*-<Key>'` shows the
   draft that holds it, say: "<Key> is in draft `wiki/<that branch>`, not on
   `<default>`. Merge its pull request first." Otherwise name the skill that
   writes the input.
2. **`wiki/spec-<Key>` exists and is not merged** into the default branch
   (`git merge-base --is-ancestor wiki/spec-<Key> "$DEFAULT"` fails). This is
   a revision, for example after review: `$T draft resume spec-<Key>`. Tell
   the user that new commits join any pull request open for that branch.
3. **`wiki/spec-<Key>` exists and is merged.** Run
   `$T draft discard spec-<Key> --remote`, then `$T draft start spec-<Key>`.
   Everything on that branch is already on the default branch, so deleting it
   loses nothing. If your environment refuses the deletion, ask the user to run
   the same `draft discard` command, then continue.
4. **Otherwise** `$T draft start spec-<Key>`.

## 4. The draft at each step

The steps are those of `flow.md`, section 1:

1. **Look up, questions, Intent gate.** Read the input on the default branch
   (`read-protocol.md`, section 2). `ls "$WIKI"/.worktrees/*/plan.md 2>/dev/null`
   lists the runs that stopped part-way; when one is for this request, resume
   it (section 3) and skip to the step its Run plan has reached. Otherwise no
   draft exists yet.
2. **Draft.** Choose `spec-<Key>` and start or resume the draft (section 3).
   Then:

   ```bash
   cd "$WIKI/.worktrees/spec-<Key>"
   READ=$(git rev-parse "$DEFAULT")
   ```

   Read the input again here, from the default branch at `READ`. For a new
   draft the worktree is that commit; a resumed draft also holds its own
   earlier commits, which are not input. Write the Run plan to `plan.md` in
   this folder, the root of the worktree. Git ignores it there.
3. **Design gate.** On rejection, stop: a draft started in this run is removed
   with `cd "$WIKI" && $T draft discard spec-<Key>`; a resumed draft is never
   discarded, whatever this run has written into it.
4. **Write** the files under `wiki/` in the worktree. Follow the schema page of
   each type you write (`.wiki-llm/schema/<type>.md`). Add an entry to the
   `log.md` of every concept folder you change, under today's date, newest
   first:

   ```markdown
   ## 2026-10-02

   * **Spec**: Wrote the PRD and 4 Requirements; version 1, status Draft. Written by an AI model with sdlc-write-spec.
   ```

   A change to `# References` only is logged as a **References** entry. A new
   or changed Reference needs a person's approval of its whole folder; the
   Design and Change-set gates are that approval.

5. **Input check.** Check whether the input changed on the default branch
   since you read it:

   ```bash
   git fetch --quiet origin 2>/dev/null
   git diff --quiet "$READ" "$DEFAULT" -- <the input paths> || git diff --stat "$READ" "$DEFAULT" -- <the input paths>
   ```

   If it changed, show the user what changed and go back to step 3. Do not
   merge the default branch in here: `$T refresh` is for a pull request that
   has conflicts (section 5).
6. **Self review, then finish.** Do the self review of `flow.md`, section 6.
   Then stamp, check and validate:

   ```bash
   $T draft finish --by "sdlc-write-spec/<the line in RELEASE>" --verified-by
   ```

   `--verified-by` without a value records the person in
   `git config user.email` as having confirmed the files; their approval at the
   gates is that confirmation. If `ok` is false, fix what `missing_logs` and
   `validate.errors` report and run it again. Never record a model name.
7. **Change-set gate.** Run `$T draft diff`. Show the files it lists (those
   marked `authored: false` were written by the tool), a commit message, and
   what the self review could not fix. Ask for approval. A change returns to
   step 4, or to step 3 if the design changes.
8. **Commit, then the summary.**

   ```bash
   $T draft commit -m "<message>"; cd "$WIKI"
   ```

   Run both in one command: `draft commit` removes the worktree you are in,
   and the `plan.md` with it. Judge the result by the JSON it prints (`ok`,
   `branch`, `pushed`), not by an error about the current directory. In the
   summary, "Done" names the branch `wiki/spec-<Key>` and says the user opens
   the pull request. If there is no remote, say the branch must be pushed
   first.

## 5. When a step goes wrong

| Situation | Do |
|---|---|
| `draft start` says the branch exists | Use section 3 again; never delete a draft that is not merged |
| The pull request has conflicts, because another draft was merged first | `$T draft resume spec-<Key>` if the worktree is gone, then `$T refresh` in it. It resolves conflicts in tool-written files itself; for a file a person writes it stops and names it: resolve it with git and run `$T refresh` again |
| `refresh` reports `ids.duplicate-key` or `ids.requirement-collision` | Another draft chose the same key: `$T rename <old> <new>` (with `--change CR-x` for a Requirement inside one ChangeRequest), then `$T refresh` |
| `draft finish` says `git config user.email` is not set | Ask the user for the id to record, and pass it: `--verified-by human:<id>` |
| `draft commit` refuses because files changed after `finish` | Run step 6 again |
| The user abandons the change | `cd "$WIKI" && $T draft discard spec-<Key> --remote` |
