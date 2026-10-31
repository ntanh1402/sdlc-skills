# How sdlc-build-task runs

This file gives the order of one run: what to find out first, how to ask,
what to plan, where to stop for approval, how to check your own work and what
to say at the end. `SKILL.md` says what is this skill's own at each step.

Work is kept in a git worktree of the code repository,
`<code folder>/.worktrees/<Task name without TASK->/`, on branch
`task/<Task name without TASK->` (unless `conventions.md` names another branch
rule). This skill never writes to the wiki.

## 1. The steps

| Step | What you do | Gate |
|---|---|---|
| 1. Look up | Read the Task, its scope, Design contracts and `conventions.md` in the wiki, and read the code repository (section 3) | |
| 2. Questions | Ask the person in rounds (section 4) | **Intent**: restate the Task, the code folder, the branch name, the worktree path, and what will not be built here |
| 3. Run plan | Start or resume the code worktree. Write the Run plan (`plan.md`, or `sdlc-plan.md` when the repo tracks `plan.md`) (section 5) | |
| 4. Review | Show the Run plan in full (for code, the Run plan is the design) | **Design** |
| 5. Work | Write the code and unit tests in the worktree, ticking each file off in the Run plan. Then check that the wiki input did not change since you read it | |
| 6. Self review | Review the output against the wiki in a fresh sub-agent with `code-checks.md` (section 6) | **Change-set**: `git diff --cached --stat` and the diff, the commit message with `Task: <Task key>`, and what the self review could not fix or could not check |
| 7. Summary | Delete the Run plan file, commit on the branch without pushing, then the summary (section 7) | |

## 2. The gates

A gate is a stop for the person's explicit approval. There are three, so the
person decides what is being done (Intent), how (Design), and exactly what is
saved (Change-set), each before the next cost is paid.

- Approval is an explicit yes to the gate's question. "Sounds good", silence
  or "whatever you think" is not approval.
- An edit at a gate reopens that gate and every later one.
- When you cannot ask the person (a run with no one to answer), or the person
  asks you to skip questions or approvals ("don't ask me, just write it"),
  stop before the first gate and start no worktree. Return the open decisions
  and the gates the work still needs. Never assume approval.
- When the person rejects the design, stop. A worktree and branch this run
  started are removed; those an earlier run started are left as they are.
- Being asked to run this skill does not approve anything it writes.
- A refusal `SKILL.md` states is a refusal. Do not turn it into a question.

## 3. Look up

Before the first question, read what the wiki already says on its default
branch (`read-protocol.md`): the Task, every Design file in its `# Planned
scope`, the parent's `# Architecture` or `# Delta` and decisions,
`conventions.md`, and the linked References. Then read the code folder to see
its layout, where each scope item lives, and how its unit tests are written. A
question the wiki or the code already answers wastes the person's time, and a
recommendation without a file path is a guess.

An earlier run of the same Task may have stopped part-way. When its branch or
worktree already exists in the code repository, do not start again and do not
ask the rounds again: go to "Resuming" in section 5.

## 4. Questions

Ask in rounds. A round is a numbered list of every question that can be
answered now, each with your recommended answer. The person confirms or
corrects, which is faster than composing an answer, and sees your reasoning
before any work is done.

```text
Q1 - Where should EP-apply-coupon live in ../orders-svc? Existing order endpoints
     are in src/api/orders.py.
     ➡️ In src/api/orders.py, with unit tests in tests/test_orders.py.
Q2 - What else in the wiki must change because of this?
     ➡️ Nothing.
```

Which questions to ask, and how many, is your judgement. Three things are
fixed:

- **The format.** Numbered questions, each with a recommendation. A
  recommendation that rests on the wiki or the code cites the path. A question
  whose answer depends on another question in the same round waits for the
  next round.
- **At least one round**, even when a Task seems complete. Its questions are
  then the assumptions you would otherwise make without saying so.
- **The wiki question.** Ask what else in the wiki must change because of
  this request, with your own answer as the recommendation. Because this skill
  never writes the wiki, every answer other than "nothing" goes under "For
  other skills".

The first round puts what the lookup found to the person: the Task, its parent
and the code folder, the branch name and worktree path, where each scope item
goes in the code, any scope item that belongs to another repository, and any
blocker that is not `Done`.

Wait for the answers. Ask another round when the answers open new questions.
When nothing that changes the output is left undecided, go to the Intent gate:
one approval, after the rounds.

**A change another skill owns.** When an answer needs a wiki change, do not
make it. List it under "For other skills" in the Run plan and in the summary.
When your work depends on it, stop before the Intent gate and name the skill
to run first.

## 5. The Run plan

The Run plan is the list of things this run has to do, with what is done so
far. It is the file `plan.md` at the root of the code worktree (or
`sdlc-plan.md` when the code repository tracks its own `plan.md` there). For
code it is also the design shown at the Design gate.

```markdown
# Run plan: sdlc-build-task, TASK-coupon-api
Intent approved 2026-10-03 · Design approved 2026-10-03

## Answers
1. Endpoint handler in src/api/coupons.py; unit tests in src/api/test_coupons.py.

## Assumed
- Uses the existing database session helper in src/db.py.

## Files
- [x] src/api/coupons.py (add: POST /coupons/apply; EP-apply-coupon; acceptance 1 and 2)
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

**Resuming.** When the lookup finds the branch or the worktree of this Task,
an earlier run stopped part-way. Never delete either. Show the branch's
commits and the Run plan when there is one, and ask one question: "does this
plan still stand?". On yes, continue at the first unticked file; work out what
it says from the answers, its line in the plan and the files already written,
then go on to the self review. Any change the person makes reopens the Design
gate: show the Run plan again before writing.

## 6. Self review

After the last file is written and the wiki input check passes, run a fresh
read-only sub-agent to review the output from disk (if the environment cannot
run sub-agents, do the review yourself by reading the files from disk). Give
the sub-agent only the worktree path (holding `plan.md` and the written code
and unit tests), the wiki path `$WIKI` (the Task file, the Design files in
scope, and `conventions.md`), and these checks plus `code-checks.md` — not
the conversation history:

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

## 7. Summary

End the run with at most four lines:

```text
Done: task/coupon-api in ../orders-svc/.worktrees/coupon-api, 1 commit, not pushed.
Not done: the coupon field of WEB-storefront (not in this folder)
For other skills: REQ-coupons-expiry is ambiguous (sdlc-write-spec)
Next: push, open the pull request, review, merge; then sdlc-close-task.
```

Leave out "Not done" and "For other skills" when they have nothing to say. Do
not list what the self review fixed, and do not repeat the Run plan.
