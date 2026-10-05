# sdlc-design-tests

Design TestSuites and TestCases from an approved design. It writes no test
code. [Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | QA (and developers, security or performance roles) |
| **Use when** | An `Approved` Feature or ChangeRequest needs test design: unit, integration, end-to-end, load or security |
| **Needs first** | The design pull request is merged. It may run at the same time as [sdlc-plan-tasks](sdlc-plan-tasks.md) |
| **Say** | "Design the tests for gift cards" |
| **You get** | TestSuites (`TS-…`) with one TestCase (`TC-…`) per file. Each case has its risk, concrete data, steps and validations, and together they cover every Requirement, contract and failure branch. Draft branch `wiki/tests-<Key>` |
| **Next** | Merge the pull request. Your team writes and runs the test code; then [sdlc-import](sdlc-import.md) on that code marks the suite `Implemented` |

## What the skill does

1. Checks readiness and builds the **inventory**: every Requirement, every new,
   changed or removed contract, every frontend route with its empty, loading,
   error and offline states, happy, alternate, validation and failure
   branches, security boundaries, retry/timeout/idempotency/ordering rules, data
   integrity and migration, and the performance and security risks.
2. Asks the first round: which **suite types** to build (it recommends the ones
   the evidence calls for), the seams each suite tests at, and the exclusions.
3. **Intent gate.**
4. Designs one suite per target and type (`TS-coupons-e2e`), one case per file.
5. **Design gate:** shows each suite, each case (key, risk, purpose, what it
   covers), the coverage matrix with every uncovered row and why, totals,
   assumptions and residual risks.
6. Writes the suites and cases, checks coverage, **Change-set gate**, commit.

Every step and validation is written so that a tester who did not design the
system can follow it.

## What you do

- Choose the suite types and the seams.
- Give numeric thresholds for load tests.
- Read the design at the Design gate. Accept a gap only deliberately.
- Merge the pull request. Write and run the test code yourself.

## Scenarios

| What happens | What the skill does | What you do |
|---|---|---|
| **The design is `Approved`** (or an `InDev` Feature) | Goes on | Answer the rounds |
| **The design is not approved** | Refuses and routes to [sdlc-design-arch](sdlc-design-arch.md) | Design first |
| **The design is in an unmerged draft** | Refuses and names the draft | Merge it |
| **The Feature or ChangeRequest is closed** | Refuses. A change to a Released Feature is a ChangeRequest | Run [sdlc-write-spec](sdlc-write-spec.md) |
| **You decline a suite type the evidence requires** | Allows it only if you explicitly accept the residual risk, and records that in the suite's log | Say so explicitly, or keep the type |
| **A load suite has no numeric threshold** in a Requirement, decision or SLO | Blocks it until you give one. It never invents a number | Give the threshold, or add it to the requirements |
| **A Requirement or contract cannot be tested as written** | Does not work around it. Names [sdlc-write-spec](sdlc-write-spec.md) | Fix the requirement |
| **A suite for this target and type already exists** | Adds to it. It never changes an existing case | Review the new cases |
| **Several suites match** | Stops and asks | Pick one |
| **A frontend is in scope** | Adds cases for each route or screen with its access rule and its empty, loading, error and offline states | Confirm |
| **Some row cannot be covered** (a gap) | Lists it with the reason in the coverage matrix. You may accept it as residual risk at the Design gate. Each accepted gap is recorded in the suite's log | Accept deliberately or ask for more cases |
| **You want runnable tests** | Does not write them. [sdlc-build-task](sdlc-build-task.md) writes a Task's unit tests with its code | Your team writes the rest |
| **The tests are written and merged** | Not this skill | Run [sdlc-import](sdlc-import.md) on the test code to mark the suite `Implemented` |
| **Tests and tasks drafts conflict** | Not a skill job | Merge one, ask your agent to run the tool's `refresh` on the other, then merge it |
| **You want to know which tests exist or what is uncovered** | Not this skill | Ask [sdlc-ask-wiki](sdlc-ask-wiki.md) |

## Not this skill

| Request | Use |
|---|---|
| No approved design yet | [sdlc-design-arch](sdlc-design-arch.md) |
| Build tasks | [sdlc-plan-tasks](sdlc-plan-tasks.md) |
| User stories (TestCases link Requirements, never stories) | [sdlc-write-stories](sdlc-write-stories.md) |
| Runnable tests, or running them | Not a wiki skill |
| Which tests exist, or what is uncovered | [sdlc-ask-wiki](sdlc-ask-wiki.md) |
