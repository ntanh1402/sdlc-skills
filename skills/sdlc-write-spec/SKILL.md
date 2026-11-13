---
name: sdlc-write-spec
description: Write and approve the requirements of a new Feature, or of a ChangeRequest to one existing Feature, in the project wiki - a PRD plus testable Requirements with a version, kept as a draft or marked ReqApproved once they are agreed; either can be merged, and design, stories, tasks and tests may start from a draft. Use when defining a new capability, turning a request or brief into requirements, writing a PRD, recording a bug, security, performance or refactor change to an existing feature, or revising requirements that are not yet Approved. Not for wiki questions, document conversion, architecture, tasks, tests or code.
---

# Write a spec

This skill is the first lifecycle step. Its output is exactly one of:

1. A **Feature**: `wiki/<app>/features/FEAT-<name>/` with `overview.md`
   (Requirements, `# Architecture` `None` until it is designed) and `log.md`,
   and its PRD, the Reference `wiki/<app>/references/REF-<name>-prd/`.
2. A **ChangeRequest** to one existing Feature:
   `wiki/<app>/change-requests/CR-<name>/` with `overview.md` (Requirements,
   `# Delta` `None — pending architecture` until it is designed) and
   `log.md`, and its change PRD, the Reference
   `wiki/<app>/references/REF-<name>-change-prd/`.

Each has a `version`, and the status says whether the Requirements are agreed
(`ReqApproved`) or still a draft (`Draft` for a Feature, `Proposed` for a
ChangeRequest). Both can be merged. The status is not a gate: architecture,
stories, Tasks and test cases may be written from a draft, and each records
the version it was written from.

Its draft prefix is `spec-`: the draft for `FEAT-coupons` is
`wiki/spec-FEAT-coupons`.

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

Then read the schema pages `schema.md`, `feature.md`, `change-request.md` and
`reference.md` in the wiki's `.wiki-llm/schema/`. When a revision removes a
Requirement, also `user-story.md`, `task.md` and `test-case.md`.

Other requests go elsewhere; say so and stop:

| Request | Skill |
|---|---|
| A question about the wiki, a list of features, an architecture view | `sdlc-ask-wiki` |
| A PDF, Word, slide or other non-text document as input | `sdlc-convert-doc` first, then this skill |
| A document, code or tests that describe something already built and running | `sdlc-import` |
| Architecture | `sdlc-design-arch`, from a draft or agreed spec |
| User stories, a story breakdown | `sdlc-write-stories`, from a draft or agreed spec |
| Build tasks, or test design | `sdlc-plan-tasks`, `sdlc-design-story-tests`, `sdlc-design-feature-tests` |
| An Application that does not exist yet | `sdlc-setup-wiki` ("add application `<key>`") |
| The code of a planned Task | `sdlc-build-task` |
| Recording that a Task's code is merged | `sdlc-close-task` |
| A typo, the glossary or conventions, a Feature marked released | `sdlc-edit-wiki` |
| A bug diagnosis, a release | not an sdlc-skills wiki skill |

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

## 1. Look up: target and mode

Read `references/interview-guide.md` now.

**Application.** Use the one the user names, else the one whose features match
the request's terms (`wiki/index.md`, `wiki/<app>/features/index.md`), else
the only one. None that exists: stop and route to `sdlc-setup-wiki`.

**Search before asking.** Search the Application for the outcome, actors,
domain words and any keys the user gave. Read the plausible Features, the
References they link (their PRDs among them), their Requirements and
Architecture, their open ChangeRequests, the References in
`references/index.md` about the subject, and the
frontends, services, channels, externals and datastores they link.

**Resolve an existing Feature** in this order, stopping at the first that
gives exactly one:

1. a `FEAT-*` key the user gave;
2. an exact title;
3. a Feature linked by a source or ChangeRequest the user gave;
4. the Feature whose recorded outcome owns the behaviour being changed.

Partial word overlap may prompt a question but never decides.

**Choose the mode and the file to write:**

| Situation | Mode |
|---|---|
| No Feature owns the capability | New Feature, status `Draft` |
| One Feature owns it and is `Draft` | Revise that Feature |
| One Feature owns it and is `ReqApproved` | Revise that Feature; it goes back to `Draft` until agreed again. Say so in the first round |
| One Feature owns it and is `Approved` or later | New ChangeRequest on that Feature, status `Proposed` |
| The request revises an open ChangeRequest that is `Proposed` or `ReqApproved` | Revise that ChangeRequest; a `ReqApproved` one goes back to `Proposed` |
| The request revises an `Approved` ChangeRequest | New ChangeRequest |

