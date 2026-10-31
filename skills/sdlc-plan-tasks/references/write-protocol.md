# Writing a tasks draft to the project wiki

This file says how `sdlc-plan-tasks` drafts, checks, approves and commits its
changes to the wiki. `SKILL.md` says what to write; this file says how.
Read it when `SKILL.md` section 1 finds an unfinished draft, or at section 4.

## 1. The rules

- Every change goes into a **draft**: a branch `wiki/tasks-<Key>` with its own
  worktree in `WIKI/.worktrees/tasks-<Key>/`. The default branch changes only
  when the user merges the draft's pull request.
- One lifecycle step is one draft and one pull request. This step reads only
  what earlier steps merged into the default branch.
- Stop at the three **approval gates** of `SKILL.md`: Intent, Design and
  Change-set. No draft is started before the Intent gate is approved.
- Never merge, never open a pull request, never call a hosting service; the
  user does that.
- Edit only what a person writes. Never edit an `index.md` or a section the
  schema page marks as written by the tool; `draft finish` writes those.
- Never edit another step's output: write only `TASK-*.md` files in the
  target's folder and that folder's `log.md`. When you find a gap in the
  requirements or architecture, name the skill that owns it under `For other
  skills`.
- Keys are names taken from titles, never numbers: `TASK-refund-endpoint`. A
  key on the default branch never changes. Before the pull request is merged,
  `$T rename <old> <new>` changes one.

## 2. The draft key

The key is `tasks-<Key>`: `tasks-` followed by the key of the Feature or
ChangeRequest (`tasks-FEAT-coupons`, `tasks-CR-sms-alerts`).

**First, look for a worktree.** When `WIKI/.worktrees/tasks-<Key>/` exists, an
earlier run started this draft and did not commit it. Never discard it and
never start it again: a draft with no commit yet passes the "merged" test of
case 3 below, and its files and its `plan.md` exist nowhere else.

- It holds a `plan.md`: `cd` into it and resume as section 4 ("Resuming")
  says.
- It holds no `plan.md`: show the user `git status` in it and ask whether to
  go on from those files or to discard them.

Otherwise decide what to do after `git fetch --quiet origin 2>/dev/null`:

1. **The step's input is not on the default branch.** Stop. If
   `git branch -a --list 'wiki/*-<Key>' 'remotes/origin/wiki/*-<Key>'` shows the
   draft that holds it, say: "<Key> is in draft `wiki/<that branch>`, not on
   `<default>`. Merge its pull request first." Otherwise name
   `sdlc-design-arch`.
2. **`wiki/tasks-<Key>` exists and is not merged** into the default branch
   (`git merge-base --is-ancestor wiki/tasks-<Key> "$DEFAULT"` fails). This is
   a revision, for example after review: `$T draft resume tasks-<Key>`. Tell
   the user that new commits join any pull request open for that branch.
3. **`wiki/tasks-<Key>` exists and is merged.** Run
   `$T draft discard tasks-<Key> --remote`, then `$T draft start tasks-<Key>`.
   Everything on that branch is already on the default branch, so deleting it
   loses nothing. If your environment refuses the deletion, ask the user to run
   the same `draft discard` command, then continue.
4. **Otherwise** `$T draft start tasks-<Key>`.

## 3. The commands of each section

Each part is for the section of `SKILL.md` it names.

### At section 4: Run plan and the Design gate

Start or resume `tasks-<Key>` (section 2). Then:

```bash
cd "$WIKI/.worktrees/tasks-<Key>"
READ=$(git rev-parse "$DEFAULT")
```

Read the input again here, from the default branch at `READ`. For a new draft
the worktree is that commit; a resumed draft also holds its own earlier commits,
which are not input. Write the Run plan (section 4) to `plan.md` in this folder,
the root of the worktree. Git ignores it there.

When the person rejects the design, remove a draft this run started:

```bash
cd "$WIKI" && $T draft discard tasks-<Key>
```

### At section 5: Write

Write the Task files under `wiki/` in the worktree, following
`.wiki-llm/schema/task.md`. Add an entry to the folder's `log.md`, under
today's date, newest first:

```markdown
## 2026-10-02

* **Tasks**: Planned 5 Tasks in 3 waves. Written by an AI model with sdlc-plan-tasks.
```

Then the **input check**: has the input changed on the default branch
since you read it?

```bash
git fetch --quiet origin 2>/dev/null
git diff --quiet "$READ" "$DEFAULT" -- <the input paths> || git diff --stat "$READ" "$DEFAULT" -- <the input paths>
```

If it changed, show the user what changed and go back to the Design gate. Do not
merge the default branch in here: `$T refresh` is for a pull request that
has conflicts (section 6).

### At section 6: Self review, finish and commit

Do the self review (section 5 of this file).
Then stamp, check and validate:

```bash
$T draft finish --by "sdlc-plan-tasks/<the line in RELEASE>" --verified-by
```

