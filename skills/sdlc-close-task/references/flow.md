# How a skill runs

This file gives the order of one run: what to find out first, how to ask,
what to plan, where to stop for approval, how to check your own work and what
to say at the end. The skill's own `SKILL.md` says what is its own at each
step.

This file does not say where the work is kept. A skill that writes the wiki
keeps it in a draft (`write-protocol.md`, next to this file); a skill that
keeps it elsewhere says where in its own `SKILL.md`. Below, "the worktree" is
that place.

## 1. The steps

| Step | What you do | Gate |
|---|---|---|
| 1. Look up | Read the wiki for everything related to the request (section 3) | |
| 2. Questions | Ask the person in rounds (section 4) | **Intent**: restate the target, the scope and what your `SKILL.md` lists for this gate |
| 3. Run plan | Start or resume the worktree. Prepare the design. Write the Run plan (section 5) | |
| 4. Review | Show the design in full, never only a summary, and the Run plan | **Design** |
| 5. Work | Write the files, ticking each one off in the Run plan. Then check that the input did not change since you read it | |
| 6. Self review | Check your own output (section 6) | **Change-set**: the diff, the commit message, and what the self review could not fix |
| 7. Summary | Commit, then the summary (section 7) | |

A skill whose `SKILL.md` says so uses the short form instead (section 8).

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
- When the person rejects the design, stop. A worktree this run started is
  discarded; a worktree an earlier run started is left as it is.
- Being asked to run a skill does not approve anything it writes.
- A refusal your `SKILL.md` states is a refusal. Do not turn it into a
  question.

## 3. Look up

Before the first question, read what the wiki already says: the input of this
step, the files that link to it, and any draft open on the same key. A
question the wiki already answers wastes the person's time, and a
recommendation without a wiki path is a guess.

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
Q1 - Where are coupons validated? SVC-orders already owns order totals
     (services/SVC-orders/overview.md).
     ➡️ In SVC-orders, with no new service.
Q2 - What else in the wiki must change because of this?
     ➡️ EP-create-order gains a couponCode field. Nothing else.
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
  this request, with your own answer as the recommendation. A request usually
  touches more files than it names; asking finds them before the plan is
  approved, not after.

The first round puts what the lookup found to the person: the Application, the
target and the mode, when your skill has modes.

Wait for the answers. Ask another round when the answers open new questions.
When nothing that changes the output is left undecided, go to the Intent gate:
one approval, after the rounds.

**A change another skill owns.** When an answer needs a wiki change your skill
does not own, do not make it. List it under "For other skills" in the Run plan
and in the summary. When your work depends on it, stop before the Intent gate
and name the skill to run first.

## 5. The Run plan

The Run plan is the list of things this run has to do, with what is done so
far. It is the file `plan.md` at the root of the worktree. A run can end
before it is finished, and the next session has no memory of the
conversation; the file is what it starts from.

```markdown
# Run plan: sdlc-design-arch, FEAT-coupons
Intent approved 2026-10-03 · Design approved 2026-10-03

## Answers
1. Coupons are validated in SVC-orders, not a new service.

## Assumed
- The coupon table is in the orders datastore.

## Files
- [x] features/FEAT-coupons/overview.md (change: # Architecture filled, status Approved)
- [ ] services/SVC-orders/EP-create-order.md (change: couponCode in the request; pending entry)
- [ ] datastores/DB-shop/TBL-coupons.md (add: Planned; pending entry)

## Self review
- checked: every file in Files exists; each answer is in the design
- fixed: missing log entry in SVC-orders

## For other skills
- REQ-coupons-expiry is ambiguous: sdlc-write-spec
```

- `## Answers` holds what the person decided in the rounds. `## Assumed` holds
  what you decided without asking; the person reads it at the Design gate.
- `## Files` has one line per file: the path, whether it is added, changed or
  deleted, and what changes. Tick a file when it is written. The checkboxes
  are the only status.
- Do not copy the design into the file. Show the design in the chat at the
  Design gate. A text that is written twice says two different things sooner
  or later.
- Add "Design approved" with the date when the Design gate is approved.
- Leave out a heading that has nothing under it.
- Git ignores the file. It is never committed and goes when the worktree goes.

**Resuming.** When the lookup finds a worktree of this work that holds a
`plan.md`, an earlier run stopped part-way. Never discard that worktree: its
files and its plan exist nowhere else. Show the plan and ask one question:
"does this plan still stand?". On yes, continue at the first unticked file;
work out what it says from the answers, its line in the plan and the files
already written, then go on to the self review. Any change the person makes
reopens the Design gate: show the design again before writing.

## 6. Self review

After the last file is written, read your output again as a reviewer would,
against the approved design, the Run plan and the answers:

- every file in `## Files` exists and says what the design says;
- nothing was written that the plan does not list;
- each answer is reflected where it applies;
- the checks your `SKILL.md` lists for this step pass.

Write what you checked and each fix under `## Self review` in the Run plan,
one line each, "checked: ..." or "fixed: ...". The Change-set gate says only
what that section says: a review you cannot list was not done, and running the
tool's checks is not a review. Show what you could not fix at the Change-set
gate. A finding that changes the
design goes back to the Design gate.

The person's review time should go to judgement, not to defects you could have
found yourself.

## 7. Summary

End the run with at most four lines:

```text
Done: wiki/arch-FEAT-coupons, 4 files, pushed. Open the pull request.
Not done: services/SVC-orders/overview.md (the contract for refunds is undecided)
For other skills: REQ-coupons-expiry is ambiguous (sdlc-write-spec)
Next: sdlc-plan-tasks after the merge.
```

Leave out "Not done" and "For other skills" when they have nothing to say. Do
not list what the self review fixed, and do not repeat the design: the person
approved the content at the gates, so the last message only says where it is
and what comes next.

## 8. The short form

A skill whose change is small and exact uses the short form when its
`SKILL.md` says so:

1. Look up.
2. Ask only when the lookup leaves something undecided.
3. One stop that is the Intent and the Design gate together: the exact
   changes, file by file.
4. Write.
5. The Change-set gate.
6. Commit, then the summary with "Done" and "Next" only.

There is no Run plan and no self review beyond the tool's own checks.
