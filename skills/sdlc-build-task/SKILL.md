---
name: sdlc-build-task
description: Write the code and unit tests of one wiki Task in one code repository, against the project wiki - read the Task's acceptance and planned scope, the contracts of the Design files it covers and the Application's conventions, plan the files, write them in a git worktree on a branch of their own, check them against the wiki and commit with a Task trailer, without pushing. Use when a developer asks to build, implement or code a Task of the project wiki. Not for coding without a wiki Task, for changing the wiki, for running tests, for pushing or opening a pull request, or for closing the Task.
---

# Build a Task

This skill writes the code of one Task. Its input is a Task key and one code
folder. Its output is one commit on a new branch of that code repository, in
a worktree of its own, not pushed. The commit message ends with the line
`Task: <Task key>`, which `sdlc-close-task` later uses to find the merged
code.

A large Task is split into subtasks in the Tracker, and one run builds one
subtask: its commit goes on the Task's branch, after the commits of earlier
subtasks, and its message ends with `Subtask: <subtask key>` before the
`Task:` line.

It writes code, never the wiki: section 8 lists what it never does.

## Before you start

Read, in this skill's folder, `references/read-protocol.md`; each section names
the other `references/` files to read when it starts.

Find the wiki as the read protocol says, and check that it matches this
skill. `RELEASE`, next to this file, holds one line such as `1.0.0`:

```bash
cd "$WIKI" && $T copy check --release "<the line in RELEASE>"
```

Any `status` but `current` stops the run: say which side is older, and that
`sdlc-setup-wiki` upgrades the wiki. Then read the schema pages `task.md`,
`convention.md` and the page of each Design type in the Task's scope, in the
wiki's `.wiki-llm/schema/`.

Other requests go elsewhere; say so and stop:

| Request | Answer |
|---|---|
| Code with no Task in the wiki | Not this skill: plan the Task first with `sdlc-plan-tasks` |
| Review a code change | `sdlc-review-code` |
| Record that the code is merged | `sdlc-close-task` |
| Change the requirements, the design, the user stories or a Task | `sdlc-write-spec`, `sdlc-design-arch`, `sdlc-write-stories`, `sdlc-plan-tasks` |
| Runnable code for a TestCase, or running tests | Not an sdlc-skills skill |
| Push, open a pull request, merge | The person does that |

## The gates

A gate is a stop for the person's explicit approval. There are three, so the
person decides what is being done (Intent), how (Design), and exactly what is
saved (Change-set), each before the next cost is paid.

- Approval is an explicit yes to the gate's question. "Sounds good", silence
  or "whatever you think" is not approval.
- An edit at a gate reopens that gate and every later one.
- When you cannot ask the person (a run with no one to answer), or the person
  asks you to skip questions or approvals ("don't ask me, just write it"),
  stop before the first gate and start no worktree. Return the open decisions
  and the gates the work still needs. Never assume approval.
- When the person rejects the design, stop. A worktree and branch this run
  started are removed; those an earlier run started are left as they are.
- Being asked to run this skill does not approve anything it writes.
- A refusal this file states is a refusal. Do not turn it into a question.

## 1. Look up: the Task, the wiki and the code

**The input.** One Task key and one code folder. The user names the folder;
"this folder" is an answer. Never guess it. A Task changes one repository, so
a second folder is a second run.

**A subtask.** The person may also name a subtask: its Tracker key and the
part of the Task it covers, as acceptance items, planned scope items or files
("Build TASK-x in ../repo, subtask SCRUM-175: the event producer"). The run
then builds only that part. No skill reads the Tracker, so the key and the
part come from the person: when the part is not said, ask for it in the first
round, and never guess it. With no subtask named, the run builds the whole
Task.

Find the Task on the wiki's default branch:
`git ls-tree -r --name-only "$DEFAULT" -- wiki | grep '/TASK-<name>.md$'`.
When several Applications have a Task with that key, ask which.

**Refuse**, naming the reason and what to do instead, when:

| Case | Say |
|---|---|
| The Task is not on the default branch | Name the draft that holds it (`git branch -a --list 'wiki/tasks-*'`) and ask to merge it first; with no such draft, `sdlc-plan-tasks` |
| The Task is `Done` | Its code is merged. A further change is a new Task or a ChangeRequest |
| The parent Feature is `Released` or `Deprecated`, or the parent ChangeRequest is `Implemented` or `Rejected` | The work is closed |
| The code folder is not a git repository | `git -C "$SRC" rev-parse --show-toplevel` prints nothing |

A refusal is not a question.

