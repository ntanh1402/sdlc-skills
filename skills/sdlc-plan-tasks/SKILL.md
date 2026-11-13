---
name: sdlc-plan-tasks
description: Plan the build Tasks of a designed Feature or ChangeRequest in the project wiki, while its requirements are a draft or once they are agreed - ordered, independently verifiable Tasks with planned scope, acceptance, size, dependencies and parallel waves, covering every concept its design adds, changes or removes, each Task serving at most one user story. Use when an architecture needs a task breakdown, implementation plan or backlog, when a design or spec changed and its Tasks must be replanned, or when user stories were written and the Tasks must link them. Not for requirements, architecture, test design, tracker sync or code.
---

# Plan the tasks

This skill is a lifecycle step after the design. It takes a Feature or
ChangeRequest whose design is merged, whether its Requirements are a draft or
agreed, and writes `TASK-<name>.md` files into its folder, so that every Design concept its
design adds, changes or removes is in the planned scope of at least one Task,
every user story in the folder is linked by at least one Task, and each Task
serves at most one story.

Its draft prefix is `tasks-`: the draft for `FEAT-coupons` is
`wiki/tasks-FEAT-coupons`. It may run at the same time as the test design skills
on the same design.

## Before you start

Read, in this skill's folder, `references/read-protocol.md`; each section names
the other `references/` files to read when it starts.

Find the wiki as the read protocol says, and check that it matches this
skill. `RELEASE`, next to this file, holds one line such as `1.0.0`:

```bash
cd "$WIKI" && $T copy check --release "<the line in RELEASE>"
```

| `status` | Do |
|---|---|
| `current` | Go on |
| `older` | Stop: "The wiki's tool is older than this skill. Run sdlc-setup-wiki to upgrade the wiki." |
| `newer` | Stop: "The wiki was set up by a newer release. Update your installed sdlc-skills." |
| `edited` | Stop: "The wiki's tool copy was edited by hand. Run sdlc-setup-wiki to restore it." |

Then read the schema pages `schema.md`, `task.md`,
`user-story.md`, `feature.md`, `change-request.md` and the page of each
Design type in scope,
in the wiki's `.wiki-llm/schema/`.

| Request | Skill |
|---|---|
| No approved design yet | `sdlc-design-arch` |
| Test cases or suites | `sdlc-design-story-tests`, `sdlc-design-feature-tests` |
| User stories | `sdlc-write-stories` |
| Create or update tickets in Jira or another tracker | No skill does: a person creates the ticket by hand and may add `trackerKey` and `resource` to the Task |
| Explain the existing Tasks | `sdlc-ask-wiki` (no gates, nothing written) |
| Write the code of a Task | `sdlc-build-task` |
| Mark a Task `Done` | `sdlc-close-task`, after its code is merged |
| Add a ticket link to a Task | `sdlc-edit-wiki` |

## The gates

A gate is a stop for the person's explicit approval. There are three, so the
person decides what is being done (Intent), how (Design), and exactly what is
saved (Change-set), each before the next cost is paid.

- Approval is an explicit yes to the gate's question. "Sounds good", silence
  or "whatever you think" is not approval.
- An edit at a gate reopens that gate and every later one.
- When you cannot ask the person (a run with no one to answer), or the person
  asks you to skip questions or approvals ("don't ask me, just write it"),
  stop before the first gate and start no draft. Return the open decisions
  and the gates the work still needs. Never assume approval.
- When the person rejects the design, stop. A draft worktree this run started
  is discarded; a worktree an earlier run started is left as it is.
- Being asked to run this skill does not approve anything it writes.
- A refusal this file states is a refusal. Do not turn it into a question.

## 1. Look up: readiness and the scope

Accept one `FEAT-*` or `CR-*` key. Read it on the default branch:

