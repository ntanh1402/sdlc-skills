# Writing the code of a Task in its own worktree

This file says how `sdlc-build-task` sets up its worktree, plans, checks,
approves and commits the code. `SKILL.md` says what to write and where the
gates are; this file says how. Read it when `SKILL.md` section 1 finds an
unfinished build, or at section 3.

## 1. The rules

- The code is written in a git worktree of its own, on a branch of its own.
  The person's checkout stays as it is; uncommitted changes in it do not
  matter.
- Stop at the three **approval gates** of `SKILL.md`: Intent, Design and
  Change-set. No worktree is added before the Intent gate is approved.
- Use plain git, not the wiki's tool. The wiki is never written.
- One commit on the branch, ending with the trailer `Task: <Task key>`. Never
  push, never open a pull request.
- The Run plan is never committed.

## 2. The worktree

The names (`NAME`, the branch, the worktree, the Run plan file) are in
`SKILL.md` section 3.

Before the worktree is added, make git ignore the worktrees and the Run plan
through the repository's `info/exclude`. That file is local and never committed,
so the repository's own `.gitignore` is not touched:

```bash
PLAN=plan.md
git -C "$SRC" cat-file -e "$BASE:plan.md" 2>/dev/null && PLAN=sdlc-plan.md
EXCLUDE="$(git -C "$SRC" rev-parse --path-format=absolute --git-common-dir)/info/exclude"
mkdir -p "$(dirname "$EXCLUDE")"
for line in ".worktrees/" "/$PLAN"; do
  grep -qxF "$line" "$EXCLUDE" 2>/dev/null || echo "$line" >> "$EXCLUDE"
done
git -C "$SRC" worktree add -b "<branch>" "$SRC/.worktrees/$NAME" "$BASE"
```

An ignore rule does not hide a file git already tracks. That is why a
repository with its own `plan.md` gets `sdlc-plan.md`: its file is never
overwritten, deleted or committed by this skill.

**First, look for the branch and the worktree.** When the branch or the
worktree already exists, an earlier run started this Task. Never delete
either. A branch with no worktree gets one:
`git -C "$SRC" worktree add "$SRC/.worktrees/$NAME" "<branch>"`. Then resume
as section 4 ("Resuming") says.

## 3. The commands of each section

Each part is for the section of `SKILL.md` it names.

### At section 3: The worktree and the Run plan

Add or find the worktree (section 2), then write
the Run plan (section 4) at its root.

### At section 4: Design gate

When the person rejects the design, remove a worktree and a branch this run
made:

```bash
git -C "$SRC" worktree remove --force "$SRC/.worktrees/$NAME"
git -C "$SRC" branch -D "<branch>"
```

### At section 6: Self review and the Change-set gate

First check that the input did not change:

```bash
git -C "$WIKI" fetch --quiet origin 2>/dev/null
git -C "$WIKI" diff --stat "$READ" "$DEFAULT" -- <the Task file and each Design file in its scope>
```

If it prints anything, show it and go back to the Design gate.

Do the self review (section 5 of this file).

**Change-set gate.** In the worktree, `git add -A`, then show
`git diff --cached --stat` and the diff, the commit message (`SKILL.md` section
6), what the self review could not fix and everything under "Not checked". Ask
for approval. A change returns to the writing, or to the Design gate if the plan
changes. On approval, delete the Run plan file and commit on the branch. Do not
push.

## 4. The Run plan

The Run plan is the list of things this run has to do, with what is done
so far. A run can end before it is finished, and the next session has no
memory of the conversation; the file is what it starts from:

```markdown
# Run plan: sdlc-build-task, TASK-coupon-api
Intent approved 2026-10-03 · Design approved 2026-10-03

## Answers
1. Endpoint handler in src/api/coupons.py; unit tests in src/api/test_coupons.py.

## Assumed
- Uses the existing database session helper in src/db.py.

## Files
- [ ] src/api/coupons.py (add: POST /coupons/apply; EP-apply-coupon; acceptance 1 and 2)
- [ ] src/api/test_coupons.py (add: unit tests for the 200, 404 and 409 paths; acceptance 1 to 3)
- [ ] db/migration/V7__coupons.sql (add: table coupons; TBL-coupons)

## Not built here
- WEB-storefront, the coupon field: not in this folder

## Self review
- checked: every # Validations rule and # Flowchart exit of EP-apply-coupon is coded and unit-tested
- fixed: status code for expired coupon changed from 400 to 409 to match EP-apply-coupon.md

## For other skills
- REQ-coupons-expiry is ambiguous: sdlc-write-spec
```

- `## Answers` holds what the person decided in the rounds. `## Assumed` holds
  what you decided without asking; the person reads it at the Design gate.
- `## Files` has one line per code file and per unit-test file: the path,
  added or changed, what it does, and the scope item and acceptance item it
  serves. Tick a file when it is written. The checkboxes are the only status.
- `## Not built here` lists each scope item the plan does not cover, with the
  reason. Leave it out when every item is covered.
- Add "Design approved" with the date when the Design gate is approved.
- Leave out a heading that has nothing under it.
- Git ignores the file via `.git/info/exclude`, and you delete it before
  committing on approval at the Change-set gate.

**Resuming.** Show the branch's commits
(`git -C "$SRC" log --oneline "$BASE..<branch>"`) and the Run plan when there is
one, and ask one question: "does this plan still stand?". On yes, continue at
the first unticked file; work out what it says from the answers, its line in the
plan and the files already written, then go on to the self review. Any change
the person makes reopens the Design gate: show the Run plan again before
writing. Do not ask the rounds again. With no Run plan, write a new one for what
is left.

## 5. Self review

After the last file is written and the input check passes, run a fresh
read-only sub-agent to review the output from disk (if the environment cannot
run sub-agents, do the review yourself by reading the files from disk). Give
the sub-agent only the worktree path (holding `plan.md` and the written code
and unit tests), the wiki path `$WIKI` (the Task file, the Design files in
scope, and `conventions.md`), and these checks plus
`code-checks.md`, next to this file — not the conversation history:

- every file in `## Files` exists and does what its line in the plan says;
- nothing was written that the plan does not list;
- each answer is reflected where it applies;
- every acceptance item, contract rule (`# Validations`, `# Flowchart` exits,
  fields, types, status codes, columns) and `conventions.md` rule in
  `code-checks.md` is met by reading.

The sub-agent edits nothing and returns what it checked, its findings, and
everything under "Not checked". When it reports that the wiki is the wrong
side, stop as `SKILL.md` section 5 says. Otherwise fix what it finds in the
worktree in a single pass, and write what was checked and each fix under
`## Self review` in the Run plan, one line each, "checked: ..." or
"fixed: ...", naming only setting names for any secret or personal data. The
Change-set gate says only what that section says: a review you cannot list was
not done. Show what you could not fix, and everything under "Not checked", at
the Change-set gate. A finding that changes the plan goes back to the Design
gate.
