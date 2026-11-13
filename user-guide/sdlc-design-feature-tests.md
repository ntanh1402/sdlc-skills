# sdlc-design-feature-tests

Design the Feature-level test cases of a Feature or ChangeRequest from its
design: end-to-end flows across user stories, and every case tied to no single
story. It writes no test code. [Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | QA (and developers or security roles) |
| **Use when** | A designed Feature or ChangeRequest, draft or agreed, needs end-to-end or cross-story test design, or its spec changed after those tests were designed. The cases of one user story come from [sdlc-design-story-tests](sdlc-design-story-tests.md) |
| **Needs first** | The design pull request is merged. It may run at the same time as [sdlc-plan-tasks](sdlc-plan-tasks.md) and [sdlc-design-story-tests](sdlc-design-story-tests.md) |
| **Say** | "Design the end-to-end tests for gift cards" |
| **You get** | The `GENERAL/` group of the target's one TestSuite (`TS-<name>`, created when missing). Each case is a file `TC-<id>-<name>.md`, numbered from 1 across the suite, with its type (integration or e2e), category (functional, field validation, negative, error handling, data validation, security validation or integration), risk, preconditions with the data that must exist, and steps that use the real table, topic and endpoint names, with the request and expected response of each API call or message. Each expected result is a checkpoint per table, topic or response (`Table orders:<br>- Rows found: 2`), and each validation names the checked fields in bold. The group lists its open questions, records the spec version it was designed from (`basedOn`) and is approved on its own. The tool writes the suite's `checklist.csv`. Draft branch `wiki/tests-<Key>` |
| **Next** | Merge the pull request. Run [sdlc-design-story-tests](sdlc-design-story-tests.md) for each story the summary names. Your team writes and runs the test code; then [sdlc-import](sdlc-import.md) on that code marks the group `Implemented` |

## What the skill does

1. Checks readiness and builds the **inventory**: every PRD user flow that
   spans two or more stories, every nonfunctional Requirement no story lists, checks that
   apply across endpoints (authentication, authorization, abuse), retries,
   idempotency and ordering across services, data integrity and migration,
   frontend states, and any story group whose story is gone.
2. Asks the first round: which **flows** the e2e cases walk, which
   **categories** to write (it recommends the ones the evidence calls for),
   the seams and the exclusions.
3. **Intent gate.**
4. Designs the `GENERAL/` group. A case that proves one story's acceptance
   criteria is left to [sdlc-design-story-tests](sdlc-design-story-tests.md).
5. **Design gate:** shows the group, each case (key, type, category, risk,
   purpose, what it covers), the coverage matrix with every uncovered row and
   why, totals, open questions, assumptions and residual risks.
6. Writes the group and cases, checks coverage, **Change-set gate**, commit.
   The summary names every Requirement or story no case covers yet.

Every step and validation is written so that a tester who did not design the
system, and does not read the wiki, can follow it: each action says what to
do ("Call API `POST /orders`", "Publish message to topic `order.created`")
with the values it needs.

## What you do

- Choose the flows, the categories and the seams.
- Answer the open questions, now or in a later run; the group stays `Draft`
  until they are answered.
- Read the design at the Design gate. Accept a gap only deliberately.
- Merge the pull request. Write and run the test code yourself.

## Scenarios

| What happens | What the skill does | What you do |
|---|---|---|
| **The design is merged**, whatever the requirement status | Goes on. For a draft spec it says the cases may change with the spec | Answer the rounds |
| **The group was designed from an older spec version** | Revises the cases the change affects and adds the ones it needs; leaves the others | Check the revised cases at the Design gate |
| **The design itself is behind the spec** | Says so and recommends [sdlc-design-arch](sdlc-design-arch.md) first | Decide whether to go on |
| **There is no design yet** | Refuses and routes to [sdlc-design-arch](sdlc-design-arch.md) | Design first |
| **The design is in an unmerged draft** | Refuses and names the draft | Merge it |
| **The Feature or ChangeRequest is closed** | Refuses. A change to a Released Feature is a ChangeRequest | Run [sdlc-write-spec](sdlc-write-spec.md) |
| **You decline a category the evidence requires** | Allows it only if you explicitly accept the residual risk, and records that in the group's log | Say so explicitly, or keep the category |
| **A step needs a table, topic or endpoint whose real name the design does not give** | Stops before the Intent gate and lists the missing names. It never writes the wiki key or a made-up name | Run [sdlc-design-arch](sdlc-design-arch.md) to add them |
| **You cannot answer a question about the requirements or design yet** | Writes it under the group's `# Open questions` and keeps the group `Draft` | Answer it, then run the skill again |
| **A story was split, merged or deleted after its tests** | Moves the cases of the gone story's group to `GENERAL/`, keeping their ids, or names the story they now prove for [sdlc-design-story-tests](sdlc-design-story-tests.md) | Check the moves at the Design gate |
| **You ask for the tests of one story** | Routes to [sdlc-design-story-tests](sdlc-design-story-tests.md) | Run it |
| **A Functional Requirement has no story yet** | Writes no case for it; names [sdlc-write-stories](sdlc-write-stories.md), then [sdlc-design-story-tests](sdlc-design-story-tests.md) | Write the story first |
| **A Requirement or contract cannot be tested as written** | Does not work around it. Names [sdlc-write-spec](sdlc-write-spec.md) | Fix the requirement |
| **The suite name is taken by another Feature's or ChangeRequest's suite** | Stops and asks | Pick a name |
| **Some row cannot be covered** (a gap) | Lists it with the reason in the coverage matrix. You may accept it as residual risk at the Design gate. Each accepted gap is recorded in the group's log | Accept deliberately or ask for more cases |
| **You want runnable tests or load tests** | Does not write them. Load tests are not kept in the wiki | Your team writes them |
| **You want to know which tests exist or what is uncovered** | Not this skill | Ask [sdlc-ask-wiki](sdlc-ask-wiki.md) |

## Not this skill

| Request | Use |
|---|---|
| No approved design yet | [sdlc-design-arch](sdlc-design-arch.md) |
| The cases of one user story | [sdlc-design-story-tests](sdlc-design-story-tests.md) |
| Build tasks | [sdlc-plan-tasks](sdlc-plan-tasks.md) |
| User stories | [sdlc-write-stories](sdlc-write-stories.md) |
| Runnable tests, or running them | Not a wiki skill |
| Which tests exist, or what is uncovered | [sdlc-ask-wiki](sdlc-ask-wiki.md) |
