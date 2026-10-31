# Whole lifecycle

One agent session in one workspace, played as BA, SA, tech lead and QA in turn.
Each skill runs as its own Draft; the person merges each Draft into `main`
before the next step reads it.

## Wiki
`forward-tests/seed.sh <dir>`.

## Steps
1. **BA, `sdlc-write-spec`.**
   - Request: "Write the spec for gift cards: customers pay part or all of an order with a gift card balance"
   - Answers: confirm the target in the first round; answer the rounds, confirming the recommendations; approve the intent; approve the PRD as "approved for design"; approve the change set.
   - Then merge `wiki/spec-FEAT-gift-cards` into `main` and push.
2. **SA, `sdlc-design-arch`, and BA, `sdlc-write-stories`**, both started
   from the same `main`, before either is merged.
   - Requests: "Design the gift cards feature", then "Break gift cards into user stories".
   - Answers: confirm the design basis and supply the outside provider's API facts; approve the target design; approve the change set. Confirm the proposed stories; approve the stories and their change set.
   - Then merge `wiki/arch-FEAT-gift-cards`, then `wiki/stories-FEAT-gift-cards`, into `main` and push. If git reports a conflict in the stories draft, run `refresh` there, then merge and push.
3. **Tech lead and QA, `sdlc-plan-tasks` and `sdlc-design-tests`**, both started
   from the same `main`, before either is merged.
   - Requests: "Plan the tasks for gift cards", then "Design the tests for gift cards".
   - Answers: confirm the planning basis; approve the task plan and its change set; choose the test suite types and the load workload; approve the test design and its change set.
   - Then merge the tasks branch, then the tests branch. If git reports a conflict in the tests draft, run `refresh` there, then merge and push.
4. **`sdlc-ask-wiki`.**
   - Requests: "List the features", then "Show the gift cards architecture".

## Expected
On `main`:
- `validate` ok; `sync --check` ok
- `coverage tasks`, `coverage tests` and `coverage stories --feature FEAT-gift-cards` all empty
- Five merged branches with the prefixes `spec-`, `arch-`, `stories-`, `tasks-`, `tests-`
- Every user story is linked by a Task under `# Stories`
- Every `generated.by` written in the run is `<skill>/<Release version>`
- No model name in any file the run wrote or changed

The answers to the last two requests:
- "List the features" has one row per Feature; `FEAT-gift-cards` shows its pending concepts
- "Show the gift cards architecture" has the nine parts of the recipe, the stored diagrams, the 12 Requirements traced, and the Tasks and tests

## Second agent
Spec decision 15: repeat the run with a second coding agent, if one is
installed. The owner runs it before tag `1.0.0` if none was available.
