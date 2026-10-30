---
name: sdlc-design-tests
description: Design traceable integration and e2e TestSuites and TestCases in the project wiki from one user story or one Feature or ChangeRequest, draft or agreed - one case per file with concrete data, steps and validations, covering every acceptance criterion, requirement, contract, input field validation, failure branch, security and performance risk. Use when QA need test design or coverage for a STORY, FEAT or CR key. Not for runnable test code, requirements, architecture, tasks or stories.
---

# Design the tests of a story or a feature

This skill is a lifecycle step after the design. It takes one user story, or
one Feature or ChangeRequest, whose Feature or ChangeRequest has a merged
design, whether its Requirements are a draft or agreed, and writes TestSuites
in `wiki/<app>/tests/TS-<name>/`, each with one `TC-<name>.md` file per case.
It never writes runnable test code or touches a code repository.

Its draft prefix is `tests-`, keyed on the Feature or ChangeRequest the input
belongs to: the draft for `FEAT-coupons` or for one of its stories is
`wiki/tests-FEAT-coupons`. It may run at the same time as
`sdlc-plan-tasks` on the same design.

## Before you start

Read, in this skill's folder, `references/read-protocol.md`,
`references/flow.md` and `references/write-protocol.md`. `flow.md` gives the
steps of the run and the three gates; this file says what is this skill's own
at each step. Then read the rules of the cases, each in one place:

- `references/classification.md`: the test levels (`integration`, `e2e`),
  testing types and categories, polarity, risk, priority, techniques,
  coverage rules and field validation;
- `references/test-design-rules.md`: the required types and no false
  completeness;
- `references/case-format.md`: how a case is written;
- `references/security-load-checklists.md`: the `security` and
  `performance` checklists.

Then read the schema pages `schema.md`, `test-suite.md`, `test-case.md`,
`user-story.md`, `feature.md`, `change-request.md`,
`architecture-decision.md` and the page of each Design type in scope, in the
wiki's `.wiki-llm/schema/`.

| Request | Skill |
|---|---|
| No approved design yet | `sdlc-design-arch` |
| No user story yet, or the story must change | `sdlc-write-stories` |
| Unit tests, runnable tests, or running them | Not this skill: it designs `integration` and `e2e` cases only. `sdlc-build-task` writes a Task's unit tests with its code |
| Which tests exist, or what is uncovered | `sdlc-ask-wiki` |

## 1. Look up: readiness and the inventory

Accept one key. Its prefix sets the mode, and the mode sets how the cases are
grouped:

| Input | Mode | Source of the inventory | Cases grouped by |
|---|---|---|---|
| `STORY-*` | story | the story's numbered acceptance criteria and the Requirements each cites | acceptance criterion of the story |
| `FEAT-*` or `CR-*` | feature | every Requirement and acceptance outcome of the Feature or ChangeRequest | suite type: `integration`, `e2e` |

Any other key, such as a `TASK-*`, is refused: say that this skill takes a
story, a Feature or a ChangeRequest, and name the Feature or ChangeRequest
the key belongs to.

Find the file: a story in `<app>/features/FEAT-*/STORY-<name>.md` or
`<app>/change-requests/CR-*/STORY-<name>.md`. The Feature or ChangeRequest of
a story is the folder it is in. Read it on the default branch:

| State | When | Do |
|---|---|---|
| `NOT_FOUND` | No story, Feature or ChangeRequest has the key | Stop: route a story to `sdlc-write-stories`, a Feature or ChangeRequest to `sdlc-write-spec` |
| `READY` | The Feature is `Draft`, `ReqApproved`, `Approved` or `InDev`, or the ChangeRequest is `Proposed`, `ReqApproved` or `Approved`, and its `# Architecture` or `# Delta` is not `None` | Go on |
| `NEEDS_DESIGN` | `# Architecture` or `# Delta` is `None` | Stop: route to `sdlc-design-arch` |
| `NOT_MERGED` | Not on the default branch, but a draft holds it: a `wiki/*-<Key>` branch, or, for a story, any `wiki/*` branch whose tree has the story file (`git ls-tree -r --name-only <branch> -- wiki/ \| grep "/<Key>.md$"`, for each branch of `git branch -a --list 'wiki/*' 'remotes/origin/wiki/*'`) | Stop and name the draft |
| `CLOSED` | A Feature that is `Released` or `Deprecated`, or a ChangeRequest that is `Implemented` or `Rejected` | Stop: say it is closed; a change to a Released Feature goes through a ChangeRequest (`sdlc-write-spec`); route nowhere else |

Check `NOT_MERGED` before `NOT_FOUND`: a story is often written in the
`stories-<FEAT or CR>` draft, whose name does not hold the story key. Every
state but `READY` is a refusal, not a question. When a story's `basedOn` is
older than its Feature's or ChangeRequest's `version`, say in the first round
that it is behind the spec and recommend `sdlc-write-stories` first; go on
only when the person says so.