| State | When | Do |
|---|---|---|
| `READY` | A Feature `Draft`, `ReqApproved`, `Approved` or `InDev`, or a ChangeRequest `Proposed`, `ReqApproved` or `Approved`, whose `# Architecture` or `# Delta` is not `None`; and `coverage tasks` reports uncovered concepts or stories no Task links, the design changed under `Todo` Tasks, `outdated` lists a Task, or the person asks to replan | Go on |
| `NEEDS_DESIGN` | `# Architecture` or `# Delta` is `None` | Stop: route to `sdlc-design-arch` |
| `NOT_MERGED` | Not on the default branch, but a `wiki/*-<Key>` draft exists | Stop and name the draft |
| `CLOSED` | A Feature that is `Released` or `Deprecated`, or a ChangeRequest that is `Implemented` or `Rejected` | Stop: say it is closed; a change to a Released Feature goes through a ChangeRequest (`sdlc-write-spec`); route nowhere else |
| `ALREADY_CURRENT` | `coverage tasks` and `outdated` report nothing and every Task matches the design | Report the existing plan and stop |

```bash
$T coverage tasks --feature FEAT-coupons      # or --change CR-sms-alerts
$T outdated --feature FEAT-coupons            # Tasks planned from an older spec version
```

When `outdated` also lists the design itself (`designBasedOn` older than
`version`), say in the first round that the design is behind the spec and
recommend `sdlc-design-arch` first; go on only when the person says so. When
the Requirements are still a draft, say that the Tasks can be built and
closed while the spec is a draft, and if the Requirements change later, a new
Task will be planned for the difference.

Every state but `READY` is a refusal, not a question.

Then read the Requirements, the Feature's `# Architecture` or the
ChangeRequest's `# Delta`, the decisions it links, every Design concept in
scope with its `# Pending changes` entry, every existing Task in the folder,
every user story in the folder with the Requirements it lists, and the
References all of these link.

Stories are optional and may not exist yet. Do not wait for them: when a
`wiki/stories-<Key>` draft is open, say so in the first round, and say that
running this skill again after it merges links the stories.

Build the scope inventory: every concept in the design qualified `new`,
`modified` or `removed`, plus the migration, compatibility, security,
observability, rollout and clean-up duties the design and its decisions
name. A frontend route, screen or `# Calls` change is scope like any other.
List the folder's stories beside the inventory, each with its Requirements.

**An unfinished run.** Last, `ls "$WIKI"/.worktrees/*/plan.md 2>/dev/null`
lists the runs that stopped part-way. When one is for this request (its
folder is `tasks-<Key>`, or its plan's title names this request), read
`references/write-protocol.md` now and go on as its section 2 says, without
asking the rounds again.

## 2. Questions and the Intent gate

Read `references/decomposition-rules.md` and `references/task-sizing.md` now:
the choices of section 3 use them.

Ask in rounds. A round is a numbered list of every question that can be
answered now, each with your recommended answer. The person confirms or
corrects, which is faster than composing an answer, and sees your reasoning
before any work is done.

```text
Q1 - How should the coupon work be sliced across repositories?
     (services/SVC-orders/overview.md, frontends/WEB-storefront/overview.md)
     ➡️ Two Tasks: TASK-coupon-api in orders-service first, then TASK-coupon-ui in shop-web.
Q2 - What else in the wiki must change because of this?
     ➡️ Nothing: only Task files and the folder's log.
```

Which questions to ask, and how many, is your judgement. Three things are
fixed:

- **The format.** Numbered questions, each with a recommendation. A
  recommendation that rests on the wiki cites the path. A question whose
  answer depends on another question in the same round waits for the next
  round.
- **At least one round**, even when a brief seems complete. Its questions are
  then the assumptions you would otherwise make without saying so.
- **The wiki question.** Ask what else in the wiki must change because of
  this request, with your own answer as the recommendation.

Wait for the answers. Ask another round when the answers open new questions.
Search the wiki again whenever an answer brings a system, a term or a claim
about current behaviour you have not read.
When nothing that changes the output is left undecided, go to the Intent gate:
one approval, after the rounds.

**A change another skill owns.** When an answer needs a wiki change this skill
does not own (such as a gap in the architecture or a missing Reference), do
not make it. List it under "For other skills" in the Run plan and in the
summary. When your work depends on it, stop before the Intent gate and name
the skill to run first.

The first round names the target and its state, shows the scope inventory, and
puts to the person the choices of section 3 that are theirs: where the slices
are cut, which repository each concept is built in when the wiki does not say,
the order when two orders are possible, and what a spike must answer. It also
holds:

- **started Tasks**, when Tasks exist. The wiki does not know whether a
  `Todo` Task has started or its code is already merged: list the `Todo`
  Tasks the design or the new spec version changes and ask which have
  started, and which have merged code;
- the wiki question. The usual answer is "nothing: only Task files and the
  folder's log"; a gap in the design that the planning found is another
  skill's change (`sdlc-write-spec` for a ChangeRequest, `sdlc-import` for a
  correction).

