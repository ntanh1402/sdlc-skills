# Writing a test-design draft to the project wiki

This file says how `sdlc-design-tests` drafts, checks, approves and commits its
changes to the wiki. `SKILL.md` says what to write; this file says how.
Read it when `SKILL.md` section 1 finds an unfinished draft, or at section 4.

## 1. The rules

- Every change goes into a **draft**: a branch `wiki/tests-<Key>` with its own
  worktree in `WIKI/.worktrees/tests-<Key>/`. The default branch changes only
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
- Never edit another step's output: write only `TS-*/` and `TC-*.md` files
  under `wiki/<app>/tests/` (plus an optional test-plan Reference folder
  `references/REF-<name>-test-plan/` when the user gave a test plan).
- Keys are names taken from titles, never numbers: `TS-coupons-e2e`,
  `TC-apply-valid-coupon`. A key on the default branch never changes. Before
  the pull request is merged, `$T rename <old> <new>` changes one.

## 2. The draft key

The key is `tests-<Key>`: `tests-` followed by the key of the Feature or
ChangeRequest (`tests-FEAT-coupons`, `tests-CR-sms-alerts`).

**First, look for a worktree.** When `WIKI/.worktrees/tests-<Key>/` exists, an
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
2. **`wiki/tests-<Key>` exists and is not merged** into the default branch
   (`git merge-base --is-ancestor wiki/tests-<Key> "$DEFAULT"` fails). This is
   a revision, for example after review: `$T draft resume tests-<Key>`. Tell
   the user that new commits join any pull request open for that branch.
3. **`wiki/tests-<Key>` exists and is merged.** Run
   `$T draft discard tests-<Key> --remote`, then `$T draft start tests-<Key>`.
   Everything on that branch is already on the default branch, so deleting it
   loses nothing. If your environment refuses the deletion, ask the user to run
   the same `draft discard` command, then continue.
4. **Otherwise** `$T draft start tests-<Key>`.

## 3. The commands of each section

Each part is for the section of `SKILL.md` it names.

### At section 4: Run plan and the Design gate

Start or resume `tests-<Key>` (section 2). Then:

```bash
cd "$WIKI/.worktrees/tests-<Key>"
READ=$(git rev-parse "$DEFAULT")
```

Read the input again here, from the default branch at `READ`. For a new draft
the worktree is that commit; a resumed draft also holds its own earlier commits,
which are not input. Write the Run plan (section 4) to `plan.md` in this folder,
the root of the worktree. Git ignores it there.

When the person rejects the design, remove a draft this run started:

```bash
cd "$WIKI" && $T draft discard tests-<Key>
```

### At section 5: Write

Write the TestSuite and TestCase files under `wiki/` in the worktree,
following `.wiki-llm/schema/test-suite.md` and `test-case.md`. Add an entry
to the `log.md` of each changed suite, under today's date, newest first:

```markdown
## 2026-10-02

* **Test design**: Added 9 cases for FEAT-coupons. Written by an AI model with sdlc-design-tests.
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
$T draft finish --by "sdlc-design-tests/<the line in RELEASE>" --verified-by
```

`--verified-by` without a value records the person in
`git config user.email` as having confirmed the files; their approval at the
gates is that confirmation. If `ok` is false, fix what `missing_logs` and
`validate.errors` report and run it again. Never record a model name.

**Change-set gate.** Run `$T draft diff`. Show the files it lists (those marked
`authored: false` were written by the tool, including each suite's
`checklist.csv`), a commit message, and what the self review could not fix. Ask
for approval. A change returns to the writing, or to the Design gate if the test
design changes.

On approval:

```bash
$T draft commit -m "<message>"; cd "$WIKI"
```

Run both in one command: `draft commit` removes the worktree you are in,
and the `plan.md` with it. Judge the result by the JSON it prints (`ok`,
`branch`, `pushed`), not by an error about the current directory. In the
summary, "Done" names the branch `wiki/tests-<Key>` and says the user opens
the pull request. If there is no remote, say the branch must be pushed
first.

## 4. The Run plan

The Run plan is the list of things this run has to do, with what is done so
far. It is the file `plan.md` at the root of the draft worktree. A run can end
before it is finished, and the next session has no memory of the
conversation; the file is what it starts from.

```markdown
# Run plan: sdlc-design-tests, FEAT-coupons
Intent approved 2026-10-03 · Design approved 2026-10-03

## Answers
1. Design integration and e2e suites for FEAT-coupons.

## Assumed
- Test data uses the sample shop currency USD.

## Files
- [x] tests/TS-coupons-e2e/overview.md (add: Approved e2e suite for FEAT-coupons)
- [ ] tests/TS-coupons-e2e/TC-apply-valid-coupon.md (add: covers REQ-coupons-redeem)
- [ ] tests/TS-coupons-e2e/log.md (add: Test design log entry)

## Self review
- checked: coverage tests reports nothing uncovered; every case has concrete data and payloads
- fixed: numbered # Test data from 1 in TC-apply-valid-coupon.md

## For other skills
- REQ-coupons-expiry lacks an exact timezone rule: sdlc-write-spec
```

- `## Answers` holds what the person decided in the rounds. `## Assumed` holds
  what you decided without asking; the person reads it at the Design gate.
- `## Files` has one line per file: the path, whether it is added, changed or
  deleted, and what changes. Tick a file when it is written. The checkboxes
  are the only status.
- Do not copy the test design into the file. Show the test design in full in
  the chat at the Design gate. A text that is written twice says two different
  things sooner or later.
- Add "Design approved" with the date when the Design gate is approved.
- Leave out a heading that has nothing under it.
- Git ignores the file. It is never committed and goes when the worktree goes.

**Resuming.** Do not ask the rounds again. Show the plan and ask one question:
"does this plan still stand?". On yes, continue at the first unticked file;
work out what it says from the answers, its line in the plan and the files
already written, then go on to the self review. Any change the person makes
reopens the Design gate: show the test design again before writing.

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
what it finds in the worktree in a single pass, run the tool check `SKILL.md`
lists for the self review, and write what was checked and each fix under
`## Self review` in the Run plan, one line each, "checked: ..." or
"fixed: ...". The Change-set gate says only what that section
says: a review you cannot list was not done, and running the tool's checks is
not a review. Show what you could not fix at the Change-set gate. A finding
that changes the test design goes back to the Design gate.

The person's review time should go to judgement, not to defects you could have
found yourself.

## 6. When a step goes wrong

| Situation | Do |
|---|---|
| `draft start` says the branch exists | Use section 2 again; never delete a draft that is not merged |
| The pull request has conflicts, because another draft was merged first | `$T draft resume tests-<Key>` if the worktree is gone, then `$T refresh` in it. It resolves conflicts in tool-written files itself; for a file a person writes it stops and names it: resolve it with git and run `$T refresh` again |
| `refresh` reports `ids.duplicate-key` | Another draft chose the same key: `$T rename <old> <new>`, then `$T refresh` |
| `draft finish` says `git config user.email` is not set | Ask the user for the id to record, and pass it: `--verified-by human:<id>` |
| `draft commit` refuses because files changed after `finish` | Run `draft finish` again |
| The user abandons the change | `cd "$WIKI" && $T draft discard tests-<Key> --remote` |
