---
name: sdlc-design-feature-tests
description: Design the Feature-level test cases of a designed Feature or ChangeRequest in the project wiki, while its requirements are a draft or once they are agreed - the GENERAL group of its one TestSuite, with end-to-end flows across user stories and every case tied to no single story, integration or e2e, each with a category, risk, concrete preconditions, self-contained steps that name real tables, topics and endpoints, request and response payloads, checkpoint-style expected results, bold validations and open questions - and report what no case covers yet. Use when QA, developers or security roles need end-to-end or cross-story test design for a whole Feature or ChangeRequest, or when the spec changed after those tests were designed. Not for the cases of one user story (sdlc-design-story-tests), runnable test code, load tests, requirements, architecture or tasks.
---

# Design the Feature-level tests

This skill is a lifecycle step after the design. It takes a Feature or
ChangeRequest whose design is merged, whether its Requirements are a draft or
agreed, and writes the `GENERAL/` group of its one TestSuite in
`wiki/<app>/tests/TS-<name>/`: end-to-end flows that span user stories, and
every other case tied to no single story. Each case is a
`TC-<id>-<name>.md` file. The cases of one user story are written by
`sdlc-design-story-tests` in that story's `STORY-<name>/` group. It never
writes runnable test code or touches a code repository.

Its draft prefix is `tests-`: the draft for `FEAT-coupons` is
`wiki/tests-FEAT-coupons`. It may run at the same time as `sdlc-plan-tasks`
and `sdlc-design-story-tests` on the same design.

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
| The cases of one user story | `sdlc-design-story-tests` |
| Build tasks | `sdlc-plan-tasks` |
| User stories | `sdlc-write-stories` |
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

Accept one `FEAT-*` or `CR-*` key. Read it on the default branch:

| State | When | Do |
|---|---|---|
| `READY` | A Feature `Draft`, `ReqApproved`, `Approved` or `InDev`, or a ChangeRequest `Proposed`, `ReqApproved` or `Approved`, whose `# Architecture` or `# Delta` is not `None` | Go on |
| `NEEDS_DESIGN` | `# Architecture` or `# Delta` is `None` | Stop: route to `sdlc-design-arch` |
| `NOT_MERGED` | Not on the default branch, but a `wiki/*-<Key>` draft exists | Stop and name the draft |
| `CLOSED` | A Feature that is `Released` or `Deprecated`, or a ChangeRequest that is `Implemented` or `Rejected` | Stop: say it is closed; a change to a Released Feature goes through a ChangeRequest (`sdlc-write-spec`); route nowhere else |

Every state but `READY` is a refusal, not a question.

Then read the Requirements, the Architecture or Delta, the decisions, every
Endpoint, Channel, Subscription, Table and External contract in scope, the
quality targets and risks, the PRD's user flows, the user stories in the
target's folder, the References they link and those about testing
in `references/index.md` (a test plan the user gave is one), and the existing
TestSuite that verifies the target (`grep -rl "<Key>" wiki/<app>/tests/*/overview.md`)
with all its groups. Run `$T outdated --feature <Key>` (or `--change <Key>`):
a group it lists was designed from an older version of the spec. When the
design itself is listed (`designBasedOn` older than `version`), say in the
first round that the design is behind the spec and recommend
`sdlc-design-arch` first; go on only when the person says so. Run
`$T validate` and keep the warnings about this suite (`tests.story-folder`,
`links.unresolved` in its files): a `STORY-*` group whose story is gone is
this skill's to fix. List:

