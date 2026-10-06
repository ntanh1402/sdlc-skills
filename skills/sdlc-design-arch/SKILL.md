---
name: sdlc-design-arch
description: Design and approve the target architecture of a Feature or ChangeRequest whose requirements are approved (ReqApproved) in the project wiki - the services, frontends, endpoints, events, data and externals it needs, their contracts, Mermaid diagrams, traceability and architecture decisions - and mark what is not built yet. Use when approved requirements need technical design, impact mapping, interface contracts or ADRs. Not for writing requirements, viewing an existing architecture, tasks, tests or code.
---

# Design the architecture

This skill is the second lifecycle step. It takes a Feature or ChangeRequest
with status `ReqApproved` and writes its approved target design:

- **Feature**: `# Architecture` filled, status `Approved`.
- **ChangeRequest**, in one change: `# Delta` filled, status `Approved`, and
  the target Feature's Requirements and Architecture updated to the new
  target.
- In both: every new or changed Design concept file written as its target,
  with a pending entry; decisions in `wiki/<app>/decisions/ADR-<name>.md`.

Its draft prefix is `arch-`: the draft for `CR-sms-alerts` is
`wiki/arch-CR-sms-alerts`.

## Before you start

Read, in this skill's folder, `references/read-protocol.md`,
`references/flow.md` and `references/write-protocol.md`. `flow.md` gives the
steps of the run and the three gates; this file says what is this skill's own
at each step. Then read `references/architecture-checklist.md`,
`references/contract-rules.md` and `references/adr-format.md`, and the schema
pages `schema.md`, `feature.md`, `change-request.md`,
`architecture-decision.md` and the page of every Design type you may touch, in
the wiki's `.wiki-llm/schema/`. When a Requirement is removed, also `user-story.md`
and `test-case.md`.

| Request | Skill |
|---|---|
| Show or explain an existing architecture | `sdlc-ask-wiki` |
| Requirements are missing, unclear or not approved | `sdlc-write-spec` |
| User stories | `sdlc-write-stories`; it runs at the same time as this skill |
| Build tasks, or test design, from an approved design | `sdlc-plan-tasks`, `sdlc-design-tests` |

When "design this" could mean several of these, ask one routing question.

## 1. Look up: readiness and what exists

Accept one `FEAT-*` or `CR-*` key; if the user named none, find the
`ReqApproved` candidates. Read it on the default branch and classify:

| State | When | Do |
|---|---|---|
| `READY` | `ReqApproved`, and Architecture (Feature) or Delta (ChangeRequest) is `None` | Go on |
| `NEEDS_SPEC` | `Draft` or `Proposed` | Stop: "The requirements of <Key> are not approved for design; ask its author to approve them with sdlc-write-spec." |
| `NOT_MERGED` | Not on the default branch, but a `wiki/*-<Key>` draft exists | Stop and name the draft (write protocol, section 3) |
| `ALREADY_DESIGNED` | `Approved` or later | Stop: a change to the design is a new ChangeRequest, written with `sdlc-write-spec` |
| `AMBIGUOUS` | Several candidates | One question that names them; write nothing until it is answered |
| `CONFLICT` | The requirements contradict an accepted decision or a live contract | Show both, with paths, in the first round and ask how to proceed |

Every state but `READY`, `AMBIGUOUS` and `CONFLICT` is a refusal, not a
question.

Then read the PRD and every Reference the Feature or ChangeRequest links,
every Requirement, the target Feature's current Architecture (for a
ChangeRequest), the accepted decisions in `decisions/`, every Design concept
the requirements touch, and the References in `references/index.md` about
the subject (an architecture document, a domain page, a code example): search
the Application's indexes and `grep -rl` for the domain words. For existing components, read
their linked repository, OpenAPI or AsyncAPI contracts when they are
available, read-only.

The wiki is the record. When code and wiki disagree, classify the difference
with `references/architecture-checklist.md` ("Drift"). Material Drift stops
the run before the Intent gate: show both sides, ask which is true, and name
the skill that settles it. It is a change another skill owns (`flow.md`,
section 4).