**Intent gate.** Restate the target, the scope inventory, the existing Tasks
and what you expect to add or change. Ask for approval
(`PLANNING BASIS CONFIRMED`).

## 3. What goes into the plan

Follow `references/decomposition-rules.md` and `references/task-sizing.md`:

- Vertical, independently reviewable and demonstrable slices; foundations,
  contracts and migrations before their consumers; risky spikes first.
- `taskType`: `dev`, `design` or `spike`. `test` only implements a TestSuite
  that is already approved; test design is `sdlc-design-story-tests` and `sdlc-design-feature-tests`.
- Size XS to L. An XL Task is split.
- Each Task's `# Planned scope` links the concepts it builds, with the
  qualifier the design gave them. Each concept in the inventory is in the
  `# Planned scope` of at least one Task. When several stories change
  different parts of one concept, each of their Tasks lists it with a note
  naming its part. When several stories only use a concept (read or call it
  without changing it), a story owns it if its acceptance criteria are what
  the concept delivers; the owning story's Task builds it. When no story owns it, one
  foundation Task with no `# Stories` builds it. Either way, the other Tasks
  that use it are `# Blocked by` that Task (examples in
  `references/decomposition-rules.md`, "Stories and coverage"). When a
  `Done` or started Task built an earlier version of a concept and the
  design changed it, a new `Todo` Task takes the difference and both Tasks
  keep the concept in `# Planned scope`.
- `# Acceptance` states observable results and links the Requirements it
  satisfies by full path and anchor.
- `# Stories` links the one story the Task serves: the story whose
  acceptance criteria its `# Acceptance` delivers. A Task that serves no
  story (a foundation Task, a migration, a spike, a Nonfunctional
  Requirement) has no `# Stories`. Every story of the folder is linked by
  at least one Task. A Task links only stories of its own folder.
- `# Blocked by` links the Tasks it waits for; no cycles.
- `# References` links the References a developer needs for this Task: those
  the Feature or ChangeRequest and the Design files in its `# Planned scope`
  link, when they bear on its work, each with a note on what to take from
  it. Do not create a Reference; when one is missing, say which in the
  summary and name `sdlc-edit-wiki`.

**One repository.** A Task changes one code repository. Work that spans two
repositories is two Tasks, one blocked by the other when the order matters.

**Replanning.** Keep each existing Task's key. A `Done` Task is never
rewritten. A `Todo` Task that has not started may be changed to match the new
design. A `Done` Task, or a `Todo` Task the person said has started or whose
code is merged, is kept as built: if the design or the spec changed under it,
add a new Task for the difference, `# Blocked by` the old one, and say so at
the Design gate.

**Spec version.** Each Task's `basedOn` is
`{ version: <the parent's version>, at: <its versionDate> }`. Write it on
every new Task and on every Task you replan. A `Done`, started or merged Task
that got a Task for the difference also gets the current `basedOn`: together
they cover the new version. Its log entry says it was built from the older
version and names the new Task. A `Done` or `Todo` Task the new version does
not change gets the current `basedOn` too, once you have checked it against
the change.

**Story links on any Task.** Adding a `# Stories` link to a Task that has
none, or dropping one to a story that no longer exists, is allowed on every
Task, `Done` and started ones included: it is traceability, not scope, and it
is the only edit made to those, besides `# References`. A run whose only work
is linking stories plans no new Task.

## 4. Run plan and the Design gate

Read `references/write-protocol.md` and `references/task-format.md` now.