`--verified-by` without a value records the person in
`git config user.email` as having confirmed the files; their approval at the
gates is that confirmation. If `ok` is false, fix what `missing_logs` and
`validate.errors` report and run it again. Never record a model name.

**Change-set gate.** Run `$T draft diff`. Show the files it lists (those marked
`authored: false` were written by the tool), a commit message, and what the self
review could not fix. Ask for approval. A change returns to the writing, or to
the Design gate if the task plan changes.

On approval:

```bash
$T draft commit -m "<message>"; cd "$WIKI"
```

Run both in one command: `draft commit` removes the worktree you are in,
and the `plan.md` with it. Judge the result by the JSON it prints (`ok`,
`branch`, `pushed`), not by an error about the current directory. In the
summary, "Done" names the branch `wiki/tasks-<Key>` and says the user opens
the pull request. If there is no remote, say the branch must be pushed
first.

## 4. The Run plan

The Run plan is the list of things this run has to do, with what is done so
far. It is the file `plan.md` at the root of the draft worktree. A run can end
before it is finished, and the next session has no memory of the
conversation; the file is what it starts from.

```markdown
# Run plan: sdlc-plan-tasks, FEAT-coupons
Intent approved 2026-10-03 · Design approved 2026-10-03

## Answers
1. Two Tasks: TASK-coupon-api in orders-service, then TASK-coupon-ui in shop-web.

## Assumed
- DB migration for TBL-coupons is part of TASK-coupon-api.

## Files
- [x] features/FEAT-coupons/TASK-coupon-api.md (add: TBL-coupons and EP-apply-coupon)
- [ ] features/FEAT-coupons/TASK-coupon-ui.md (add: WEB-storefront coupon input)
- [ ] features/FEAT-coupons/log.md (change: Tasks log entry)

## Self review
- checked: coverage tasks reports nothing; every Task has current basedOn
- fixed: added # Stories link on TASK-coupon-api

## For other skills
- Missing Reference for coupon code format: sdlc-edit-wiki
```

- `## Answers` holds what the person decided in the rounds. `## Assumed` holds
  what you decided without asking; the person reads it at the Design gate.
- `## Files` has one line per file: the path, whether it is added, changed or
  deleted, and what changes. Tick a file when it is written. The checkboxes
  are the only status.
- Do not copy the task plan into the file. Show the task plan in full in the
  chat at the Design gate. A text that is written twice says two different
  things sooner or later.
- Add "Design approved" with the date when the Design gate is approved.
- Leave out a heading that has nothing under it.
- Git ignores the file. It is never committed and goes when the worktree goes.

**Resuming.** Do not ask the rounds again. Show the plan and ask one question:
"does this plan still stand?". On yes, continue at the first unticked file;
work out what it says from the answers, its line in the plan and the files
already written, then go on to the self review. Any change the person makes
reopens the Design gate: show the task plan again before writing.

## 5. Self review

After the last file is written, run a fresh read-only sub-agent to review the
output from disk (if the environment cannot run sub-agents, do the review
yourself by reading the files from disk). Give the sub-agent only the worktree
path (holding `plan.md` and the written files), the upstream input files in
`$WIKI/wiki/` (verified unchanged by the input check), and these checks — not
the conversation history:

- every file in `## Files` exists and says what its line in the plan says;
- nothing was written that the plan does not list;
- each answer is reflected where it applies;
- the reading checks `SKILL.md` lists for the self review pass.

The sub-agent edits nothing and returns what it checked and its findings. Fix
what it finds in the worktree in a single pass, run the tool checks `SKILL.md`
lists for the self review, and write what was checked and each fix under
`## Self review` in the Run plan, one line each, "checked: ..." or
"fixed: ...". The Change-set gate says only what that section
says: a review you cannot list was not done, and running the tool's checks is
not a review. Show what you could not fix at the Change-set gate. A finding
that changes how Tasks are sliced or ordered goes back to the Design gate.

The person's review time should go to judgement, not to defects you could have
found yourself.

## 6. When a step goes wrong

| Situation | Do |
|---|---|
| `draft start` says the branch exists | Use section 2 again; never delete a draft that is not merged |
| The pull request has conflicts, because another draft was merged first | `$T draft resume tasks-<Key>` if the worktree is gone, then `$T refresh` in it. It resolves conflicts in tool-written files itself; for a file a person writes it stops and names it: resolve it with git and run `$T refresh` again |
| `refresh` reports `ids.duplicate-key` | Another draft chose the same key: `$T rename <old> <new>`, then `$T refresh` |
| `draft finish` says `git config user.email` is not set | Ask the user for the id to record, and pass it: `--verified-by human:<id>` |
| `draft commit` refuses because files changed after `finish` | Run `draft finish` again |
| The user abandons the change | `cd "$WIKI" && $T draft discard tasks-<Key> --remote` |