Also read the Tasks and TestSuites that already exist for the Feature: the
design may make them out of date.

## 2. Questions and the Intent gate

Ask in rounds, as `references/flow.md` section 4 says. The first round names
the target and its state, and puts to the person the choices of section 3
that are theirs to make, each with your recommendation and the wiki paths it
rests on: what is reused and what is new, how the parts talk to each other,
who owns new data, and each choice that will become a decision. It also
holds:

- any drift or conflict the lookup found;
- the wiki question, answered with the concepts you expect to add, change or
  remove;
- **downstream freshness.** The wiki does not know whether a `Todo` Task has
  started. List the existing Tasks and TestSuites the design will make out of
  date, and ask which of the `Todo` Tasks have started. Each started Task
  needs a separate, explicit acknowledgement.

Do not ask what the Requirements, an accepted decision or a live contract
already settle.

**Intent gate.** Restate the target, its Requirements, the systems you will
reuse or add, the decisions you expect, drift found, and the Tasks or
TestSuites that go out of date. Ask for approval (`DESIGN BASIS CONFIRMED`).

## 3. What goes into the design

Go Requirement by Requirement and flow step by flow step, and decide with
`references/architecture-checklist.md`:

- **Existing or new.** Reuse an existing Service, frontend, table or channel
  unless a different ownership or lifecycle boundary is proven. Never copy a
  concept to avoid changing it.
- **Interaction**: a synchronous Endpoint, an asynchronous Channel and
  Subscription, or an External Operation; request, response, payload,
  validation, errors, compatibility and version
  (`references/contract-rules.md`).
- **User interface**: only when a Requirement has one; which WebFrontend or
  MobileFrontend owns each surface. Never invent a frontend.
- **Data**: owner, read and write paths, schema, migration, retention, PII.
- **Security**: authentication, authorization, secrets, audit, abuse.
- **Failure**: idempotency, timeout, retry, ordering, dead letters, fallback,
  recovery.
- **Operation**: capacity, latency, availability, observability, rollout,
  rollback.
- **Decisions.** Every material, hard-to-reverse choice with a credible
  alternative becomes a decision (`references/adr-format.md`). Reuse an
  accepted decision that already covers it; supersede one only with a new
  decision.

Do not pick a technology before a constraint requires it.

**Descriptive fields.** A field whose schema page lists values as "common"
(`serviceType`, `deployTarget`, `platform`, `authType` and the like) is the
person's to choose. Suggest the values the Application already uses for it,
then the common ones, and ask in a question round when the evidence does not
settle it.

**References.** Link the References a later step will need from the Design
files and the Feature or ChangeRequest you write, under `# References`, with
a note on what to take from each: a code example of a pattern the design
reuses, a vendor document behind an Operation. Do not create a Reference;
when the design needs one the wiki lacks, say so at the Intent gate and name
`sdlc-edit-wiki` or `sdlc-import`.

## 4. Run plan and the Design gate

Start or resume the draft `arch-<Key>` as `references/write-protocol.md`
section 3 says. The input paths are the Feature's or ChangeRequest's
`overview.md` and its PRD, and for a ChangeRequest also the target Feature's
`overview.md`, which another ChangeRequest may change meanwhile.

Prepare the design packet:

1. Context and constraints.
2. The concept ledger: every concept new, modified, removed or reused, with the
   reason.
3. The high-level Mermaid `flowchart`, and one `sequenceDiagram` per main flow
   with its failure branches.
4. The contract of every new or changed concept, as its schema page requires.
5. The decisions, with alternatives.
6. Traceability: each Requirement to the concepts that satisfy it.
7. Drift, risks, rollout and rollback.
8. Downstream freshness: each existing Task or TestSuite this design makes out
   of date, and which `Todo` Tasks the person said have started.

