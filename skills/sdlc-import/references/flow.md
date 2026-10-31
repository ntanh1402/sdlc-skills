# How sdlc-import runs

This file gives the order of one run: what to find out first, how to ask,
what to plan, where to stop for approval and what to say at the end.
`SKILL.md` says what is this skill's own at each step.

Work is kept in the draft worktree `WIKI/.worktrees/import-<key>/`
(`write-protocol.md`, next to this file).

## 1. The steps

| Step | What you do | Gate |
|---|---|---|
| 1. Look up | Read the Import source and what the wiki already says about it (section 3) | |
| 2. Questions | Ask the person in rounds (section 4) | **Intent**: restate the answers, the kind, create or compare, the draft key, the file types, and that prerequisites are on the default branch |
| 3. Run plan | Start or resume the draft worktree. Prepare the files and write the Run plan grouped by review group (section 5) | |
| 4. Review and write | Show the Run plan once, then show the files group by group in full; write and tick each group's files as soon as the group is answered. After all groups, show the three lists | **Design** (taken group by group) |
| 5. Input check and finish | Check that the wiki files compared or linked did not change on the default branch since you read them, then run `draft finish` | |
| 6. Change-set | Show `draft diff` and the commit message | **Change-set** |
| 7. Summary | Commit, then the summary (section 6) | |

## 2. The gates

A gate is a stop for the person's explicit approval. There are three, so the
person decides what is being done (Intent), how (Design, taken group by
group), and exactly what is saved (Change-set), each before the next cost is
paid.

- Approval is an explicit yes to the gate's question (or, for a Design group,
  Approve, Change, or "Save it, I did not check it"). "Sounds good", silence
  or "whatever you think" is not approval.
- An edit at a gate reopens that gate (or group) and every later one.
- When you cannot ask the person (a run with no one to answer), or the person
  asks you to skip questions or approvals ("don't ask me, just write it"),
  stop before the first gate and start no draft. Return the open decisions
  and the gates the work still needs. Never assume approval.
- When the person rejects the import as a whole, stop. A draft worktree this
  run started is discarded; a worktree an earlier run started is left as it
  is.
- Being asked to run this skill does not approve anything it writes.
- A refusal `SKILL.md` states is a refusal. Do not turn it into a question.

## 3. Look up

Before the first question, read both the Import source and what the wiki
already says about it on the default branch (`read-protocol.md`): the main
concept if it exists, the prerequisites for this kind, and any draft open on
the same key. A question the Import source or the wiki already answers wastes
the person's time.

An earlier run of the same work may have stopped part-way. When its worktree
still exists and holds a `plan.md`, do not start again and do not ask the
rounds again: go to "Resuming" in section 5.

## 4. Questions

Ask in rounds. A round is a numbered list of every question that can be
answered now, each with your recommended answer. The person confirms or
corrects, which is faster than composing an answer, and sees your reasoning
before any work is done.

```text
Q1 - What kind of Import source is ../orders-service, and which Application does it belong to?
     ➡️ Code of SVC-orders in Application shop (wiki/index.md); SVC-orders is not in the wiki yet, so this run creates it.
Q2 - What else in the wiki does this Import source touch?
     ➡️ SVC-orders, its Endpoints and Subscriptions, TBL-orders in DB-shop, and CHAN-order-created.
```

Which questions to ask, and how many, is your judgement. Three things are
fixed:

- **The format.** Numbered questions, each with a recommendation (except the
  differences of a compare run: see below). A recommendation that rests on the
  wiki or the Import source cites the path. A question whose answer depends on
  another question in the same round waits for the next round.
- **At least one round**, even when a request seems complete. Its questions are
  then the assumptions you would otherwise make without saying so.
- **The wiki question.** Ask what else in the wiki this Import source touches,
  with your own answer as the recommendation. A file of another kind is
  another run, listed under "For other skills".

**Compare runs.** When the Import source is already in the wiki, the
differences found between the Import source and the wiki are asked as one
numbered round with **no recommendation**, except the two proposals
`references/compare.md` allows. Never choose between the wiki and the source
for the person.

Wait for the answers. Ask another round when the answers open new questions.
When nothing that changes the output is left undecided, go to the Intent gate:
one approval, after the rounds.

**A change another skill owns.** When an answer needs a wiki change this skill
does not own (such as a ChangeRequest for unbuilt work or a bugfix when "the
code is wrong"), do not make it. List it under "For other skills" in the Run
plan and in the summary. When a prerequisite of this kind is not on the
default branch yet, stop before the Intent gate and name the import run to do
first.

## 5. The Run plan

The Run plan is the list of things this run has to do, with what is done so
far. It is the file `plan.md` at the root of the draft worktree. A compare run
starts its draft, and so its Run plan, only when it has something to write or
to confirm.

Under `## Files`, list the files under their group headings (`SKILL.md`
section 5), and record each group's answer on its heading once given:

```markdown
# Run plan: sdlc-import, SVC-orders
Intent approved 2026-10-03 · Design approved 2026-10-03

## Answers
1. Code import of SVC-orders in shop, owned by team orders.

## Assumed
- Database DB-shop holds TBL-orders.

## Files
### The Service page: approved
- [x] services/SVC-orders/overview.md (add)
- [x] services/SVC-orders/log.md (add)
### Endpoints: saved unchecked
- [x] services/SVC-orders/EP-create-order.md (add)
### Tables of DB-shop
- [ ] datastores/DB-shop/TBL-orders.md (add)
- [ ] datastores/DB-shop/log.md (change)

## For other skills
- Unbuilt refund endpoint in branch feature/refund: sdlc-write-spec
```

- `## Answers` holds what the person decided in the rounds. `## Assumed` holds
  what you decided without asking.
- `## Files` groups files by their review group. Write and tick the files of a
  group as soon as the group has its answer, and record the answer (`approved`
  or `saved unchecked`) on the group's heading.
- Do not copy the files into `plan.md`. Show each group's files in full in the
  chat at the Design gate.
- Add "Design approved" with the date when the last group is answered.
- Leave out a heading that has nothing under it.
- Git ignores the file. It is never committed and goes when the worktree goes.

**Resuming.** When the lookup finds a worktree of this work that holds a
`plan.md`, an earlier run stopped part-way. Never discard that worktree: its
files and its plan exist nowhere else. Show the plan and ask one question:
"does this plan still stand?". On yes, continue at the first group that has no
answer yet (or the first unticked file in an answered group), then go on to
the input check and the Change-set gate. Any change the person makes to an
already-approved group reopens that group: show the group in full again and
take its answer again.

## 6. Summary

End the run with at most four lines:

```text
Done: wiki/import-SVC-orders, 6 files, pushed. Open the pull request.
Not done: services/SVC-orders/EP-legacy-export.md (missing response schema)
For other skills: checkout timeout bug in code needs a ChangeRequest (sdlc-write-spec)
Next: Import the requirement document with sdlc-import after the merge.
```

Leave out "Not done" and "For other skills" when they have nothing to say. Do
not repeat the three lists of `SKILL.md` section 5.
