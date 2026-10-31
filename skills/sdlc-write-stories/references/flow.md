# How sdlc-write-stories runs

This file gives the order of one run: what to find out first, how to ask,
what to plan, where to stop for approval, how to check your own work and what
to say at the end. `SKILL.md` says what is this skill's own at each step.

Work is kept in the draft worktree `WIKI/.worktrees/stories-<Key>/`
(`write-protocol.md`, next to this file).

## 1. The steps

| Step | What you do | Gate |
|---|---|---|
| 1. Look up | Read the wiki for the target's Requirements, PRD, stories and Tasks (section 3) | |
| 2. Questions | Ask the person in rounds (section 4) | **Intent**: restate the target, the Requirement inventory and the proposed stories |
| 3. Run plan | Start or resume the draft worktree. Prepare every story in full and the coverage matrix. Write the Run plan (section 5) | |
| 4. Review | Show every story in full, never only a summary, the coverage matrix and the Run plan | **Design** |
| 5. Work | Write the files, ticking each one off in the Run plan. Then check that the target's Requirements did not change since you read them | |
| 6. Self review | Review the output in a fresh sub-agent (section 6) | **Change-set**: the diff, the commit message, and what the self review could not fix |
| 7. Summary | Commit, print the paste-ready stories (`paste-format.md`), then the summary (section 7) | |

## 2. The gates

A gate is a stop for the person's explicit approval. There are three, so the
person decides what is being done (Intent), how (Design), and exactly what is
saved (Change-set), each before the next cost is paid.

- Approval is an explicit yes to the gate's question. "Sounds good", silence
  or "whatever you think" is not approval.
- An edit at a gate reopens that gate and every later one.
- When you cannot ask the person (a run with no one to answer), or the person
  asks you to skip questions or approvals ("don't ask me, just write it"),
  stop before the first gate and start no draft. Return the open decisions
  and the gates the work still needs. Never assume approval.
- When the person rejects the design, stop. A draft worktree this run started
  is discarded; a worktree an earlier run started is left as it is.
- Being asked to run this skill does not approve anything it writes.
- A refusal `SKILL.md` states is a refusal. Do not turn it into a question.

## 3. Look up

Before the first question, read what the wiki already says: the target Feature
or ChangeRequest, its PRD Reference, the stories already in the folder, the
Tasks that link them, and any draft open on the same key. A question the wiki
already answers wastes the person's time, and a recommendation without a wiki
path is a guess.

Read the default branch, as `read-protocol.md` says. Search again whenever an
answer brings a system, a term or a claim about current behaviour you have not
read.

An earlier run of the same work may have stopped part-way. When its worktree
still exists and holds a `plan.md`, do not start again and do not ask the
rounds again: go to "Resuming" in section 5.

## 4. Questions

Ask in rounds. A round is a numbered list of every question that can be
answered now, each with your recommended answer. The person confirms or
corrects, which is faster than composing an answer, and sees your reasoning
before any work is done.

```text
Q1 - How should the coupon Requirements be grouped into stories?
     (features/FEAT-coupons/overview.md)
     ➡️ Two stories: STORY-coupons-apply-at-checkout and STORY-coupons-remove-coupon.
Q2 - What else in the wiki must change because of this?
     ➡️ Nothing: only story files and the folder's log.
```

Which questions to ask, and how many, is your judgement. Three things are
fixed:

- **The format.** Numbered questions, each with a recommendation. A
  recommendation that rests on the wiki cites the path. A question whose
  answer depends on another question in the same round waits for the next
  round.
- **At least one round**, even when a brief seems complete. Its questions are
  then the assumptions you would otherwise make without saying so.
- **The wiki question.** Ask what else in the wiki must change because of
  this request, with your own answer as the recommendation.

The first round puts what the lookup found to the person: the target and its
state, the Requirement inventory, and the proposed stories.

Wait for the answers. Ask another round when the answers open new questions.
When nothing that changes the output is left undecided, go to the Intent gate:
one approval, after the rounds.