"New feature" in the request never overrides an exact match. Change language
with no Feature to change cannot silently become a new Feature. A
ChangeRequest changes exactly one Feature.

For a ChangeRequest, choose `changeType` and `riskLevel` with
`references/interview-guide.md` ("Change type and risk").

A brief or document that describes something already built and running, with
no Feature for it in the wiki, is not a spec to write. When the source reads
that way, ask once whether it is built; if it is, stop: "this is already
built; use sdlc-import to record it".

**An unfinished run.** Last, `ls "$WIKI"/.worktrees/*/plan.md 2>/dev/null`
lists the runs that stopped part-way. When one is for this request (its
folder is `spec-<Key>`, or its plan's title names this request), read
`references/write-protocol.md` now and go on as its section 2 says, without
asking the rounds again.

## 2. Questions and the Intent gate
Ask in rounds. A round is a numbered list of every question that can be
answered now, each with your recommended answer. The person confirms or
corrects, which is faster than composing an answer, and sees your reasoning
before any work is done.

```text
Q1 - Which Application and mode apply? No Feature covers coupon codes in shop
     (shop/features/index.md).
     ➡️ New Feature FEAT-coupons in shop, status Draft.
Q2 - What else in the wiki must change because of this?
     ➡️ Only FEAT-coupons and its PRD Reference REF-coupons-prd.
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

Wait for the answers. Ask another round when the answers open new questions.
Search the wiki again whenever an answer brings a system, a term or a claim
about current behaviour you have not read.
When nothing that changes the output is left undecided, go to the Intent gate:
one approval, after the rounds.

**A change another skill owns.** When an answer needs a wiki change this skill
does not own, do not make it. List it under "For other skills" in the Run plan
and in the summary. When your work depends on it, stop before the Intent gate
and name the skill to run first.


**The first round** puts what you found to the person, each as a question
with your answer as the recommendation and the wiki paths as evidence: the
Application, the mode, the target Feature or ChangeRequest and its status,
and, for a ChangeRequest, the change type and risk. Several plausible
Applications or target Features are one question that names the candidates;
write nothing until it is answered. The same round holds the questions about
the requirements that you can already ask.

**What to ask about** is in `references/interview-guide.md`: its readiness
list says what a Feature's or a ChangeRequest's intent needs before you stop
asking. When a brief or the conversation already covers the list, the round
is short: the assumptions you would make, the contradictions you found, and
the wiki question. Take what the brief states as given: its Requirements are
the Requirements, as many and as worded. Do not split, add or reword them
yourself. A flow, rule or event the brief describes without a Requirement of
its own stays in the PRD as context; do not ask whether to promote it. Beyond
the first-round items, ask at most two questions about scope, and only where
the brief contradicts itself or the wiki.

Choose keys from titles, never numbers:

- a Feature: `FEAT-<words>`, for example `FEAT-gift-cards`;
- a ChangeRequest: `CR-<words>`, for example `CR-gift-card-expiry`;
- a Requirement: `REQ-<feature words>-<words>`, for example
  `REQ-gift-cards-redeem-at-checkout`. A ChangeRequest that changes an existing
  Requirement reuses its key; a new one gets a name neither the Feature nor
  another open ChangeRequest on it uses. A removed Requirement is described in
  the PRD, never written as a new positive Requirement.

Check a new key is free: no such folder in the Application, and
`git branch -a --list 'wiki/*-<Key>'` shows no draft using it.

**Intent gate.** Restate the Application, the mode and the target; then the
outcome, users, why now, flow, each Requirement (key, priority, type,
verification), success measures, constraints, risks, assumptions, open
questions and what is out of scope. Ask for approval. A correction returns to
the rounds; a rejection writes nothing.

## 3. Run plan and the Design gate

Read `references/write-protocol.md` and `references/prd-templates.md` now.

Start or resume the draft `spec-<Key>` as `write-protocol.md` section 2 and
section 3, "At section 3", say. For a new Feature or ChangeRequest the input is
the Application and, for a ChangeRequest, the target Feature's `overview.md`; it
must be on the default branch.

Prepare the PRD with `references/prd-templates.md` and write it straight to
its content file in the worktree (`prd.md` or `change-prd.md` in the
Reference folder, as section 4 shows; in a revision, edit the content file of
the existing Reference). The PRD is the design and one of the outputs, so it
is written once: the person approves the text that will be committed, and a
resumed run still has it. Prepare a table mapping each Requirement to the PRD
sections it comes from.

**An older PRD in a revision.** When the existing PRD does not have the
headings of `references/prd-templates.md`, rewrite it whole in that shape as
part of this revision, and at the Design gate name each piece of its old
content that no new section takes (an `## Acceptance` list, `## Data and
events`) as a gap: dropped, moved to a Requirement, or kept under business
rules. Never revise a Feature or ChangeRequest only to reshape its PRD: that
would raise its version for no change in behaviour.

Write the Run plan (`write-protocol.md` section 4): its `## Files` are
`overview.md` and `log.md` in the Feature's or ChangeRequest's folder, and the
PRD's Reference folder: `overview.md`, `log.md` and the content file (already
ticked).

