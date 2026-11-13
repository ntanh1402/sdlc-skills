# sdlc-design-story-tests

Design the test cases of one user story from its Feature's or ChangeRequest's
design, so that every acceptance criterion is proved. It writes no test code.
[Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | QA (and developers) |
| **Use when** | A user story of a designed Feature or ChangeRequest, draft or agreed, needs test cases, or the story or its spec changed after they were designed. Flows across stories come from [sdlc-design-feature-tests](sdlc-design-feature-tests.md) |
| **Needs first** | The design and the story are merged. It may run at the same time as [sdlc-plan-tasks](sdlc-plan-tasks.md), [sdlc-design-feature-tests](sdlc-design-feature-tests.md), and itself for another story |
| **Say** | "Design the tests for STORY-gift-cards-redeem" |
| **You get** | The story's group `STORY-<name>/` in the target's one TestSuite (`TS-<name>`, created when missing). Each case is a file `TC-<id>-<name>.md`, numbered from 1 across the suite, that names the acceptance criteria it proves (`— AC 1, 3` after the story link), with its type (integration or e2e), category, risk, preconditions with the data that must exist, and steps that use the real table, topic and endpoint names, with the request and expected response of each API call or message. Each expected result is a checkpoint per table, topic or response (`Table orders:<br>- Rows found: 2`), and each validation names the checked fields in bold. Every criterion is proved by at least one case. The group lists its open questions, records the spec version it was designed from (`basedOn`) and is approved on its own. The suite's `checklist.csv` shows the criteria each case proves. Draft branch `wiki/tests-<story key>` |
| **Next** | Merge the pull request. Run [sdlc-design-feature-tests](sdlc-design-feature-tests.md) for the flows across stories if not done. Your team writes and runs the test code; then [sdlc-import](sdlc-import.md) on that code marks the group `Implemented` |

## What the skill does

1. Finds the story's Feature or ChangeRequest, checks readiness, and builds
   the **inventory**: every acceptance criterion by number, the branches of
   the contracts each reaches, security boundaries, retries and idempotency
   on the story's path, the data it writes, its screens, and what the
   existing group already covers.
2. Asks the first round: which **categories** to write (it recommends the
   ones the evidence calls for), the seams and the exclusions.
3. **Intent gate.**
4. Designs the story's group: every case links the story with the criteria
   it proves and covers one of the story's Requirements.
5. **Design gate:** shows the group, each case (key, type, category, risk,
   purpose, criteria proved), the coverage matrix by criterion, totals, open
   questions, assumptions and residual risks. A criterion no case proves
   cannot be approved.
6. Writes the group and cases, checks them, **Change-set gate**, commit.

## What you do

- Choose the categories and the seams.
- Answer the open questions, now or in a later run; the group stays `Draft`
  until they are answered.
- Read the design at the Design gate.
- Merge the pull request. Write and run the test code yourself.

## Scenarios

| What happens | What the skill does | What you do |
|---|---|---|
| **The design and the story are merged**, whatever the requirement status | Goes on. For a draft spec it says the cases may change with the spec | Answer the rounds |
| **You name several stories** | Takes one; each other story is a separate run | Run it again for the next story |
| **There is no such story** | Refuses and routes to [sdlc-write-stories](sdlc-write-stories.md) | Write the story first |
| **The story was revised after its cases** (a criterion added, removed or renumbered) | Fixes the criterion numbers the cases name, covers each new criterion, and moves a case that covers none of the story's Requirements to `GENERAL/`, keeping its id and dropping its story link (it creates a `Draft` `GENERAL/` group when there is none) | Check the changes at the Design gate |
| **The group was designed from an older spec version** | Revises the cases the change affects and adds the ones it needs; leaves the others | Check the revised cases at the Design gate |
| **There is no design yet** | Refuses and routes to [sdlc-design-arch](sdlc-design-arch.md) | Design first |
| **The Feature or ChangeRequest is closed** | Refuses. A change to a Released Feature is a ChangeRequest | Run [sdlc-write-spec](sdlc-write-spec.md) |
| **A step needs a table, topic or endpoint whose real name the design does not give** | Stops before the Intent gate and lists the missing names | Run [sdlc-design-arch](sdlc-design-arch.md) to add them |
| **A criterion cannot be tested as written** | Does not work around it. Names [sdlc-write-stories](sdlc-write-stories.md) | Fix the criterion |
| **You cannot answer a question about the criteria or design yet** | Writes it under the group's `# Open questions` and keeps the group `Draft` | Answer it, then run the skill again |
| **You want a flow across stories** | Routes to [sdlc-design-feature-tests](sdlc-design-feature-tests.md) | Run it |
| **You want to know which tests exist or what is uncovered** | Not this skill | Ask [sdlc-ask-wiki](sdlc-ask-wiki.md) |

## Not this skill

| Request | Use |
|---|---|
| No approved design yet | [sdlc-design-arch](sdlc-design-arch.md) |
| End-to-end flows, or the tests of a whole Feature or ChangeRequest | [sdlc-design-feature-tests](sdlc-design-feature-tests.md) |
| Writing or changing a story | [sdlc-write-stories](sdlc-write-stories.md) |
| Runnable tests, or running them | Not a wiki skill |
| Which tests exist, or what is uncovered | [sdlc-ask-wiki](sdlc-ask-wiki.md) |
