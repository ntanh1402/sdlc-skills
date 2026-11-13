---
name: sdlc-design-story-tests
description: Design the test cases of one user story of a designed Feature or ChangeRequest in the project wiki, while its requirements are a draft or once they are agreed - the story's STORY group in the TestSuite of its Feature or ChangeRequest, proving every acceptance criterion, integration or e2e. Use when QA or developers need test cases for a user story, or when the story or the spec changed after its tests were designed. Not for end-to-end flows across stories or a whole Feature (sdlc-design-feature-tests), runnable test code, load tests, requirements, architecture or tasks.
---

# Design the tests of one user story

This skill is a lifecycle step after the design. It takes one user story of
a Feature or ChangeRequest whose design is merged, whether its Requirements
are a draft or agreed, and writes the story's group
`wiki/<app>/tests/TS-<name>/STORY-<name>/` in the TestSuite of that Feature
or ChangeRequest: cases that prove every acceptance criterion of the story.
Each case is a `TC-<id>-<name>.md` file. Flows across stories and cases tied
to no single story are written by `sdlc-design-feature-tests` in `GENERAL/`.
It never writes runnable test code or touches a code repository.

Its draft prefix is `tests-`: the draft for `STORY-coupons-apply` is
`wiki/tests-STORY-coupons-apply`. It may run at the same time as
`sdlc-plan-tasks`, `sdlc-design-feature-tests`, and itself for another story
of the same design.

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

Then read the schema pages `schema.md`, `test-suite.md`, `test-group.md`,
`test-case.md`, `user-story.md`, `feature.md`, `change-request.md`,
`architecture-decision.md` and the page of each Design type in scope, in the
wiki's `.wiki-llm/schema/`.

| Request | Skill |
|---|---|
| No approved design yet | `sdlc-design-arch` |
| No such story, or the story must change | `sdlc-write-stories` |
| End-to-end flows across stories, or tests of a whole Feature or ChangeRequest | `sdlc-design-feature-tests` |
| Build tasks | `sdlc-plan-tasks` |
| Runnable tests, or running them | Not this skill. `sdlc-build-task` writes a Task's unit tests with its code |
| Load or performance tests | Not kept in the wiki; no skill designs them |
| Which tests exist, or what is uncovered | `sdlc-ask-wiki` |

## The gates

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
- A refusal this file states is a refusal. Do not turn it into a question.

## 1. Look up: readiness and the inventory

Accept one `STORY-*` key; when the person names several stories, take one
and say the others are separate runs. Find the story on the default branch
(`ls wiki/*/features/*/<key>.md wiki/*/change-requests/*/<key>.md`); its
folder's Feature or ChangeRequest is the target. When it is not there,
look for it in the stories drafts
(`git branch -a --list 'wiki/stories-*' 'remotes/origin/wiki/stories-*'`,
then `git grep -l "" <branch> -- '*/<key>.md'` on each): a draft that holds
it is `NOT_MERGED`. A story in no draft is a refusal: route to
`sdlc-write-stories`. Read the target:

| State | When | Do |
|---|---|---|
| `READY` | A Feature `Draft`, `ReqApproved`, `Approved` or `InDev`, or a ChangeRequest `Proposed`, `ReqApproved` or `Approved`, whose `# Architecture` or `# Delta` is not `None` | Go on |
| `NEEDS_DESIGN` | `# Architecture` or `# Delta` is `None` | Stop: route to `sdlc-design-arch` |
| `NOT_MERGED` | The story or the target is not on the default branch, but a draft holds it (`wiki/stories-<target key>`, or `wiki/*-<target key>` for the target) | Stop and name the draft |
| `CLOSED` | A Feature that is `Released` or `Deprecated`, or a ChangeRequest that is `Implemented` or `Rejected` | Stop: say it is closed; a change to a Released Feature goes through a ChangeRequest (`sdlc-write-spec`); route nowhere else |