**Design gate.** Show the full PRD as the file holds it and the mapping, never
only a summary, then the Run plan, and ask two questions:

1. Is the PRD approved as written?
2. Are these requirements **agreed** (`ReqApproved`), or a draft to keep
   working on (`Draft` for a Feature, `Proposed` for a ChangeRequest)?
   Recommend the draft unless the person said they are agreed. Say that
   either one can be merged, and that the architecture, stories, Tasks and
   tests can start from a draft.

Make any edit to the PRD in its file; it needs the gate again. The person's
approval of the PRD is the approval the Reference needs.

## 4. Write

In the draft worktree, under `wiki/<app>/`:

**New or revised Feature** `features/FEAT-<name>/`:

```markdown
---
type: Feature
title: Gift cards
description: Let a customer pay with a gift card.
status: Draft
ownerTeam: checkout
version: 1
versionDate: 2026-10-02
priority: P1
---

# Gift cards

<two or three sentences: what the capability is and who it is for>

# Requirements

### REQ-gift-cards-redeem-at-checkout

**Must** — A customer can pay part or all of an order with a gift card balance.
Functional. Verified by test.

# Architecture

None

# References

* [REF-gift-cards-prd](../../references/REF-gift-cards-prd/overview.md) — the PRD these Requirements were written from.
```

A new Feature has `# Architecture` `None`. Write every Requirement out in
full; none says "see the PRD". Link other References that apply to the
Feature under `# References` too, with a note on what to take from each. In a
revision, keep everything you were not asked to change, and set the status
the Design gate decided. Never touch `# Architecture`, `# Delta` or
`designBasedOn`: they are `sdlc-design-arch`'s.

**Version.** A new Feature or ChangeRequest has `version: 1` and
`versionDate` today. A revision that changes a Requirement or the PRD adds 1
to `version` and sets `versionDate` to today; a revision that only changes
the status keeps both.

**Approved.** The Design gate's answer is the status, with one exception: a
**Feature** marked `ReqApproved` whose `designBasedOn` names its version
after this run (the architecture was designed from exactly these
Requirements) and that has no `Done` or outdated Tasks becomes `Approved`
instead. Say so at the Design gate. A Feature that already has a `Done` Task,
or a ChangeRequest, never becomes `Approved` here: approving it also updates
Design files or its target Feature, which is `sdlc-design-arch`'s.

**Stories, Tasks and TestCases after a removed Requirement.** A revision that
removes a Requirement a user story in the same folder lists fixes those
stories in the same draft, as the last rule of `user-story.md` says: drop the
Requirement and each criterion that links only it; delete a story left with
no Functional Requirement and drop the links to it. Nothing else in a story
changes. In any Task of the folder whose `# Acceptance` links the removed
Requirement, unlink `[REQ-x](overview.md#req-x)` to plain text `` `REQ-x` ``
so the Task's prose stays as built; `sdlc-design-arch` and `sdlc-plan-tasks`
plan a new Task to remove or adjust any already-built code. Fix the TestCases
that cover it the same way, as the last rule of `test-case.md` says. List
these files in the Run plan, show the edits at the Design gate and log them.

