# sdlc-plan-tasks

Plan the build Tasks of an approved design. [Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | Tech lead |
| **Use when** | An `Approved` design needs build Tasks; a changed design needs its Tasks planned again; or stories were written afterwards and the Tasks must link them |
| **Needs first** | The design pull request is merged. It may run at the same time as [sdlc-design-tests](sdlc-design-tests.md) |
| **Say** | "Plan the tasks for gift cards" |
| **You get** | `TASK-…` files, each with its acceptance, planned scope, size, dependencies and parallel wave. Every design item that is added, changed or removed is covered by exactly one Task, and every user story is linked by at least one Task. Draft branch `wiki/tasks-<Key>` |
| **Next** | Merge the pull request, then create a ticket per Task in your tracker. To record the ticket link in the Task, ask [sdlc-edit-wiki](sdlc-edit-wiki.md). The summary names the first wave of Tasks that can start |

## What the skill does

1. Checks readiness (see the scenarios) and runs the wiki's coverage check.
2. Builds the **scope inventory**: every concept the design adds, changes or
   removes, plus the migration, compatibility, security, observability, rollout
   and clean-up duties the design names, and lists the stories beside it.
3. Asks the first round: where the slices are cut, which repository each
   concept is built in when the wiki does not say, the order when two are
   possible, what a spike must answer, and which `Todo` Tasks have started.
4. **Intent gate** (planning basis).
5. Prepares the **task plan** in dependency order: key, title, type
   (`dev`, `design`, `spike`), size (XS to L), repository, planned scope,
   stories, acceptance, blockers, confidence. Then the coverage matrix and the
   parallel waves.
6. **Design gate:** shows the whole plan.
7. Writes the Task files, checks that nothing is left uncovered, **Change-set
   gate**, commit.

Rules the plan follows: vertical slices that can be reviewed and demonstrated
one by one; foundations, contracts and migrations before their consumers; risky
spikes first; no XL Task (it is split); each design concept belongs to exactly
one Task; no dependency cycles; every acceptance item is an observable result.

## What you do

- Say which Feature or ChangeRequest.
- Decide the cuts and the order, name the repository when the wiki does not,
  and say which Tasks have started.
- Read the whole plan at the Design gate.
- Merge, then create the tickets in your tracker.

## Scenarios

| What happens | What the skill does | What you do |
|---|---|---|
| **The design is `Approved`** (or an `InDev` Feature) and something is uncovered | Goes on | Answer the rounds |
| **The design is not approved** (`Draft`, `Proposed`, `ReqApproved`) | Refuses and routes to [sdlc-design-arch](sdlc-design-arch.md) | Design first |
| **The design is in an unmerged draft** | Refuses and names the draft | Merge it |
| **The Feature is `Released` or `Deprecated`, or the ChangeRequest `Implemented` or `Rejected`** | Says it is closed. A change to a Released Feature goes through a ChangeRequest | Run [sdlc-write-spec](sdlc-write-spec.md) |
| **Everything is already covered and the Tasks match the design** | Reports the existing plan and stops | Nothing |
| **The design changed after Tasks were planned** | Replans: keeps each Task's key, changes `Todo` Tasks that have not started to match | Tell it which have started |
| **A `Todo` Task has started and the design changed under it** | Treats it like a `Done` one: never rewrites it. Adds a new Task for the difference and says so at the Design gate | Approve |
| **A Task is `Done`** | Never rewrites it | Nothing |
| **Work spans two repositories** | Plans two Tasks, one blocked by the other when the order matters. A Task changes one repository | Name the repository of each if the wiki does not |
| **A slice is too big** (XL) | Splits it | Review the split |
| **The unknown is big** | Plans a `spike` first, with what it must answer | Decide what the spike must answer |
| **Stories do not exist yet** | Does not wait. If a stories draft is open it says so | Run this skill again after the stories merge |
| **Stories exist** | Links each Task to the stories its acceptance serves, from its own folder. Migration, spike or non-functional Tasks have no stories | Check the links |
| **The only work is linking stories** | Plans no new Task. Adding or dropping a story link is allowed even on `Done` and started Tasks (traceability, not scope) | Approve |
| **Planning finds a gap in the design** | Does not fix it. Lists it for [sdlc-write-spec](sdlc-write-spec.md) (ChangeRequest) or [sdlc-import](sdlc-import.md) (correction) | Run that skill |
| **You ask for tickets in the tracker** | No skill does it | Create the tickets by hand |
| **You want the ticket link in the Task** | Not this skill | Ask [sdlc-edit-wiki](sdlc-edit-wiki.md) |
| **Tests and tasks drafts conflict at merge** | Not a skill job | Merge one, ask your agent to run the tool's `refresh` on the other draft, then merge it |

## Not this skill

| Request | Use |
|---|---|
| No approved design yet | [sdlc-design-arch](sdlc-design-arch.md) |
| Test cases or suites | [sdlc-design-tests](sdlc-design-tests.md) |
| User stories | [sdlc-write-stories](sdlc-write-stories.md) |
| Writing a Task's code | [sdlc-build-task](sdlc-build-task.md) |
| Marking a Task `Done` | [sdlc-close-task](sdlc-close-task.md) |
| Explaining existing Tasks | [sdlc-ask-wiki](sdlc-ask-wiki.md) |