- every PRD user flow that spans two or more stories;
- every nonfunctional Requirement and Constraint no story lists, and every
  Functional Requirement no story lists yet (it is not covered here: name it
  for `sdlc-write-stories`, then `sdlc-design-story-tests`, under "For other
  skills");
- checks that apply across endpoints or stories: authentication,
  authorization, privacy, audit and abuse boundaries;
- retry, timeout, idempotency, ordering, replay, dead letters and fallback
  that span services;
- data integrity, migration, compatibility, regression and clean-up;
- every new, changed or removed contract no story's cases will cover;
- every frontend route or screen with its access rule and its empty, loading,
  error and offline states, when a frontend is in scope;
- the performance and security risks the Requirements and decisions state;
- the cases of the existing `GENERAL/` group, and the cases of any stale
  `STORY-*` group.

**An unfinished run.** Last, `ls "$WIKI"/.worktrees/*/plan.md 2>/dev/null`
lists the runs that stopped part-way. When one is for this request (its
folder is `tests-<Key>`, or its plan's title names this request), read
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
Q1 - Which flows should the e2e cases of TS-coupons walk?
     (features/FEAT-coupons/overview.md#user-flows)
     ➡️ Apply a coupon and pay; apply, remove and pay. Both span STORY-coupons-apply and STORY-coupons-remove.
Q2 - Should security-validation cases be written?
     ➡️ No: no auth or PII rule changes.
Q3 - What else in the wiki must change because of this?
     ➡️ Nothing: only the suite's GENERAL group and its cases.
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
does not own (such as a Requirement or contract that cannot be tested as
written), do not make it. List it under "For other skills" in the Run plan and
in the summary. When your work depends on it, stop before the Intent gate and
name the skill to run first.

The first round names the target and its state, shows the inventory, and
asks the person to choose the flows the `e2e` cases walk and the categories
to write (`test-case.md` lists them). Each case runs as one of two types:

- `integration`: one service and what it calls: datastores, externals,
  messages;
- `e2e`: an actor outcome across the deployed flow, through the owning
  frontend when there is one.

A developer's unit tests are written with the code (`sdlc-build-task`). Load
tests are not kept in the wiki: a latency, throughput or capacity
Requirement is listed as not covered here.

The same round asks about the seams the cases test at, the exclusions, and
the wiki question; the usual answer to that one is "nothing: only the
suite's `GENERAL/` group and its cases".

- A category the evidence requires (`references/test-design-rules.md`,
  "Required categories") may be declined only when the user explicitly
  accepts the residual risk; record that acceptance in the group's `log.md`.
- A step names the real table, topic, endpoint, cache key, bucket or index,
  from the design file's `tableName`, `channelName`, `method` and `path`,
  `keyPattern`, `bucket` or `indexName`. When a case needs one the design
  does not give, stop before the Intent gate, list the missing names, and
  route to `sdlc-design-arch`. Never write the wiki key or a made-up name
  instead.
- A contract or Requirement that cannot be tested as written is another
  skill's change: `sdlc-write-spec`.
- A question about the Requirements, the acceptance criteria or the design
  that the person cannot answer now becomes an open question of the group;
  the group then stays `Draft`.
- When the Requirements are still a draft (`Draft`, `Proposed`), say so: the
  cases may have to change when the spec does.

**Intent gate.** Restate the target, the inventory, the flows, the
categories, the seams, the exclusions, the open questions and the residual
risk the person accepted. Ask for approval.

## 3. What goes into the design

Read `references/case-format.md` now. For each chosen category, partition
inputs and branches with `references/test-design-rules.md`. "All cases"
means complete coverage of the requirement, contract and risk partitions not
left to a story, not every combination of inputs.

One suite per target: `TS-<name>`, the target's key without its prefix
(`FEAT-coupons` → `TS-coupons`, `CR-coupon-stacking` → `TS-coupon-stacking`).
If it exists, add to it. If the name is already taken by the suite of
another Feature or ChangeRequest, stop and ask.

This skill writes only the `GENERAL/` group: an `e2e` case for each PRD
user flow that spans two or more stories, a check that applies across
endpoints or stories, a case for a nonfunctional Requirement or Constraint no
story lists. A Functional Requirement no story lists gets no case here: its
cases belong to the story `sdlc-write-stories` will write for it. A case that
proves one story's acceptance criteria belongs in that story's group, which
`sdlc-design-story-tests` writes; name the story and route there. A case's
id is the highest id in the suite + 1, across all its groups; ids of deleted
cases are never reused.

**A stale story group.** A `STORY-*` group whose story was split, merged or
deleted is a warning. Move each of its cases to `GENERAL/`, keeping its id
and dropping the link to the gone story from `# Covers`, log each move in
`GENERAL/log.md`, then delete the empty group folder and list its deleted
files in the Run plan's `## Files`; or, when a case now proves another story,
name that story for `sdlc-design-story-tests`. Show each move at the Design
gate.

**A group designed from an older version.** Compare the spec at the version
in the `GENERAL/` group's `basedOn` with the current one (`git log -p` on the
`overview.md`). Revise the cases the change affects, add the cases it needs,
and delete the cases of removed Requirements as the last rule of
`test-case.md` says; leave the other cases as they are. Show each revised
case in full at the Design gate.

Each case is a file `TC-<id>-<behaviour words>.md` in `GENERAL/`, written
with `references/case-format.md`.

**Open questions.** An answer the person gave to a question under the
group's `# Open questions` is applied to the cases it affects; the question
is then removed and the answer logged in the group's `log.md`.

## 4. Run plan and the Design gate

Read `references/write-protocol.md` now.

Start or resume the draft `tests-<Key>` as `write-protocol.md` section 2 and
section 3, "At section 4", say. The input paths are the Feature's or
ChangeRequest's `overview.md` and, for a ChangeRequest, the target Feature's
`overview.md`.

Prepare the test design. Build the matrix from every inventory row to its
cases; rows without their own wiki concept (a failure branch, a risk) are
added by hand. The design is:

- the group with its scope, seams, exclusions and open questions;
- each case: key, test type, category, risk, purpose, what it covers;
- the coverage matrix, with every uncovered row and why;
- the totals by Requirement, Design concept, risk, type and category;
- assumptions and residual risks.

Write the Run plan (`write-protocol.md` section 4). Its `## Files` are the
suite's `overview.md` when it is new, the group's `overview.md` and
`log.md`, and one line per case file with what it covers. When the user gave
a test plan that the wiki does not hold yet, add its Reference folder
`references/REF-<name>-test-plan/` (`overview.md`, `log.md` and the plan as a
content file); the Design gate is the person's approval of it.

**Design gate.** Show the design in full, never only a summary, then the Run
plan. Ask for approval. Approval with an uncovered in-scope row is allowed
only when the user explicitly accepts that gap as residual risk.

## 5. Write

In the draft worktree, under `wiki/<app>/tests/`:

- a new suite folder `TS-<name>/` with `overview.md` (`type: TestSuite`,
  `# Verifies` linking the Feature or ChangeRequest) when there is none;
- the group `TS-<name>/GENERAL/` with `overview.md` (`type: TestGroup`,
  `basedOn: { version: <the target's version>, at: <its versionDate> }`,
  `# Scope` saying which flows and checks it covers) and `log.md`;
- `status: Draft` while `# Open questions` has items, otherwise `Approved`;
- `# Open questions`, a numbered list, each question linking the
  Requirement, story, Design concept or decision it is about;
- one `TC-<id>-<name>.md` per new case in `GENERAL/`, with `testType` and
  `testCategory`;
- `# References` on the group that links the test plan it was written from,
  and any other Reference a tester needs, with a note on what to take from
  it;
- an entry in the group's `log.md`, for example
  `* **Test design**: Added 4 cases for FEAT-coupons. Written by an AI model with sdlc-design-feature-tests.`

Every step and validation must make sense to a tester who did not design the
system and does not read the wiki. Do not write `index.md` or `checklist.csv`: `draft finish` writes
both. Do not change a `STORY-*` group except to empty a stale one.

## 6. Self review, finish and commit

Follow `write-protocol.md` section 3, "At section 6", with the self review of
its section 5. In the self review, have the review sub-agent check by reading
that:

- every case has its test type, category, risk, concrete preconditions,
  complete steps, clean-up and links;
- each Action starts with what to do and its target, copies the values it
  needs, and points at no other step or data; preconditions, steps and
  clean-up use real names, never a wiki key;
- each Expected result is one checkpoint per table, topic, cache entry, page
  or group of API fields, `- <field>: <value>` lines joined with `<br>`, and
  each Validation names the fields it checks in bold;
- ids are unique in the suite; no case proves only one story's criteria;
- no case is written twice, no existing case was changed except those a
  newer spec version affects, and no runnable code was written;
- each step that calls an API or publishes to a channel has its request and
  expected response;
- the group's `basedOn` names the current version of its target, and it is
  `Draft` exactly when it has open questions;
- `GENERAL/` has an `e2e` case for each PRD user flow that spans two or more
  stories;
- each accepted risk or gap is recorded in the group's `log.md`.

Then run `$T coverage tests --feature <FEAT>` (or `--change <CR>`) in the
worktree, and `$T validate`: no warning about this suite may be left except
in a `STORY-*` group that `sdlc-design-story-tests` owns.

Commit message: `tests(<Key>): design <n> Feature-level cases`. In the
summary, "Not done" names each gap the user accepted, each open question,
and each Requirement or story that no case of any group covers yet, and
"Next" names `sdlc-design-story-tests` for each story whose group is missing
or behind, and says the suite's `checklist.csv` lists its cases.

## The summary

End the run with at most four lines:

```text
Done: wiki/tests-FEAT-coupons, 5 files, pushed. Open the pull request.
Not done: no case covers STORY-coupons-remove yet
For other skills: REQ-coupons-expiry lacks an exact timezone rule (sdlc-write-spec)
Next: sdlc-design-story-tests STORY-coupons-remove; TS-coupons/checklist.csv lists the cases.
```

Leave out "Not done" and "For other skills" when they have nothing to say. Do
not list what the self review fixed, and do not repeat the test design: the
person approved the content at the gates, so the last message only says where
it is and what comes next.

## Done when

- The user chose the flows and categories, and any declined required
  category has an accepted residual risk.
- Every in-scope flow, cross-story check, contract, branch and risk is
  covered, or the gap was accepted.
- Every case has concrete preconditions, self-contained steps with real
  names, checkpoint expected results, bold validations, clean-up and links,
  and a unique id; no case is duplicated; no runnable code was written.
- The self review found nothing it could not fix, or the person accepted what
  was left at the Change-set gate.
- `draft finish` was `ok`, the change set was approved, and `draft commit`
  reported the branch.
