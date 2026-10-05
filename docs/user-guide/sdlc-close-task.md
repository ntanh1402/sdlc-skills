# sdlc-close-task

Record in the wiki that a Task's code is merged.
[Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | Developer |
| **Use when** | A Task's code pull request is merged |
| **Needs first** | The merge is on the code repository's default branch, with the `Task: <key>` line that [sdlc-build-task](sdlc-build-task.md) wrote in the commit message |
| **Say** | "Close TASK-gift-card-redeem; the code is in ../shop-orders" |
| **You get** | The Task `Done` with its merge commit and time; the design files it covered marked as built (live); and the Feature `InDev`, or the ChangeRequest `Implemented` once all its Tasks are `Done`. Draft branch `wiki/close-<TASK key>` |
| **Next** | Merge the close pull request. Close the ticket in your tracker yourself |

One Task per run. This skill uses the short form: no rounds and no Run plan.

## What the skill does

1. Finds the Task on the wiki's default branch, and refuses if it is `Done` or
   not merged.
2. Finds the **merged commit**: it fetches the code repository's remote default
   branch and searches for the `Task: <key>` line. The commit's hash and
   committer date become the Task's merge commit and merge time.
3. Asks one question: **"Was this change reviewed?"**
4. Works out the wiki changes and shows them file by file (**one stop** that is
   both Intent and Design gate).
5. Writes them, then the **Change-set gate**, commit.
6. Offers to remove the build worktree.

The changes it writes:

- the Task: `Done`, merge commit, merge time;
- each design item the Task covered: its pending entry removed, and when no entry
  is left its status becomes live (`Active`, or `Deprecated` for one that was
  `Removing`);
- the parent: a Feature `Approved` becomes `InDev`; a ChangeRequest whose other
  Tasks are all `Done` becomes `Implemented`.

## What you do

- Name the Task and the code folder.
- Answer whether the change was reviewed.
- Approve the file-by-file list, and the change set.
- Answer whether to remove the worktree.
- Merge the pull request. Close the tracker ticket by hand.

## Scenarios

| What happens | What the skill does | What you do |
|---|---|---|
| **The Task's trailer is on the remote default branch** | Takes the newest matching commit as the merge commit | Approve |
| **A squash merge dropped the trailer**, or the code was written by hand | Asks for the commit, then checks it is on the remote default branch | Give the commit |
| **The commit is only local or not merged** | Refuses: the Task is closed after the merge. A commit that is not on the remote's default branch is not merged | Merge first |
| **The folder has no remote** the skill can read, or the fetch fails | Refuses | Give a folder with a remote |
| **The Task is already `Done`** | Says so and names its merge commit if it has one | Nothing |
| **The Task is not on the default branch** | Names the draft that holds it | Merge it |
| **You answer "No" to "Was this change reviewed?"** | Says [sdlc-review-code](sdlc-review-code.md) checks a change against the wiki, and asks: review first, or close anyway? "Review first" ends the run. "Close anyway" goes on | Choose |
| **Another Task of the same parent also covers a design file** | Leaves that file's pending entry. It stays until the last Task covering it is closed | Nothing |
| **A design file still has an entry from another Feature or ChangeRequest** | Keeps the section and the status | Nothing |
| **A removed design item** | The file stays (this Task and its parent link it). Its status becomes `Deprecated` | Nothing |
| **The Feature is already `InDev`**, even when this was the last Task | Leaves it. Code merged is not code deployed | Deploy, then ask [sdlc-edit-wiki](sdlc-edit-wiki.md) to mark it `Released` |
| **A ChangeRequest has another `Todo` Task** | Leaves its status | Close the next Task |
| **Another close draft is open on the same parent and shares a design file** | Says so at the stop, naming the draft and the files, and goes on. After both merge, the wiki's checks report any pending entry left behind | Merge both, then check that no pending entry is left behind (ask [sdlc-ask-wiki](sdlc-ask-wiki.md) what is not live) |
| **The merged code differs from the design** | It does not compare. Names the remedies | [sdlc-import](sdlc-import.md) compares and corrects; a ChangeRequest when the design should change |
| **A build worktree exists** | Asks whether to remove it, and removes it only on a yes and only when it has no uncommitted change. It never deletes the branch | Answer |
| **You want the ticket closed or commented** | No skill does it. It offers to record the merge in the wiki and writes nothing until you ask | Do it in the tracker |
| **You want a Feature marked released** | Never. It only goes to `InDev` | [sdlc-edit-wiki](sdlc-edit-wiki.md) |
| **You reject the plan** | Writes nothing | Nothing |

## Not this skill

| Request | Use |
|---|---|
| Close, move or comment a ticket in a tracker | You, by hand |
| Write or fix the Task's code | [sdlc-build-task](sdlc-build-task.md) |
| Review before the merge | [sdlc-review-code](sdlc-review-code.md) |
| Mark a Feature released or deprecated; add a ticket link | [sdlc-edit-wiki](sdlc-edit-wiki.md) |
| Push, merge, or open a pull request | You |