Start or resume the draft `tasks-<Key>` as `write-protocol.md` section 2 and
section 3, "At section 4", say. The input paths are the Feature's or
ChangeRequest's `overview.md` and, for a ChangeRequest, the target Feature's
`overview.md`.

Prepare the task plan: in dependency order, one row per Task with its key,
title, type, size, repository, planned scope, story, acceptance summary,
blockers and confidence; then the coverage matrix (each inventory row to the
Tasks that cover it, and each story to the Tasks that link it) and the
parallel waves (Tasks with no unfinished blocker start together).

Write the Run plan (`write-protocol.md` section 4). Its `## Files` are one line
per Task file, added or changed, with its planned scope in a few words, and the
folder's `log.md`.

**Design gate.** Show the task plan in full, never only a summary, then the
Run plan. Ask for approval (`TASK PLAN APPROVED`).

## 5. Write

In the draft worktree, in the Feature's or ChangeRequest's folder, write each
new Task as `TASK-<name>.md` with `references/task-format.md`, and edit the
`Todo` Tasks being replanned. Add an entry to the folder's `log.md`, for
example
`* **Tasks**: Planned 5 Tasks in 3 waves. Written by an AI model with sdlc-plan-tasks.`

Do not touch the Design concepts: their pending entries were written with the
design. Do not write `index.md`.

## 6. Self review, finish and commit

Follow `write-protocol.md` section 3, "At section 6", with the self review of
its section 5. In the self review, have the review sub-agent check by reading
that:

- each concept of the inventory is in the `# Planned scope` of at least one
  Task, and no Task is XL;
- each concept several stories need is either split into named parts
  across their Tasks, or built by one Task (the owning story's Task, or a
  foundation Task when no story owns it) that the other Tasks using it are
  `# Blocked by`; each `Todo` Task that shares a concept with another Task
  names its part in the note;
- each Task links at most one story, and every story is linked by a Task;
- every `# Acceptance` states an observable result and links its
  Requirements;
- no `Done` Task and no started Task was rewritten beyond what `task.md`
  allows on a `Done` Task (its `# Stories` and `# References` links and its
  `basedOn`; this skill never unlinks a Requirement), and no Design concept or
  user story was touched.

Then run `$T coverage tasks` (which must report nothing uncovered: no concept
without its Task and no user story without a Task) and `$T outdated` (no Task
of the folder listed) in the worktree.

Commit message: `tasks(<Key>): plan <n> tasks`. In the summary, "Next" names
the Tasks of the first wave: the ones that can start once the pull request
is merged. When the Requirements are still a draft, add that the Tasks can
be built and closed while the spec is a draft, and any later Requirement
change will add a new Task for the difference. When the parent is
`ReqApproved`, add that `sdlc-design-arch` can approve it once this pull
request is merged: an approved parent needs every Task at its current
version.

## The summary

End the run with at most four lines:

```text
Done: wiki/tasks-FEAT-coupons, 3 files, pushed. Open the pull request.
Not done: features/FEAT-coupons/TASK-coupon-export.md (export contract undecided)
For other skills: Missing Reference for coupon code format (sdlc-edit-wiki)
Next: Build wave 1 (TASK-coupon-api) with sdlc-build-task after the merge.
```

Leave out "Not done" and "For other skills" when they have nothing to say. Do
not list what the self review fixed, and do not repeat the task plan: the
person approved the content at the gates, so the last message only says where
it is and what comes next.

## Done when

- The target, the scope inventory and the started Tasks were confirmed in the
  rounds, and the planning basis was approved at the Intent gate.
- Every concept and duty in the scope inventory is covered by a Task, every
  user story of the folder is linked by a Task, and no Task links two stories.
- No XL Task, no dependency cycle, no part of a concept planned twice among
  unstarted `Todo` Tasks, no Task without observable acceptance.
- No `Done` or started Task was rewritten beyond what `task.md` allows on a
  `Done` Task.
- Every Task in the folder has the parent's current `basedOn`.
- The self review found nothing it could not fix, or the person accepted what
  was left at the Change-set gate.
- `coverage tasks` reports nothing, `draft finish` was `ok`, the change set was
  approved, and `draft commit` reported the branch.