Every state but `READY` is a refusal, not a question.

Then read the story, every Requirement it lists, the Architecture or Delta,
the decisions, every Endpoint, Channel, Subscription, Table and External
contract the story's Requirements reach, the References the story links and
those about testing in `references/index.md`, and the existing TestSuite
that verifies the target (`grep -rl "<target key>" wiki/<app>/tests/*/overview.md`)
with its `STORY-<name>/` group, if any. Run `$T outdated --feature <Key>` (or
`--change <Key>`): the group, when listed, was designed from an older version
of the spec. When the design itself is listed, say in the first round that
the design is behind the spec and recommend `sdlc-design-arch` first; go on
only when the person says so. Run `$T validate` and keep the warnings about
this group (`tests.story-ac`, `tests.story-covers`): they are this skill's to
fix. List:

- every acceptance criterion of the story, by its number, as a partition of
  the Requirement it cites;
- for each criterion, the happy, alternate, validation and failure branches
  of the contracts it reaches;
- the authentication, authorization, privacy and abuse boundaries the
  criteria touch;
- retry, timeout, idempotency and duplicate handling on the story's path;
- the data the story writes or emits, and its integrity;
- the screens of the story with their access rule and their empty, loading,
  error and offline states, when a frontend is in scope;
- the cases of the existing group, with the criterion numbers they name.

