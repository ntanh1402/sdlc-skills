# First plan

## Wiki
A copy (`cp -R`) of the directory kept by `sdlc-design-arch/first-feature.md`, with `main` holding the merged design.

## Request
"Plan the tasks for gift cards"

## Answers
- Confirm the recommendations of each round
- Approve each gate

## Expected
- `READY`
- The first round names `FEAT-gift-cards`, shows the scope inventory, and asks its numbered questions with a recommendation each; a round asks what else in the wiki must change
- One Intent gate, after the rounds
- The Design gate shows one row per Task with its repository, the coverage matrix, the waves and the Run plan
- At the Design gate, `<wiki>/.worktrees/tasks-FEAT-gift-cards/plan.md` lists one line per Task file and the folder's `log.md`
- The Change-set gate says what the self review checked and fixed, as `## Self review` of the Run plan records it
- Every new and changed concept has exactly one owning Task
- Sizes XS–L
- `TASK-*.md` files in `FEAT-gift-cards/`, `status: Todo`, no `trackerKey`
- `coverage tasks --feature FEAT-gift-cards` empty on the branch
- Branch `wiki/tasks-FEAT-gift-cards` pushed; `plan.md` is not in it; `validate` ok
- The last message is the summary, at most four lines; "Next" names the Tasks of the first wave
- **Keep this directory**: merge the branch into `main` and push; `sdlc-plan-tasks/stories-later.md` copies it
