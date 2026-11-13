---
name: sdlc-write-stories
description: Break the Requirements of a Feature or ChangeRequest in the project wiki into user stories, while they are a draft or once they are agreed - one actor goal each, "As a … I want … so that …", with numbered pass/fail acceptance criteria that cite the Requirements, and a paste-ready copy for the tracker. Use when a business analyst wants user stories, a story breakdown or story acceptance criteria for requirements, wants existing stories regrouped, or the spec changed after the stories were written. Not for writing or changing Requirements, architecture, tasks, test design, tracker sync or code.
---

# Write the user stories

This skill is a lifecycle step after the Requirements are written; they may
still be a draft. It runs at the same time as `sdlc-design-arch` on the same
target; neither waits for the other. It takes a Feature or ChangeRequest and writes `STORY-<name>.md`
files into its folder, so that every Functional Requirement that is not
**Wont** is listed by at least one story.

Stories are optional: a Feature or ChangeRequest without them is planned,
tested and built as before. A story groups Requirements; it never adds
behaviour. The Requirements stay the testable unit.

Its draft prefix is `stories-`: the draft for `FEAT-coupons` is
`wiki/stories-FEAT-coupons`.

## Before you start

Read, in this skill's folder, `references/read-protocol.md`; each section names
the other `references/` files to read when it starts.

Find the wiki as the read protocol says, and check that it matches this
skill. `RELEASE`, next to this file, holds one line such as `1.0.0`:

```bash
cd "$WIKI" && $T copy check --release "<the line in RELEASE>"
```

| `status` | Do |
|---|---|
| `current` | Go on |
| `older` | Stop: "The wiki's tool is older than this skill. Run sdlc-setup-wiki to upgrade the wiki." |
| `newer` | Stop: "The wiki was set up by a newer release. Update your installed sdlc-skills." |
| `edited` | Stop: "The wiki's tool copy was edited by hand. Run sdlc-setup-wiki to restore it." |

Then read the schema pages `schema.md`, `user-story.md`, `feature.md`,
`change-request.md` and `task.md` in the wiki's `.wiki-llm/schema/`.

| Request | Skill |
|---|---|
| New or changed Requirements, or a criterion no Requirement supports | `sdlc-write-spec` |
| Architecture | `sdlc-design-arch` |
| Build tasks, or linking Tasks to stories | `sdlc-plan-tasks` |
| Test cases or suites | `sdlc-design-story-tests` for one story, `sdlc-design-feature-tests` for flows across stories |
| Create or update tickets in the tracker | No skill does: a person pastes the story and may add `trackerKey` and `resource` to it (`sdlc-edit-wiki`) |
| Show a story, or its paste-ready copy again | `sdlc-ask-wiki` |
| A typo in a story | `sdlc-edit-wiki` |

## The gates

A gate is a stop for the person's explicit approval. There are three, so the
person decides what is being done (Intent, section 2), how (Design, section 3),
and exactly what is saved (Change-set, section 5), each before the next cost is
paid.

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
- A refusal this file states is a refusal. Do not turn it into a question.

## 1. Look up: readiness and the inventory

Accept one `FEAT-*` or `CR-*` key, or find it as `sdlc-write-spec` does
(a key the user gave, an exact title, the Feature whose outcome owns the
behaviour). Read it on the default branch:

| State | When | Do |
|---|---|---|
| `READY` | A Feature `Draft`, `ReqApproved`, `Approved` or `InDev`, or a ChangeRequest `Proposed`, `ReqApproved` or `Approved`; and `coverage stories` reports Requirements, `outdated` lists a story, or the person asks to revise the stories | Go on |
| `NOT_MERGED` | Not on the default branch, but a `wiki/*-<Key>` draft exists | Stop and name the draft |
| `CLOSED` | A Feature `Released` or `Deprecated`, or a ChangeRequest `Implemented` or `Rejected` | Stop: a change to a Released Feature goes through a ChangeRequest (`sdlc-write-spec`) |
| `ALREADY_CURRENT` | `coverage stories` and `outdated` report nothing and the person asks for nothing to change | Report the stories and stop |