**An unfinished run.** Last, `ls "$WIKI"/.worktrees/*/plan.md 2>/dev/null`
lists the runs that stopped part-way. When one is for this request (its
folder is `tests-<story key>`, or its plan's title names this story), read
`references/write-protocol.md` now and go on as its section 2 says, without
asking the rounds again.

## 2. Questions and the Intent gate

Read `references/test-design-rules.md` and
`references/security-checklist.md` now: the choices of section 3 use them.

Ask in rounds. A round is a numbered list of every question that can be
answered now, each with your recommended answer. The person confirms or
corrects, which is faster than composing an answer, and sees your reasoning
before any work is done.

```text
Q1 - Which categories should the cases of STORY-coupons-apply have?
     (features/FEAT-coupons/STORY-coupons-apply.md, services/SVC-orders/EP-coupon-apply.md)
     ➡️ functional, field-validation, negative and data-validation; security-validation is not needed: no auth rule changes.
Q2 - What else in the wiki must change because of this?
     ➡️ Nothing: only the story's group and its cases.
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

Wait for the answers. Ask another round when the answers open new questions.
Search the wiki again whenever an answer brings a system, a term or a claim
about current behaviour you have not read.
When nothing that changes the output is left undecided, go to the Intent gate:
one approval, after the rounds.

**A change another skill owns.** When an answer needs a wiki change this skill
does not own (such as an acceptance criterion or Requirement that cannot be
tested as written), do not make it. List it under "For other skills" in the
Run plan and in the summary. When your work depends on it, stop before the
Intent gate and name the skill to run first.

The first round names the story, its target and the target's state, shows
the inventory, and asks the person to choose the categories to write
(`test-case.md` lists them). Each case runs as one of two types:

- `integration`: one service and what it calls: datastores, externals,
  messages;
- `e2e`: the story's outcome across the deployed flow, through the owning
  frontend when there is one.

A developer's unit tests are written with the code (`sdlc-build-task`). Load
tests are not kept in the wiki.

The same round asks about the seams the cases test at, the exclusions, and
the wiki question; the usual answer to that one is "nothing: only the
story's group and its cases".

- A category the evidence requires (`references/test-design-rules.md`,
  "Required categories") may be declined only when the user explicitly
  accepts the residual risk; record that acceptance in the group's `log.md`.
- A step names the real table, topic, endpoint, cache key, bucket or index,
  from the design file's `tableName`, `channelName`, `method` and `path`,
  `keyPattern`, `bucket` or `indexName`. When a case needs one the design
  does not give, stop before the Intent gate, list the missing names, and
  route to `sdlc-design-arch`. Never write the wiki key or a made-up name
  instead.
- An acceptance criterion that cannot be tested as written is another
  skill's change: `sdlc-write-stories`; a Requirement or contract,
  `sdlc-write-spec`.
- A question about the criteria, the Requirements or the design that the
  person cannot answer now becomes an open question of the group; the group
  then stays `Draft`.
- When the Requirements are still a draft (`Draft`, `Proposed`), say so: the
  cases may have to change when the spec does.

**Intent gate.** Restate the story, the inventory, the chosen categories,
the seams, the exclusions, the open questions and the residual risk the
person accepted. Ask for approval.

## 3. What goes into the design

Read `references/case-format.md` now. For each criterion and chosen
category, partition inputs and branches with `references/test-design-rules.md`.
"All cases" means every criterion proved, with the branches and risks of its
partition, not every combination of inputs.

One suite per target: `TS-<name>`, the target's key without its prefix
(`FEAT-coupons` → `TS-coupons`, `CR-coupon-stacking` → `TS-coupon-stacking`).
When it does not exist, this run creates it. If the name is already taken by
the suite of another Feature or ChangeRequest, stop and ask.

This skill writes only the group `STORY-<name>/`, named exactly as the
story. Every case of it links the story under `# Covers` with the criteria it
proves (`— AC 1, 3`) and covers at least one Requirement the story lists.
Every criterion is proved by at least one case. A case that proves no
criterion of this story, such as a flow across stories, belongs in
`GENERAL/`: name it for `sdlc-design-feature-tests`. A case's id is the
highest id in the suite + 1, across all its groups; ids of deleted cases are
never reused.

**A story that changed.** When the story was revised after its cases were
written, fix every warning `validate` gives about the group: correct the
criterion numbers a case names (read the criteria, not only their numbers:
renumbered criteria give no warning), cover each criterion no case proves,
and move a case that covers none of the story's Requirements to `GENERAL/`,
keeping its id and dropping the story link from its `# Covers`, with an
entry in `GENERAL/log.md`. When the suite has no `GENERAL/` group yet,
create it with `status: Draft`, `basedOn` and a `# Scope` saying it holds
cases moved from story groups, so `sdlc-design-feature-tests` reviews them.
Show each change at the Design gate.

**A group designed from an older version.** Compare the spec at the version
in the group's `basedOn` with the current one (`git log -p` on the
`overview.md`). Revise the cases the change affects, add the cases it needs,
and delete the cases of removed Requirements as the last rule of
`test-case.md` says; leave the other cases as they are. Show each revised
case in full at the Design gate.

Each case is a file `TC-<id>-<behaviour words>.md` in the group, written
with `references/case-format.md`.

**Open questions.** An answer the person gave to a question under the
group's `# Open questions` is applied to the cases it affects; the question
is then removed and the answer logged in the group's `log.md`.

## 4. Run plan and the Design gate

Read `references/write-protocol.md` now.

Start or resume the draft `tests-<story key>` as `write-protocol.md` section
2 and section 3, "At section 4", say. The input paths are the story file and
its folder's `overview.md`.

Prepare the test design. Build the matrix from every criterion and inventory
row to its cases. The design is:

- the group with its seams, exclusions and open questions;
- each case: key, test type, category, risk, purpose, the criteria it
  proves and what else it covers;
- the coverage matrix by criterion, with every uncovered row and why;
- the totals by criterion, risk, type and category;
- assumptions and residual risks.

Write the Run plan (`write-protocol.md` section 4). Its `## Files` are the
suite's `overview.md` when it is new, the group's `overview.md` and
`log.md`, one line per case file with what it covers, and each case moved to
`GENERAL/` with `GENERAL/log.md` (and `GENERAL/overview.md` when new).