**New or revised ChangeRequest** `change-requests/CR-<name>/`: frontmatter
`type: ChangeRequest`, `title`, `description`, `status` (`Proposed` or
`ReqApproved`), `changeType`, `riskLevel`, optional `priority`,
`requestedBy`, `version`, `versionDate`; then the headings of `change-request.md` in order:
`# Changes` (one link to the Feature's `overview.md`), `# Reason`,
`# Requirements` (added and changed ones only), `# Delta` with
`None — pending architecture` (a revision keeps the Delta it has), and
`# References` linking `REF-<name>-change-prd`. Never edit the target
Feature.

**The PRD**, a Reference folder `references/REF-<name>-prd/` for a Feature or
`references/REF-<name>-change-prd/` for a ChangeRequest, as `reference.md`
says:

- `overview.md` summarises it and lists the content file:

  ```markdown
  ---
  type: Reference
  title: Gift cards PRD
  description: Product requirements for gift cards; read before changing how a customer pays with a gift card.
  status: Active
  ---

  # Gift cards PRD

  The product requirements the [Gift cards](../../features/FEAT-gift-cards/overview.md)
  Feature was written from: <one or two sentences on the objective and scope>.

  # Contents

  * [prd.md](prd.md) — the PRD as approved.
  ```

- The content file `prd.md` or `change-prd.md` was written in step 3 (with no
  frontmatter: `# Gift cards PRD`, then the sections of
  `references/prd-templates.md`).
- `log.md` starts as below, with a **PRD** entry.

**`log.md`** in each folder. A new folder starts with:

```markdown
# Gift cards — change log

Append-only history. Newest first.

## 2026-10-02

* **Spec**: Wrote the PRD and 4 Requirements; version 1, status Draft. Written by an AI model with sdlc-write-spec.
```

Do not write `generated`, `verified` or any `index.md`: `draft finish` does.

## 5. Self review, finish and commit

Follow `write-protocol.md` section 3, "At section 5", with the self review of
its section 5. The input paths for the input check are the Application's
`overview.md` (new Feature mode; not `features/index.md`, which the tool
rewrites whenever any Feature merges), the target Feature's `overview.md`
(ChangeRequest mode) and the file being revised (revision mode).

In the self review, have the review sub-agent also check by reading that:

- every Requirement is one testable behaviour or constraint, has a key,
  priority, type and verification, and maps to the PRD content file;
- the PRD Reference folder has its content file, `overview.md` and `log.md`,
  and the Feature or ChangeRequest links its Reference under `# References`;
- a ChangeRequest left the target Feature unchanged, and its `# Delta` is
  `None — pending architecture` unless it was already designed;
- `# Architecture`, `# Delta` and `designBasedOn` are as they were;
- `version` went up by exactly 1 when a Requirement or the PRD changed, and
  not otherwise, with `versionDate` today;
- the status matches `plan.md` (a Feature marked `ReqApproved` whose
  `designBasedOn` names its `version` after this run, with no `Done` or
  outdated Tasks, is `Approved`);
- no user story links a removed Requirement, and no Task's `# Acceptance`
  links one.

Commit message: `spec(<Key>): <title>`, for example
`spec(FEAT-gift-cards): Gift cards`.

**What the new version makes outdated.** After a revision that raised the
version, run `$T outdated --feature <Key>` (or `--change <Key>`) in the
worktree. It lists the design, stories, Tasks and TestSuites written from an
older version. Put them under "For other skills" in the summary, each with
the skill that rewrites it (`sdlc-design-arch`, `sdlc-write-stories`,
`sdlc-plan-tasks`, `sdlc-design-story-tests`, `sdlc-design-feature-tests`), and say that `sdlc-edit-wiki` can
record one as still current when the change does not touch it. Nothing is
stored: the list empties as those steps run.

"Next" in the summary, by the status and the design:

| After this run | Next |
|---|---|
| Not designed yet | "`sdlc-design-arch` after the merge, even while the Requirements are a draft; `sdlc-write-stories` at the same time if you want user stories" |
| Designed from an older version | "`sdlc-design-arch` again for the new version" |
| A Feature that became `Approved` | "`sdlc-plan-tasks`, `sdlc-design-story-tests` and `sdlc-design-feature-tests` after the merge, if not done yet" |
| A Feature or ChangeRequest `ReqApproved` whose design is current but that has an outdated Task (`$T outdated` lists a Task) | "`sdlc-plan-tasks` first: an approved target has no outdated Task. Then `sdlc-design-arch` again to approve it" |
| A ChangeRequest `ReqApproved` whose Delta is current, or a Feature `ReqApproved` whose Architecture is current and that already has `Done` Tasks, with no outdated Task | "`sdlc-design-arch` again to approve it: no redesign, it updates the Feature / Design files and sets the status" |
| A draft that is designed and current | "Mark the Requirements agreed with this skill when they are; the Tasks can be built and closed meanwhile" |

## The summary

End the run with at most four lines:

```text
Done: wiki/spec-FEAT-coupons, 5 files, pushed. Open the pull request.
Not done: features/FEAT-coupons/overview.md (refund coupon rule undecided)
For other skills: TASK-checkout-ui is outdated for version 2 (sdlc-plan-tasks)
Next: sdlc-design-arch after the merge, even while the Requirements are a draft.
```

Leave out "Not done" and "For other skills" when they have nothing to say. Do
not list what the self review fixed, and do not repeat the PRD: the person
approved the content at the gates, so the last message only says where it is
and what comes next.

## Done when

- The Application, mode and target were confirmed in the first round, and the
  intent was approved at the Intent gate.
- The PRD and the status were approved at the Design gate.
- The self review found nothing it could not fix, or the person accepted what
  was left at the Change-set gate.
- `draft finish` was `ok`, the change set was approved, and `draft commit`
  reported the branch.
