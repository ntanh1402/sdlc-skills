# sdlc-review-code

Review a code change against the wiki. Read-only. [Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | Reviewer, developer |
| **Use when** | You review a branch, a working tree, a pull request, one commit or a commit range against the wiki: its Task's acceptance, the contracts in the wiki's design files, the Task's planned scope and the Application's conventions |
| **Needs first** | The change is in a local code folder |
| **Say** | "Review this branch against TASK-gift-card-redeem". One commit: "Review the SCRUM-175 commit in this folder", or "review commit 3f2a1c9" |
| **You get** | A list of findings **in the chat**, each marked **must fix** or **should fix**, with the code location and the wiki path. It changes nothing and gives **no verdict** |
| **Next** | Fix what you decide to fix, then merge the code pull request. After the merge, [sdlc-close-task](sdlc-close-task.md) |

It never edits code, writes to the wiki, changes a Task's status, runs tests
or posts comments to a hosting service. A person decides whether the code is
merged.

## What the skill does

1. Finds the wiki and reads its default branch.
2. Finds the change: everything between the merge-base with the default branch
   and your working tree, including new files; or, when you name one, a
   commit's diff or a range's. It reads changed files in full where the diff
   alone does not show what the code does.
3. Reads the Task (acceptance, linked Requirements, planned scope, design
   files), or, without a Task, the Service or frontend that matches this
   repository and the design files the change touches, plus `conventions.md`.
4. Checks five groups, including that each validation rule and each flowchart
   exit of an endpoint or consumer in scope exists in the code, and reports them in order: **Acceptance**, **Contract**,
   **Outside the scope**, **Convention**, **Not checked**.
5. Prints the report. The last line counts the findings, and names the wiki
   commit it read.

## What you do

- Name the code folder, and the Task if there is one. If you give none, the
  skill asks once ("None is an answer"), unless the commit you review ends
  with `Task: <key>`.
- To review a large Task commit by commit, name the commit or its subtask
  key; review the whole branch once, too, to check every acceptance item.
- Read the findings. Decide what to fix.
- If you think the wiki is the wrong side, say so; the skill names the remedy
  and changes nothing.

## Scenarios

| What happens | What the skill does | What you do |
|---|---|---|
| **You give a Task** | Reviews against that Task's acceptance, planned scope and design files | Fix, then merge |
| **No Task** | Finds the Service or frontend whose repository is this one, and reviews the design files the change touches. Differences in files with pending changes go to "Not checked" and it asks for the Task | Give the Task if you have one |
| **The repository is not in the wiki** | Says so under "Not checked": "this repository is not in the wiki; import it with sdlc-import" | Run [sdlc-import](sdlc-import.md) |
| **The change is empty** | Says so and stops | Check the branch |
| **You name a commit, a range or a subtask key** | Reviews only that diff, finding a subtask's commit by its `Subtask:` line on the branch and the Task by its `Task:` line. The first line names the commit; for a range, each finding names its commit. An acceptance item the commit does not touch goes to "Not checked" | Review the next commit; review the branch for the whole Task |
| **No commit, or several, has that `Subtask:` line** | Lists the branch's commits and asks which | Name it |
| **A design file is partly pending** (it holds the target) | Reviews the code against the target | Nothing |
| **Another Task or another request also covers the same design file** | Puts a difference to "Not checked" with that Task's or request's key, unless this Task's acceptance states it | Check it in the review of the other work |
| **The acceptance mentions something only a load test can show** (p95 latency) | Lists it under "Not checked" | Verify in your own tests |
| **A finding** | One line: severity, what is wrong, the code location, the wiki path | Fix it or dispute it |
| **A group has nothing** | Writes "none" under it | Nothing |
| **You ask "can I merge?"** | Never gives a verdict such as "approved". It reports findings only | You decide |
| **You say the design is wrong, not the code** | Names the remedy and changes nothing: a ChangeRequest with [sdlc-write-spec](sdlc-write-spec.md) | Run it. The finding stays in the report until the wiki changes |
| **You say the wiki is wrong about code that exists** | Names the remedy and changes nothing: [sdlc-import](sdlc-import.md) on the same folder | Run it |
| **You ask it to fix the code** | Refuses. [sdlc-build-task](sdlc-build-task.md) writes a Task's code | Fix it yourself or build the Task again |
| **You want a review of a wiki draft** | Not a skill. The approval gates and the pull request are that review | Review the pull request |
| **No wiki is linked** | Stops | Run [sdlc-setup-wiki](sdlc-setup-wiki.md) |
| **A review made against a Task** | Ends with one line: after the merge, close the Task with `sdlc-close-task` | Do it after the merge |

## Not this skill

| Request | Use |
|---|---|
| Fix the code, or write it | [sdlc-build-task](sdlc-build-task.md) |
| Record that the change is merged | [sdlc-close-task](sdlc-close-task.md) |
| The wiki is wrong about what is built | [sdlc-import](sdlc-import.md) |
| The design or stories should change | A ChangeRequest with [sdlc-write-spec](sdlc-write-spec.md) |
| A question about the wiki | [sdlc-ask-wiki](sdlc-ask-wiki.md) |
| A general review with no wiki | Not this skill |