Write the Run plan. Its `## Files` are the Feature's or ChangeRequest's
`overview.md` first, then for a ChangeRequest the target Feature's
`overview.md`, each Design concept file of the ledger that is not reused,
each decision file, and the `log.md` of every concept folder they are in. The
out-of-date Tasks and TestSuites go under `## For other skills`
(`sdlc-plan-tasks`, `sdlc-design-tests`); never edit them.

**Design gate.** Show the full packet, never only a summary, then the Run
plan. Ask for approval (`TARGET DESIGN APPROVED`). Any edit needs the gate
again.

## 5. Write

In the draft worktree, under `wiki/<app>/`. Write the Feature's or
ChangeRequest's `overview.md` first: it holds the diagrams, the decisions and
the traceability, so a run that stops after it can be resumed from the file.

- **Feature**: fill `# Architecture` with its nested sections in the schema's
  order (`## Context and constraints`, `## High-level architecture`,
  `## Services`, `## Frontends` only with a user interface,
  `## Runtime sequences`, `## Decisions`, `## Traceability`). Set
  `status: Approved`.
- **ChangeRequest**: fill `# Delta` (`## Target delta` with every concept
  qualified `new`, `modified` or `removed`, `## Runtime sequences`,
  `## Decisions`, `## Traceability`) and set `status: Approved`. In the same
  draft, update the target Feature's Requirements (the Feature's copy becomes
  the current text) and its `# Architecture` to the new target. When that
  removes a Requirement a Feature user story lists, fix those stories in the
  same draft as the last rule of `user-story.md` says, list them in the Run
  plan and show the edits at the Design gate. When it removes a Requirement
  that TestCases cover, fix those cases the same way, as the last rule of
  `test-case.md` says. A changed Requirement keeps its
  key: its stories stay as they are.
- **Design concepts**: write each new one as the full target with
  `status: Planned`; rewrite each changed one to the target with
  `status: Modifying`; set each removed one to `status: Removing` and keep its
  file. Give each a last section:

  ```markdown
  # Pending changes

  * [CR-sms-alerts](../../change-requests/CR-sms-alerts/overview.md) — modified — the SMS send path is not live yet.
  ```

  A concept that already has a `# Pending changes` section gets one more entry.
- **Calls** go under the caller's `# Calls`. Never write a reverse section
  (`# Used by`, `# Publishers`, `# Subscribers`, `# Superseded by`) or an
  `index.md`; the tool writes them.
- **Decisions**: `decisions/ADR-<name>.md` with `status: Accepted`, linked
  from `## Decisions`.
- **Logs**: an entry in the `log.md` of every concept folder you change, for
  example `* **Target design**: Designed the SMS channel for CR-sms-alerts. Written by an AI model with sdlc-design-arch.`

## 6. Self review, finish and commit

Follow `references/write-protocol.md` section 4 from step 5. In the self
review, also check by reading that:

- every Requirement appears in `## Traceability`;
- the diagrams match the prose and the contracts;
- every concept in `## Target delta` (or in `## Services` and `## Frontends`
  for a new Feature) exists and has its pending entry;
- no Task or TestSuite was edited, and no TestCase except by the removed-
  Requirement fix.

Commit message: `arch(<Key>): <title>`. In the summary, "For other skills"
lists the Tasks and TestSuites reported out of date, and "Next" is
"`sdlc-plan-tasks` and `sdlc-design-tests` after the merge".

## Done when

- The target and the design choices were confirmed in the rounds, and the
  design basis was approved at the Intent gate.
- Every Requirement maps to concrete target concepts.
- Existing systems were searched and reused where they fit.
- Interfaces, data, security, failure paths, quality targets and rollout are
  explicit.
- Every material one-way choice has an accepted decision.
- Every changed concept has its target status and pending entry.
- Downstream Tasks and TestSuites were confirmed current or reported out of
  date.
- The self review found nothing it could not fix, or the person accepted what
  was left at the Change-set gate.
- `draft finish` was `ok`, the change set was approved, and `draft commit`
  reported the branch.
