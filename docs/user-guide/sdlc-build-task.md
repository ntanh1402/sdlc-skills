# sdlc-build-task

Write the code and unit tests of one wiki Task, on a branch of its own.
[Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | Developer |
| **Use when** | You implement one Task of the wiki |
| **Needs first** | The Task is merged and `Todo`, and its Feature (or ChangeRequest) is `Approved` (a Feature may be `InDev`). You name the code folder |
| **Say** | "Build TASK-gift-card-redeem in this folder" |
| **You get** | The code and its unit tests, committed on a new branch (`task/<name>`, unless your conventions name branches differently) in a git worktree at `<code folder>/.worktrees/<name>/`. The commit message ends with `Task: <key>`. **Nothing is pushed and nothing is run** |
| **Next** | Build and run the tests yourself, push, open the pull request, have it reviewed ([sdlc-review-code](sdlc-review-code.md)), merge it, then [sdlc-close-task](sdlc-close-task.md) |

It writes code, never the wiki. It never changes a Task's status.

## What the skill does

1. Checks that the wiki matches the skill (release check) and refuses if not.
2. Reads the Task (acceptance, linked Requirements, planned scope, stories for
   context), the contract of each design item in scope (the **target**), the
   parent's architecture and decisions, and the Application's `conventions.md`
   (coding standards, branching, testing policy, definition of done). Then it
   reads your code: layout, where each item lives, how unit tests are written.
3. Asks the first round: the branch name and worktree path, where each scope
   item goes when the code allows more than one place, anything not in this
   folder, and any blocker that is not `Done`.
4. **Intent gate.**
5. Creates a worktree on a new branch, so your own checkout is not touched, and
   writes a **Run plan** (`plan.md`) that lists each code and test file with the
   scope item and acceptance item it serves.
6. **Design gate:** the Run plan, in full. For code, the plan is the design.
7. Writes the code and unit tests to match the code around it.
8. Self review by reading (acceptance, contract, outside the scope,
   convention).
9. **Change-set gate:** the diff, the commit message, and what the self review
   could not fix. It deletes the Run plan and commits. It does not push.

## What you do

- Name the Task and the code folder. "This folder" is an answer.
- Approve the branch, the worktree and the Run plan.
- Review the diff at the Change-set gate.
- Afterwards: build, run the tests, push, open the pull request, merge.

## Scenarios

| What happens | What the skill does | What you do |
|---|---|---|
| **The Task is ready** | Builds it as described | Review and push |
| **The Task is not on the default branch** | Refuses. Names the draft that holds it (`wiki/tasks-…`), or [sdlc-plan-tasks](sdlc-plan-tasks.md) if there is none | Merge it |
| **There is no Task for this code** | Refuses. Not this skill | Plan the Task first with [sdlc-plan-tasks](sdlc-plan-tasks.md) |
| **The Task is `Done`** | Refuses. Its code is merged | A further change is a new Task or a ChangeRequest |
| **The parent is not `Approved` or `InDev`** | Refuses: the design is not approved, or the work is closed | Check with [sdlc-ask-wiki](sdlc-ask-wiki.md) |
| **The folder is not a git repository** | Refuses | Give the right folder |
| **Several Applications have a Task with that key** | Asks which | Name it |
| **A Task it is blocked by is still `Todo`** | Says so in the first round and goes on only if you say so: that code may be merged and not yet closed in the wiki | Close the blocker with [sdlc-close-task](sdlc-close-task.md), or tell it to go on |
| **A scope item belongs to another repository** | Lists it under "Not built here" and builds only this folder's items | Run another build for the other folder |
| **The code allows more than one place for an item** | Recommends one with the file paths it relies on | Choose |
| **Your branch naming differs** | Follows `conventions.md` when it names a rule | Say if it is wrong |
| **You have uncommitted changes in your checkout** | Does not matter. It works in a worktree | Nothing |
| **The repository already tracks its own `plan.md`** | Uses `sdlc-plan.md` instead and never overwrites yours | Nothing |
| **The branch or worktree already exists** (an earlier run) | Never deletes either. Shows the commits and the Run plan and continues with what is left | Confirm the plan still stands |
| **The code cannot meet a design contract**, or needs one the wiki lacks | Stops at that point. It never codes past a contract that differs from the design. Shows the code location and the wiki path | Choose: change the design (ChangeRequest, [sdlc-write-spec](sdlc-write-spec.md)), or correct the wiki if it is wrong about code that exists ([sdlc-import](sdlc-import.md)) |
| **You say to go on without that part** | Leaves it out, moves it to "Not built here" and lists it as "Not done" | Plan the missing work |
| **The wiki's Task or design changed while it worked** | Notices at the self review, shows the change and goes back to the Design gate | Re-approve |
| **You reject the plan** | Removes the worktree and branch this run made. A resumed build is left alone | Nothing |
| **You expect it to run the tests** | It never runs tests, the build or the code. The pipeline and the reviewer say whether they pass, and the wiki records no test result | Run them yourself |
| **You expect a pull request** | It never pushes or opens one | Do it yourself |
| **You want runnable code for a wiki TestCase** | Not this skill. It writes unit tests only and touches no TestSuite | Your team writes it, then [sdlc-import](sdlc-import.md) |

## Not this skill

| Request | Use |
|---|---|
| Code with no Task in the wiki | [sdlc-plan-tasks](sdlc-plan-tasks.md) first |
| Review a code change | [sdlc-review-code](sdlc-review-code.md) |
| Record that the code is merged | [sdlc-close-task](sdlc-close-task.md) |
| Change requirements, design, stories or a Task | [sdlc-write-spec](sdlc-write-spec.md), [sdlc-design-arch](sdlc-design-arch.md), [sdlc-write-stories](sdlc-write-stories.md), [sdlc-plan-tasks](sdlc-plan-tasks.md) |
| Push, open a pull request, merge | You |