Then read the source of the inventory, the Requirements it cites, the
Architecture or Delta, the decisions, every Endpoint, Channel, Subscription,
Table and External contract in scope, the quality targets and risks, and the
References they link and those about testing in `references/index.md` (a
test plan the user gave is one).

Search the existing cases on the default branch **and** in every open test
draft, since a case that is not merged yet still counts:

```bash
for b in main $(git branch -a --format='%(refname:short)' --list 'wiki/tests-*' 'origin/wiki/tests-*'); do
  git ls-tree -r --name-only "$b" -- wiki/<app>/tests/ | grep -i "<pattern>"
done | sort -u
```

Use the default branch's name for `main`. Look for the TestSuites that verify
the target, the cases that already name the input key or cover the
Requirements and Design concepts in scope ("One behaviour has one case per
level" in `references/classification.md`), and what the test case ID needs
(step 3).

Run `$T outdated --feature <Key>` (or `--change <Key>`): a suite it lists was
designed from an older version of the spec. When the design itself is listed
(`designBasedOn` older than `version`), say in the first round that the
design is behind the spec and recommend `sdlc-design-arch` first; go on only
when the person says so.

List the inventory, for each acceptance criterion or Requirement of the
mode: the item, every Requirement it cites with its acceptance outcome, every
new, changed or removed contract, and every row of "Coverage rules" and of
"Field validation" in `references/classification.md` that applies to it.
Note each constraint a contract leaves out, to ask about.

## 2. Questions and the Intent gate

Ask in rounds, as `references/flow.md` section 4 says. The first round names
the input, its mode, its Feature or ChangeRequest and its state, shows the
inventory in the grouping of the mode, and asks the person to choose the
suite types and the testing types and categories. Recommend the ones that
apply, each with its evidence. The `functional` categories the coverage rules
require are chosen by default and only listed; ask about the
`non-functional` categories and about any `functional` one the person may
want to leave out.

The same round asks about the seams each suite tests at, the exclusions, the
constraints the contracts leave out, and the wiki question; the usual answer
to that one is "nothing: only suites and cases".

- A type the evidence requires (`references/test-design-rules.md`, "Required
  types") may be declined only when the user explicitly accepts the residual
  risk; record that acceptance in the suite's `log.md`.
- A performance case with no numeric threshold from a Requirement, decision
  or SLO is blocked until the user gives one. Ask for it; never invent it.
- A contract or Requirement that cannot be tested as written is another
  skill's change: `sdlc-write-spec`. An acceptance criterion of a story that
  cannot be tested as written is `sdlc-write-stories`' change.
- When the Requirements are still a draft (`Draft`, `Proposed`), say so: the
  cases may have to change when the spec does.

**Intent gate.** Restate the input and its mode, the feature code (step 3),
the inventory, the chosen suite types, testing types and categories, the
seams, the exclusions and the residual risk the person accepted. Ask for
approval. A new feature code is part of that approval.

## 3. What goes into the design

For each inventory item and each chosen type, derive the cases with the
techniques and coverage rules of `references/classification.md`. "All cases"
means complete coverage of the acceptance criterion, requirement, contract,
field and risk partitions, not every combination of inputs.

One suite per target and type: `TS-<target words>-<type>`, for example
`TS-coupons-e2e`, where the target is the input's Feature or ChangeRequest. If
one exists, add to it; if several match, stop and ask. An existing suite of
the target with `suiteType` `load` or `security` stays as it is: new
`performance` and `security` cases go in the suite of their level, and the
coverage matrix lists the cases of the old suite that already prove a row.

**A suite designed from an older version.** Compare the spec at the version
in its `basedOn` with the current one (`git log -p` on the `overview.md`).
Revise the cases the change affects, add the cases it needs, and delete the
cases of removed Requirements as the last rule of `test-case.md` says; leave
the other cases as they are. Show each revised case in full at the Design
gate.

**Test case ID.** Each case has an ID that indexes it, unique in the
application: `TC-<FEATURE CODE>-<LEVEL>-<NNN>`, for example `TC-CPN-E2E-007`.
Every part is read with the search of step 1, on the default branch and in
every open test draft.

- `<FEATURE CODE>` is two to four capital letters, one per Feature or
  ChangeRequest in the application. Reuse the code its existing cases have
  (the code in their file names). When it has none, propose one from its
  name, check that no case file name and no `Feature code <CODE> for <Key>`
  line of a suite's `log.md` uses it, and ask for it at the Intent gate.
- `<LEVEL>` is `INT` or `E2E`, from the suite's `suiteType`.
- `<NNN>` is three digits: one more than the highest number the same code
  and level already have (search `/TC-<code>-<level>-`), then counting up. A
  number is never reused; a deleted case leaves a gap. When a draft is found
  only after the IDs were given (at the input check of
  `references/write-protocol.md`), renumber the new cases above its highest
  number before the Change-set gate.
- The file is named after the ID in lower case, followed by its behaviour
  words, which do not repeat the level:
  `TC-<feature code>-<level>-<nnn>-<behaviour words>.md`, for example
  `TC-cpn-e2e-007-expired-coupon-rejected.md`.
- The first `log.md` entry that uses a new code also says
  `Feature code CPN for FEAT-coupons.`

Write each case with `references/case-format.md`.

## 4. Run plan and the Design gate

Start or resume the draft `tests-<Key>` as `references/write-protocol.md`
section 3 says, where `<Key>` is the input's Feature or ChangeRequest. The
input paths are the story file in story mode, the Feature's or
ChangeRequest's `overview.md` and, for a ChangeRequest, the target Feature's
`overview.md`.

Prepare the test design. Build the matrix from every inventory item and row
to its cases; rows without their own wiki concept (a failure branch, a risk)
are added by hand. The design is:

- each suite with its type, seams and exclusions;
- each case: test case ID, key, risk, acceptance criterion, testing type,
  category, polarity, priority, purpose, what it covers;
- the coverage matrix in the grouping of the mode, with every uncovered row
  and why;
- the field matrix: for each entry point, each input field, each of its
  constraints and the values sent, with the case and data row that prove it,
  or why it is uncovered;
- the totals by group, Requirement, Design concept, risk, suite type, testing
  type, category, polarity and priority;
- assumptions and residual risks.

Write the Run plan. Its `## Files` are each new suite's `overview.md`, one
line per case file with what it covers, and the `log.md` of each suite.
When the user gave a test plan that the wiki does not hold yet, add its
Reference folder `references/REF-<name>-test-plan/` (`overview.md`, `log.md`
and the plan as a content file); the Design gate is the person's approval of
it.

**Design gate.** Show the design in full, never only a summary, then the Run
plan. Ask for approval. Approval with an uncovered in-scope row is allowed
only when the user explicitly accepts that gap as residual risk.

When the design holds more than about 30 cases, show it in parts, one group
of the mode at a time (an acceptance criterion in story mode, a suite type in
feature mode): first the totals and the coverage matrix of the whole design,
then each group's cases, and ask for approval of each group before the next.
The Design gate is passed when every group is approved; a change asked for in
a later group that touches an approved one shows that group again.

## 5. Write

In the draft worktree, under `wiki/<app>/tests/`:

- a new suite folder `TS-<name>/` with `overview.md` (`type: TestSuite`,
  `status: Approved`, `suiteType`, `basedOn`, `# Verifies` linking the
  Feature or ChangeRequest) and `log.md`;
- `basedOn` with one entry per target under `# Verifies`:
  `{ id: <key>, version: <its version>, at: <its versionDate> }`. On an
  existing suite, update the entry of the target you designed for;
- one case file per new case, named as step 3 says;
- `# References` on a suite that links the test plan it was written from,
  and any other Reference a tester needs, with a note on what to take from
  it;
- an entry in each changed suite's `log.md`, for example
  `* **Test design**: Added 9 cases for STORY-coupons-apply-code, TC-CPN-E2E-001 to TC-CPN-E2E-009. Written by an AI model with sdlc-design-tests.`

Every step and validation must make sense to a tester who did not design the
system. Do not write `generated` or `verified`, `index.md` or
`checklist.csv`: `draft finish` writes them.

## 6. Self review, finish and commit

Follow `references/write-protocol.md` section 4 from step 5. In the self
review, also check that:

- `$T coverage tests --feature <FEAT>` (or `--change <CR>`), run in the
  worktree, reports nothing uncovered for the Requirements in scope except
  the gaps the user accepted;
- every acceptance criterion (story mode) or Requirement (feature mode) has
  at least one case, and every row of the coverage and field matrices has
  its case and data row, or an accepted gap;
- every coverage rule of `references/classification.md` holds, checked one
  by one;
- every case follows each rule of `references/case-format.md`, checked one
  by one;
- every test case ID follows the "Test case ID" rules of step 3 (run the
  search of step 1 again), and no `unit` suite or `UNIT` ID was written;
- no existing case was changed except those a newer spec version affects,
  and no runnable code was written;
- each suite's `basedOn` names the current version of each target it was
  designed for;
- each accepted risk or gap is recorded in its suite's `log.md`.

Commit message: `tests(<input key>): design <n> cases`. In the summary, "Not
done" names each gap the user accepted, and "Next" says the suites can be
turned into runnable tests once the pull request is merged, and that each
suite's `checklist.csv` lists its cases.

## Done when

- The user chose the suite types, testing types and categories, and any
  declined required type has an accepted residual risk.
- Every inventory item is covered at `integration` or `e2e`, or the gap was
  accepted.
- The self review found nothing it could not fix, or the person accepted what
  was left at the Change-set gate.
- `draft finish` was `ok`, the change set was approved, and `draft commit`
  reported the branch.
