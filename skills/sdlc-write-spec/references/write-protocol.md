# Writing a spec draft to the project wiki

This file says how `sdlc-write-spec` drafts, checks, approves and commits its
changes to the wiki. `SKILL.md` says what to write; this file says how.
Read it when `SKILL.md` section 1 finds an unfinished draft, or at section 3.

## 1. The rules

- Every change goes into a **draft**: a branch `wiki/spec-<Key>` with its own
  worktree in `WIKI/.worktrees/spec-<Key>/`. The default branch changes only
  when the user merges the draft's pull request.
- One lifecycle step is one draft and one pull request. This step reads only
  what earlier steps merged into the default branch.
- Stop at the three **approval gates** of `SKILL.md`: Intent, Design and
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

## 2. The draft key

The key is `spec-<Key>`: `spec-` followed by the key of the Feature or
ChangeRequest (`spec-FEAT-coupons`, `spec-CR-gift-card-expiry`).

**First, look for a worktree.** When `WIKI/.worktrees/spec-<Key>/` exists, an
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

## 3. The commands of each section

Each part is for the section of `SKILL.md` it names.

### At section 3: Run plan and the Design gate

Choose `spec-<Key>` and start or resume the draft (section 2).
Then:

```bash
cd "$WIKI/.worktrees/spec-<Key>"
READ=$(git rev-parse "$DEFAULT")
```

Read the input again here, from the default branch at `READ`. For a new draft
the worktree is that commit; a resumed draft also holds its own earlier commits,
which are not input. Write the Run plan (section 4) to `plan.md` in this folder,
the root of the worktree. Git ignores it there.

When the person rejects the design, remove a draft this run started:

```bash
cd "$WIKI" && $T draft discard spec-<Key>
```

### At section 4: Write

Write the files under `wiki/` in the worktree. Follow the schema page of
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

Then the **input check**: has the input changed on the default branch
since you read it?

```bash
git fetch --quiet origin 2>/dev/null
git diff --quiet "$READ" "$DEFAULT" -- <the input paths> || git diff --stat "$READ" "$DEFAULT" -- <the input paths>
```

If it changed, show the user what changed and go back to the Design gate. Do not
merge the default branch in here: `$T refresh` is for a pull request that
has conflicts (section 6).

### At section 5: Self review, finish and commit

Do the self review (section 5 of this file).
Then stamp, check and validate:

```bash
$T draft finish --by "sdlc-write-spec/<the line in RELEASE>" --verified-by
```

`--verified-by` without a value records the person in
`git config user.email` as having confirmed the files; their approval at the
gates is that confirmation. If `ok` is false, fix what `missing_logs` and
`validate.errors` report and run it again. Never record a model name.

**Change-set gate.** Run `$T draft diff`. Show the files it lists (those marked
`authored: false` were written by the tool), a commit message, and what the self
review could not fix. Ask for approval. A change returns to the writing, or to
the Design gate if the design changes.

On approval:

```bash
$T draft commit -m "<message>"; cd "$WIKI"
```

Run both in one command: `draft commit` removes the worktree you are in,
and the `plan.md` with it. Judge the result by the JSON it prints (`ok`,
`branch`, `pushed`), not by an error about the current directory. In the
summary, "Done" names the branch `wiki/spec-<Key>` and says the user opens
the pull request. If there is no remote, say the branch must be pushed
first.

## 4. The Run plan

The Run plan is the list of things this run has to do, with what is done so
far. It is the file `plan.md` at the root of the draft worktree. A run can end
before it is finished, and the next session has no memory of the
conversation; the file is what it starts from.

```markdown
# Run plan: sdlc-write-spec, FEAT-coupons
Intent approved 2026-10-03 · Design approved 2026-10-03

## Answers
1. New Feature FEAT-coupons in shop, status Draft.

## Assumed
- Owner team is checkout.

## Files
- [x] references/REF-coupons-prd/prd.md (add: approved PRD)
- [ ] references/REF-coupons-prd/overview.md (add: Reference overview)
- [ ] references/REF-coupons-prd/log.md (add: PRD log entry)
- [ ] features/FEAT-coupons/overview.md (add: 4 Requirements, status Draft, version 1)
- [ ] features/FEAT-coupons/log.md (add: Spec log entry)

## Self review
- checked: every file in Files exists; each Requirement maps to approved PRD text
- fixed: missing Reference link under # References

## For other skills
- Arch design next: sdlc-design-arch
```

- `## Answers` holds what the person decided in the rounds. `## Assumed` holds
  what you decided without asking; the person reads it at the Design gate.
- `## Files` has one line per file: the path, whether it is added, changed or
  deleted, and what changes. Tick a file when it is written. The checkboxes
  are the only status.
- Add "Design approved" with the date when the Design gate is approved.
- Leave out a heading that has nothing under it.
- Git ignores the file. It is never committed and goes when the worktree goes.

**Resuming.** Do not ask the rounds again. Show the plan and ask one question:
"does this plan still stand?". On yes, continue at the first unticked file;
work out what it says from the answers, its line in the plan and the files
already written, then go on to the self review. Any change the person makes
reopens the Design gate: show the PRD and mapping again before writing.

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
- the checks `SKILL.md` lists for the self review pass.

The sub-agent edits nothing and returns what it checked and its findings. Fix
what it finds in the worktree in a single pass, and write what was checked and
each fix under `## Self review` in the Run plan, one line each, "checked: ..."
or "fixed: ...". The Change-set gate says only
what that section says: a review you cannot list was not done, and running the
tool's checks is not a review. Show what you could not fix at the Change-set
gate. A finding that changes the PRD or Requirements goes back to the Design
gate.

The person's review time should go to judgement, not to defects you could have
found yourself.

## 6. When a step goes wrong

| Situation | Do |
|---|---|
| `draft start` says the branch exists | Use section 2 again; never delete a draft that is not merged |
| The pull request has conflicts, because another draft was merged first | `$T draft resume spec-<Key>` if the worktree is gone, then `$T refresh` in it. It resolves conflicts in tool-written files itself; for a file a person writes it stops and names it: resolve it with git and run `$T refresh` again |
| `refresh` reports `ids.duplicate-key` or `ids.requirement-collision` | Another draft chose the same key: `$T rename <old> <new>` (with `--change CR-x` for a Requirement inside one ChangeRequest), then `$T refresh` |
| `draft finish` says `git config user.email` is not set | Ask the user for the id to record, and pass it: `--verified-by human:<id>` |
| `draft commit` refuses because files changed after `finish` | Run `draft finish` again |
| The user abandons the change | `cd "$WIKI" && $T draft discard spec-<Key> --remote` |