**Design gate.** Show the design in full, never only a summary, then the Run
plan. Ask for approval. Approval with an uncovered criterion is not
possible; approval with another uncovered in-scope row is allowed only when
the user explicitly accepts that gap as residual risk.

## 5. Write

In the draft worktree, under `wiki/<app>/tests/`:

- a new suite folder `TS-<name>/` with `overview.md` (`type: TestSuite`,
  `# Verifies` linking the Feature or ChangeRequest) when there is none;
- the group `TS-<name>/STORY-<name>/` with `overview.md` (`type: TestGroup`,
  `basedOn: { version: <the target's version>, at: <its versionDate> }`,
  `# Story` linking the story) and `log.md`;
- `status: Draft` while `# Open questions` has items, otherwise `Approved`;
- `# Open questions`, a numbered list, each question linking the
  criterion's story, Requirement, Design concept or decision it is about;
- one `TC-<id>-<name>.md` per new case in the group, with `testType` and
  `testCategory`;
- an entry in the group's `log.md`, for example
  `* **Test design**: Added 5 cases for STORY-coupons-apply. Written by an AI model with sdlc-design-story-tests.`

Every step and validation must make sense to a tester who did not design the
system and does not read the wiki. Do not write `index.md` or `checklist.csv`: `draft finish` writes
both. Do not change another group except to add a case moved to `GENERAL/`.

## 6. Self review, finish and commit

Follow `write-protocol.md` section 3, "At section 6", with the self review of
its section 5. In the self review, have the review sub-agent check by reading
that:

- every case has its test type, category, risk, concrete preconditions,
  complete steps, clean-up and links, and names the criteria it proves;
- every criterion of the story is proved by a case, and each named
  criterion says what the case proves;
- each Action starts with what to do and its target, copies the values it
  needs, and points at no other step or data; preconditions, steps and
  clean-up use real names, never a wiki key;
- each Expected result is one checkpoint per table, topic, cache entry, page
  or group of API fields, `- <field>: <value>` lines joined with `<br>`, and
  each Validation names the fields it checks in bold;
- ids are unique in the suite;
- no case is written twice, no existing case was changed except those the
  story or a newer spec version affects, and no runnable code was written;
- each step that calls an API or publishes to a channel has its request and
  expected response;
- the group's `basedOn` names the current version of its target, and it is
  `Draft` exactly when it has open questions;
- each accepted risk or gap is recorded in the group's `log.md`.

Then run `$T validate` in the worktree: no warning about this group may be
left.

Commit message: `tests(<story key>): design <n> cases`. In the summary, "Not
done" names each gap the user accepted and each open question, and "Next"
names `sdlc-design-feature-tests` when the target has flows across stories
and no `GENERAL/` group, and says the suite's `checklist.csv` lists its
cases.

## The summary

End the run with at most four lines:

```text
Done: wiki/tests-STORY-coupons-apply, 7 files, pushed. Open the pull request.
Not done: open question on AC 3 keeps the group Draft
For other skills: AC 2 of STORY-coupons-apply names no amount (sdlc-write-stories)
Next: sdlc-design-feature-tests FEAT-coupons for the flows across stories.
```

Leave out "Not done" and "For other skills" when they have nothing to say. Do
not list what the self review fixed, and do not repeat the test design: the
person approved the content at the gates, so the last message only says where
it is and what comes next.

## Done when

- The user chose the categories, and any declined required category has an
  accepted residual risk.
- Every acceptance criterion of the story is proved by a case, and every
  in-scope branch and risk is covered or the gap was accepted.
- Every case has concrete preconditions, self-contained steps with real
  names, checkpoint expected results, bold validations, clean-up and links,
  names the criteria it proves, and has a unique id; no case is duplicated;
  no runnable code was written.
- The self review found nothing it could not fix, or the person accepted what
  was left at the Change-set gate.
- `draft finish` was `ok`, the change set was approved, and `draft commit`
  reported the branch.
