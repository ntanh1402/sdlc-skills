# A change another skill owns

## Wiki
A copy (`cp -R`) of the directory kept by `sdlc-design-arch/first-feature.md`, with `main` holding the merged design.

## Request
"Design the tests for gift cards"

## Answers
- Choose `integration` and `e2e`; decline `load`, accepting the gap
- To the question about what else in the wiki must change: "yes, there are no Tasks for gift cards yet. Add a Task for writing these tests"
- Confirm the other recommendations
- Approve each gate

## Expected
- Writes no `TASK-*.md`
- Says Tasks are planned with `sdlc-plan-tasks`
- The Run plan has it under `## For other skills`
- The summary has a "For other skills" line naming `sdlc-plan-tasks`
- The diff holds only `tests/` and tool-written files