**A change another skill owns.** When an answer needs a wiki change this skill
does not own (such as a criterion no Requirement supports), do not make it.
List it under "For other skills" in the Run plan and in the summary. When your
work depends on it, stop before the Intent gate and name `sdlc-write-spec` to
run first.

## 5. The Run plan

The Run plan is the list of things this run has to do, with what is done so
far. It is the file `plan.md` at the root of the draft worktree. A run can end
before it is finished, and the next session has no memory of the
conversation; the file is what it starts from.

```markdown
# Run plan: sdlc-write-stories, FEAT-coupons
Intent approved 2026-10-03 · Design approved 2026-10-03

## Answers
1. Two stories: apply at checkout (P1) and remove coupon (P2).

## Assumed
- Non-functional latency Requirement REQ-coupons-latency needs no story of its own.

## Files
- [x] features/FEAT-coupons/STORY-coupons-apply-at-checkout.md (add: customer applies a coupon)
- [ ] features/FEAT-coupons/STORY-coupons-remove-coupon.md (add: customer removes an applied coupon)
- [ ] features/FEAT-coupons/log.md (change: Stories log entry)

## Self review
- checked: coverage stories reports nothing; every story has current basedOn
- fixed: added missing Requirement citation on criterion 2

## For other skills
- REQ-coupons-stacking is missing for multiple coupons: sdlc-write-spec
```

- `## Answers` holds what the person decided in the rounds. `## Assumed` holds
  what you decided without asking; the person reads it at the Design gate.
- `## Files` has one line per file: the path, whether it is added, changed or
  deleted, and what changes. Tick a file when it is written. The checkboxes
  are the only status.
- Do not copy the stories into the file. Show the stories in full in the chat
  at the Design gate. A text that is written twice says two different things
  sooner or later.
- Add "Design approved" with the date when the Design gate is approved.
- Leave out a heading that has nothing under it.
- Git ignores the file. It is never committed and goes when the worktree goes.

**Resuming.** When the lookup finds a worktree of this work that holds a
`plan.md`, an earlier run stopped part-way. Never discard that worktree: its
files and its plan exist nowhere else. Show the plan and ask one question:
"does this plan still stand?". On yes, continue at the first unticked file;
work out what it says from the answers, its line in the plan and the files
already written, then go on to the self review. Any change the person makes
reopens the Design gate: show the stories again before writing.

## 6. Self review

After the last file is written, run a fresh read-only sub-agent to review the
output from disk (if the environment cannot run sub-agents, do the review
yourself by reading the files from disk). Give the sub-agent only the worktree
path (holding `plan.md` and the written files), the upstream input files in
`$WIKI/wiki/` (verified unchanged by the input check), and these checks, the
reading checks `SKILL.md` lists for this step, and `story-rules.md` — not the
conversation history:

- every file in `## Files` exists and says what its line in the plan says;
- nothing was written that the plan does not list;
- each answer is reflected where it applies;
- the reading checks `SKILL.md` lists for this step pass.

The sub-agent edits nothing and returns what it checked and its findings. Fix
what it finds in the worktree in a single pass, run the tool checks `SKILL.md`
lists for this step, and write what was checked and each fix under
`## Self review` in the Run plan, one line each, "checked: ..." or
"fixed: ...". The Change-set gate says only what that section
says: a review you cannot list was not done, and running the tool's checks is
not a review. Show what you could not fix at the Change-set gate. A finding
that changes a story's meaning or criteria goes back to the Design gate.

The person's review time should go to judgement, not to defects you could have
found yourself.

## 7. Summary

After committing and printing the paste-ready copy of each added or changed
story (`paste-format.md`), end the run with at most four lines:

```text
Done: wiki/stories-FEAT-coupons, 3 files, pushed. Open the pull request.
Not done: STORY-coupons-stacking (needs a new Requirement first)
For other skills: REQ-coupons-stacking is missing (sdlc-write-spec)
Next: sdlc-plan-tasks once the design is merged.
```

Leave out "Not done" and "For other skills" when they have nothing to say. Do
not list what the self review fixed, and do not repeat the stories in the
summary.
