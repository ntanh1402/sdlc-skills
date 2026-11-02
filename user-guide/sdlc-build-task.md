# sdlc-build-task

Write the code and unit tests of one wiki Task, on a branch of its own.
[Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | Developer |
| **Use when** | You implement one Task of the wiki |
| **Needs first** | The Task is merged and `Todo`. You name the code folder. A Feature or ChangeRequest that is not `Approved` yet gets a warning, not a refusal |
| **Say** | "Build TASK-gift-card-redeem in this folder". For one subtask of a large Task: "Build TASK-gift-card-redeem in this folder, subtask SCRUM-175: the redeem endpoint" |
| **You get** | The code and its unit tests, committed on a new branch (`task/<name>`, unless your conventions name branches differently) in a git worktree at `<code folder>/.worktrees/<name>/`. The commit message ends with `Task: <key>`; for a subtask, with `Subtask: <subtask key>` then `Task: <key>`, on the Task's branch. **Nothing is pushed and nothing is run** |
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
   folder, any blocker that is not `Done`, and, for a subtask, the part it
   covers when you did not say it.
4. **Intent gate.**
5. Creates a worktree on a new branch, so your own checkout is not touched (a
   later subtask reuses the Task's branch and worktree), and writes a
   **Run plan** (`plan.md`) that lists each code and test file with the scope
   item and acceptance item it serves.
   For each endpoint or consumer in scope, the plan also names where each
   validation rule and flowchart exit is coded and tested.
6. **Design gate:** the Run plan, in full. For code, the plan is the design.
7. Writes the code and unit tests to match the code around it.
8. Self review by reading (acceptance, contract, outside the scope,
   convention).
9. **Change-set gate:** the diff, the commit message, and what the self review
   could not fix. It deletes the Run plan and commits. It does not push.

## What you do

- Name the Task and the code folder. "This folder" is an answer.
- For a large Task split into subtasks in your tracker, run the skill once per
  subtask: name the subtask key and the part of the Task it covers
  (acceptance items, planned scope items or files). Each run adds one commit
  to the Task's branch.
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
| **The parent is not `Approved` yet**, or the Task was planned from an older spec version | Warns in the first round and goes on only if you say so: the Requirements may still change, and if they do, a new Task will be planned for the difference | Decide whether to build now |
| **The parent is closed** (`Released`, `Deprecated`, `Implemented`, `Rejected`) | Refuses: the work is closed | A further change is a ChangeRequest |
| **The folder is not a git repository** | Refuses | Give the right folder |
| **Several Applications have a Task with that key** | Asks which | Name it |
| **A Task it is blocked by is still `Todo`** | Says so in the first round and goes on only if you say so: that code may be merged and not yet closed in the wiki | Close the blocker with [sdlc-close-task](sdlc-close-task.md), or tell it to go on |
| **A scope item belongs to another repository** | Lists it under "Not built here" and builds only this folder's items | Run another build for the other folder |
| **The code allows more than one place for an item** | Recommends one with the file paths it relies on | Choose |
| **Your branch naming differs** | Follows `conventions.md` when it names a rule | Say if it is wrong |
| **You have uncommitted changes in your checkout** | Does not matter. It works in a worktree | Nothing |
| **The repository already tracks its own `plan.md`** | Uses `sdlc-plan.md` instead and never overwrites yours | Nothing |
| **The branch or worktree already exists** (an earlier run) | Never deletes either. Shows the commits and the Run plan and continues with what is left | Confirm the plan still stands |
| **You name a subtask and its part** | Builds only that part, on the Task's branch. The Intent gate restates the subtask, its part and what is left for other subtasks. The Run plan lists only its files. The commit message ends with `Subtask: <subtask key>` then `Task: <key>` | Build the next subtask the same way |
| **You name a subtask but not its part** | Asks which acceptance items, scope items or files it covers, without guessing | Say the part |
| **The branch already has commits of earlier subtasks** and no Run plan | Not a resumed build: keeps their commits, asks the rounds and the gates, and adds this subtask's commit on top. Its self review checks this subtask's part and that the earlier commits are untouched | Approve as usual |
| **The branch already has a commit for this subtask** | Says so and stops | Fold a fix into that commit yourself (`git commit --fixup`) |
| **A subtask's run stopped part-way** (its Run plan is still in the worktree) | Resumes it, as for any earlier run. When you name another subtask, it says so and stops until that one is finished | Confirm the plan still stands |
| **You name no subtask, but the branch has subtask commits** | Names the subtasks built and asks which subtask this run builds | Name it |
| **The code cannot meet a design contract**, or needs one the wiki lacks | Stops at that point. It never codes past a contract that differs from the design. Shows the code location and the wiki path | Choose: change the design (ChangeRequest, [sdlc-write-spec](sdlc-write-spec.md)), or correct the wiki if it is wrong about code that exists ([sdlc-import](sdlc-import.md)) |
| **You say to go on without that part** | Leaves it out, moves it to "Not built here" and lists it as "Not done" | Plan the missing work |
| **The wiki's Task or design changed while it worked** | Notices at the self review, shows the change and goes back to the Design gate | Re-approve |
| **You reject the plan** | Removes the worktree and branch this run made. A branch an earlier run made, with its subtask commits, is never deleted | Nothing |
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