```bash
$T coverage stories --feature FEAT-coupons      # or --change CR-sms-alerts
$T outdated --feature FEAT-coupons              # stories written from an older spec version
```

When the Requirements are still a draft, say so in the first round: the
stories may have to change when the spec does. A story `outdated` lists was
written from an older version: compare its Requirements at that version with
the current ones (`git log -p` on the `overview.md`), and revise it only when
the change touches it; a story you revise is rewritten whole.

Every state but `READY` is a refusal, not a question.

Then read the Requirements, the PRD (the Reference the Feature or
ChangeRequest links under `# References`), the stories already in the
folder, and the Tasks that link them. For a
ChangeRequest, also read the changed Feature's stories that list a
Requirement the ChangeRequest changes (same key).

Build the inventory: each Requirement with its key, priority and type,
marked **needs a story** (Functional, not **Wont**) or **optional**; and the
actors and goals the PRD names.

**An unfinished run.** Last, `ls "$WIKI"/.worktrees/*/plan.md 2>/dev/null`
lists the runs that stopped part-way. When one is for this request (its
folder is `stories-<Key>`, or its plan's title names this request), read
`references/write-protocol.md` now and go on as its section 2 says, without
asking the rounds again.

## 2. Questions and the Intent gate

Read `references/story-rules.md` now.

Ask in rounds. A round is a numbered list of every question that can be
answered now, each with your recommended answer, so the person confirms or
corrects instead of composing an answer:

```text
Q1 - How should the coupon Requirements be grouped into stories?
     (features/FEAT-coupons/overview.md)
     ➡️ Two stories: STORY-coupons-apply-at-checkout and STORY-coupons-remove-coupon.
Q2 - What else in the wiki must change because of this?
     ➡️ Nothing: only story files and the folder's log.
```

- A recommendation that rests on the wiki cites the path. A question whose
  answer depends on another question in the same round waits for the next round.
- Ask at least one round, even when a brief seems complete: its questions are
  then the assumptions you would otherwise make without saying so.
- Which questions to ask, and how many, is your judgement.
- Always ask the wiki question: what else in the wiki must change because of
  this request, with your own answer as the recommendation.
- Wait for the answers, and ask another round when they open new questions.
  Search the wiki again whenever an answer brings a system, a term or a claim
  about current behaviour you have not read. When nothing that changes the
  output is left undecided, go to the Intent gate: one approval, after the
  rounds.

The first round names the target and its state, shows the inventory, and
proposes the stories: key, actor, goal and the Requirements each lists, split as
`references/story-rules.md` says. It asks the choices that are the person's:

- where one goal is cut into two stories;
- which actor a story is for when the PRD names several;
- the priority of each story;
- for a ChangeRequest, which Feature stories it affects.

When the brief or the person already names stories, take them as given, with
their wording: propose only the tracing, and report what they leave
uncovered. Do not split, merge or reword them yourself.

A criterion the person wants that no Requirement supports is not written. It is
a gap in the Requirements: name it under "For other skills" for
`sdlc-write-spec`, in the Run plan and in the summary. When the stories cannot
be written without it, stop before the Intent gate and name `sdlc-write-spec` as
the skill to run first.

The wiki question's usual answer is "nothing: only story files and the
folder's log".

**Intent gate.** Restate the target, the inventory and the proposed stories
(key, actor, goal, Requirements). Ask for approval.

## 3. Run plan and the Design gate

Read `references/write-protocol.md` and `references/story-format.md` now.

Start or resume the draft `stories-<Key>` as `write-protocol.md` section 2 and
section 3, "At section 3", say. The input paths are the target's `overview.md`
and, for a ChangeRequest, the changed Feature's `overview.md` and the Feature
stories it affects.

Prepare every story in full, with `references/story-format.md`: the
sentence, the numbered pass/fail criteria with real values, the
Requirements, and for
a ChangeRequest `# Affects`. Prepare the coverage matrix: each Requirement of
the inventory to the stories that list it, and each optional Requirement no
story lists.

Write the Run plan (`write-protocol.md` section 4). Its `## Files` are one line
per story file, added, changed or deleted, with its goal in a few words, each
Task or other story whose link to a deleted story is dropped, and each `log.md`
changed.

**Design gate.** Show every story as it will be written, never only a
summary, then the coverage matrix, then the Run plan. Ask for approval.

## 4. Write

In the draft worktree, in the Feature's or ChangeRequest's folder, write each
story as `STORY-<feature-name>-<name>.md`, with
`basedOn: { version: <the folder's Feature or ChangeRequest version>, at: <its versionDate> }`.
In a revision, keep each existing story's key, rewrite each story you touch
whole in the current form (`references/story-rules.md`, "Revisions"), and
give each story you revise, or checked against the new version, the current
`basedOn`. Delete a story whose Requirements were all removed, or that was
folded into another story, and change the links to it, as "Revisions" in
`references/story-rules.md` says. Add an entry to the folder's `log.md`, for
example
`* **Stories**: Wrote 3 user stories. Written by an AI model with sdlc-write-stories.`

Do not touch `overview.md`, the PRD or the changed Feature's stories, and
change a Task only to drop or replace a link to a deleted story. Linking Tasks
to the stories is `sdlc-plan-tasks`. Do not write `index.md`, `# Changed by`
or `# Test cases`: `draft finish` does.

**Input check.** `sdlc-design-arch` may merge while this draft is open, and
it writes the same `overview.md` (its `# Architecture` or `# Delta`, and the
status). When the input check of `write-protocol.md` section 3 shows that
file changed, compare only its `# Requirements` between `READ` and the
default branch. The same Requirements: the input did not change for this
step; go on. Different: show what changed and go back to section 3.

## 5. Self review, finish and commit

Read `references/paste-format.md` now. Follow `write-protocol.md` section 3, "At
section 5". In the self review (`write-protocol.md` section 5), have the review
sub-agent check by reading (with `references/story-rules.md`) that:

- each story is one actor's goal on one surface and passes the INVEST check
  of `references/story-rules.md`;
- no story is made only of RULEs of another story's SPINE;
- each criterion is a pass/fail statement with real values and cites only
  Requirements its story lists;
- no file outside the story files and the folder's `log.md` changed, except
  a dropped or replaced link to a deleted story and its log entry;
- every story of the folder has the current `basedOn`.

Then run `$T coverage stories` (which must report nothing) and `$T validate`
(no `story.*` or `ids.story-format` finding) in the worktree.

Commit message: `stories(<Key>): <n> user stories`, for example
`stories(FEAT-gift-cards): 3 user stories`.

Before the summary, print the paste-ready copy of each story added or
changed, as `references/paste-format.md` shows. It is not written to the
wiki. Then end with at most four lines:

```text
Done: wiki/stories-FEAT-coupons, 3 files, pushed. Open the pull request.
Not done: STORY-coupons-stacking (needs a new Requirement first)
For other skills: REQ-coupons-stacking is missing (sdlc-write-spec)
Next: sdlc-plan-tasks once the design is merged.
```

Leave out "Not done" and "For other skills" when they have nothing to say. Do
not list what the self review fixed, and do not repeat the stories. "Next" is
"`sdlc-plan-tasks` once the design is merged, even while the Requirements are
a draft"; when the folder already has Tasks, "run `sdlc-plan-tasks` again to
link the stories".

## Done when

- The target and the proposed stories were confirmed in the rounds, and the
  intent was approved at the Intent gate.
- Every story was shown in full and approved at the Design gate.
- Every Functional Requirement that is not **Wont** is listed by a story;
  every criterion cites a listed Requirement, and every listed Requirement is
  cited.
- The self review found nothing it could not fix, or the person accepted what
  was left at the Change-set gate.
- `coverage stories` reports nothing, `draft finish` was `ok`, the change set
  was approved, `draft commit` reported the branch, and the paste-ready copy
  was printed.