**A spec that is not agreed yet.** When the parent is not `Approved` (a
Feature `Draft` or `ReqApproved`, a ChangeRequest `Proposed` or
`ReqApproved`), or `$T outdated` lists this Task (its `basedOn` is older than
the parent's `version`), say so in the first round and go on only when the
person says so: the Requirements may still change, and if they do,
`sdlc-plan-tasks` will plan a new Task for the difference.

**A blocker that is not `Done`.** When a Task under `# Blocked by` is `Todo`,
say so in the first round and go on only when the person says so: its code
may be merged and not yet closed in the wiki.

Uncommitted changes in the code folder do not matter. This skill works in a
worktree of its own and leaves the person's checkout as it is.

**Read**, on the wiki's default branch:

- the Task: `# Acceptance`, the Requirements it links, `# Planned scope`,
  and the user story under `# Stories`, if any, for the actor's goal and the
  acceptance criteria its code must satisfy (read only);
- each Design file in the scope: its contract, which is the target, and its
  `# Pending changes` entry for this Task's parent;
- the parent's `# Architecture` or `# Delta`, and the decisions it links;
- `<app>/conventions.md`: coding standards, branching, testing policy,
  definition of done;
- the References the Task, its parent and its Design files link under
  `# References`, and those in `<app>/references/index.md` about the scope:
  each overview, then the content or the code at `resource` it points to.
  Follow what each note says to take from it. A Reference is an example, not
  a contract: where it differs from the Task, a Design file or
  `conventions.md`, those win.

Take every rule under `# Validations` and every exit of `# Flowchart` of
each Endpoint and Subscription in scope as a checklist: the plan names where
each is coded and the unit test that covers it, and the check before the
commit ticks each one off.

Note the wiki commit you read: `READ=$(git -C "$WIKI" rev-parse "$DEFAULT")`.

Then read the code folder: how it is laid out, where each scope item lives or
will live, how its unit tests are written, and what the default branch is:

```bash
SRC=<the code folder>
git -C "$SRC" fetch --quiet origin 2>/dev/null
BASE=$(git -C "$SRC" symbolic-ref --quiet --short refs/remotes/origin/HEAD \
  || { git -C "$SRC" show-ref --verify --quiet refs/heads/main && echo main; } \
  || echo master)
```

`BASE` is the remote's default branch, else a local `main`, else `master`, so
a repository with no remote still works.

**An earlier run.** Last, when the branch or the worktree of section 3
already exists, locally or on `origin`, read `references/write-protocol.md`
now and go on as its section 2 says. It tells two cases apart: a run that
stopped part-way is resumed without asking the rounds again; the commits of
earlier subtasks are kept, and this run builds a new subtask on them after the
rounds and the gates.

## 2. Questions and the Intent gate

Ask in rounds. A round is a numbered list of every question that can be
answered now, each with your recommended answer. The person confirms or
corrects, which is faster than composing an answer, and sees your reasoning
before any work is done.

```text
Q1 - Where should EP-apply-coupon live in ../orders-svc? Existing order endpoints
     are in src/api/orders.py.
     ➡️ In src/api/orders.py, with unit tests in tests/test_orders.py.
Q2 - What else in the wiki must change because of this?
     ➡️ Nothing.
```

Which questions to ask, and how many, is your judgement. Three things are
fixed:

- **The format.** Numbered questions, each with a recommendation. A
  recommendation that rests on the wiki or the code cites the path. A question
  whose answer depends on another question in the same round waits for the
  next round.
- **At least one round**, even when a Task seems complete. Its questions are
  then the assumptions you would otherwise make without saying so.
- **The wiki question.** Ask what else in the wiki must change because of
  this request, with your own answer as the recommendation. Because this skill
  never writes the wiki, every answer other than "nothing" goes under "For
  other skills".

Wait for the answers. Ask another round when the answers open new questions.
When nothing that changes the output is left undecided, go to the Intent gate:
one approval, after the rounds.

**A change another skill owns.** When an answer needs a wiki change, do not
make it. List it under "For other skills" in the Run plan and in the summary.
When your work depends on it, stop before the Intent gate and name the skill
to run first.

The first round names the Task, its parent and the code folder, and puts to the
person:

- the branch name and the worktree path (section 3);
- where each scope item goes in the code, when the code allows more than one
  place, with your recommendation and the file paths it rests on;
- a scope item that is not in this folder: it belongs to another repository,
  and is listed, not built;
- a blocker that is not `Done`;
- with a subtask: the part it covers, when the person did not say it, asked
  with the Task's acceptance items and planned scope items to choose from and
  no recommendation; and the commits of earlier subtasks on the branch;
- the wiki question. This skill never writes the wiki, so every answer but
  "nothing" goes under "For other skills".

Do not ask what the Task, a Design file or `conventions.md` already settles.

**Intent gate.** Restate the Task, the code folder, the branch name and the
worktree path, and what will not be built here. With a subtask, also restate
its key, the part it covers, and what is left for other subtasks. Ask for
approval.

## 3. The worktree and the Run plan

| Name | Value |
|---|---|
| `NAME` | The Task key without `TASK-`: `coupon-api` |
| The branch | `task/<NAME>`, unless `conventions.md` says how branches are named; then that rule. Every subtask of the Task uses this branch |
| The worktree | `<code folder>/.worktrees/<NAME>/` |
| The Run plan | `plan.md` at the root of the worktree; `sdlc-plan.md` when the repository tracks a `plan.md` of its own there |

Read `references/write-protocol.md` now. Add the worktree as its section 2
says, and write the Run plan as its section 4 says. For code the Run plan is
the design, so nothing else is shown at the Design gate.

## 4. Design gate

Show the Run plan in full. Ask for approval. On rejection, follow
`write-protocol.md` section 3, "At section 4".

## 5. Write

Read `references/code-checks.md` now: the self review checks the code against
it.

In the worktree, write the code and its unit tests as `conventions.md`
requires, ticking each file in the Run plan. Match the code around it: its
layout, its names, its way of testing.

Never run the tests, the build or the code. Whether they pass is the
pipeline's and the reviewer's to say, and the wiki records no test result.

Write no runnable test for a TestCase of the wiki, and touch no TestSuite:
unit tests only.

**When the design is wrong.** The code cannot meet a Design file's contract,
or needs a contract the wiki does not have. Stop at that point; never code
past a contract that differs from the Design file. Show the difference with
the code location and the wiki path, and name the remedy:

- the design should change: a ChangeRequest with `sdlc-write-spec`;
- the wiki is wrong about code that exists: a correction with `sdlc-import`
  on this folder.

The person may tell you to go on without that part. Then leave it out, move
its line to `## Not built here`, and list it in the summary under "Not done"
and "For other skills".

## 6. Self review and the Change-set gate

Follow `write-protocol.md` section 3, "At section 6", with the self review of
its section 5. The commit message follows `conventions.md` and ends with the
trailer, after an empty line:

```text
Add the apply-coupon endpoint

Task: TASK-coupon-api
```

With a subtask, the message ends with two lines, the subtask first:

```text
Add the coupons table

Subtask: SCRUM-175
Task: TASK-coupon-api
```

## 7. Summary

"Done" names the branch and the worktree and says the commit is not pushed.
"Next" says: push the branch, open the pull request, have it reviewed
(`sdlc-review-code` checks it against the wiki), merge it, then close the
Task with `sdlc-close-task`.

End the run with at most four lines:

```text
Done: task/coupon-api in ../orders-svc/.worktrees/coupon-api, 1 commit, not pushed.
Not done: the coupon field of WEB-storefront (not in this folder)
For other skills: REQ-coupons-expiry is ambiguous (sdlc-write-spec)
Next: push, open the pull request, review, merge; then sdlc-close-task.
```

Leave out "Not done" and "For other skills" when they have nothing to say. Do
not list what the self review fixed, and do not repeat the Run plan.

With a subtask, "Done" names the subtask and the commits of earlier subtasks
kept on the branch; what is left for other subtasks is not "Not done". "Next"
says: build the next subtask the same way; push and open the pull request when
the commits are to be reviewed, one by one (`sdlc-review-code` reviews one
commit); merge without squashing; then `sdlc-close-task`.

## 8. What this skill never does

- It never writes to the wiki, and never changes a Task's status.
- It never touches a TestCase or a TestSuite.
- It never runs tests, the build or the code.
- It never pushes, opens a pull request, or calls a hosting service or a
  Tracker.
- It never changes the person's checkout, the repository's `.gitignore`, or
  a file named `plan.md` that the repository tracks.

## Done when

- The Task, the code folder, the branch and the worktree were approved at the
  Intent gate, and the Run plan at the Design gate.
- Every file of the Run plan is written, or is listed as not built with its
  reason.
- The checks of `code-checks.md` were made by reading, and what they could
  not settle was shown at the Change-set gate.
- This run added one commit to the branch, ending with `Task: <Task key>`,
  and with a subtask `Subtask: <subtask key>` on the line before it; the
  commits of earlier subtasks are unchanged; the Run plan file is not in the
  commit; nothing was pushed.
- Nothing in the wiki changed.
