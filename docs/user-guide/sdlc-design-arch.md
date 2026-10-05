# sdlc-design-arch

Design the target architecture of a Feature or ChangeRequest whose requirements
are approved. [Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | Architect |
| **Use when** | A Feature or ChangeRequest is `ReqApproved` and needs a technical design: the services, frontends, endpoints, events, data and externals it needs, their contracts, diagrams, and the decisions behind them |
| **Needs first** | The spec pull request is merged |
| **Say** | "Design the gift cards feature" |
| **You get** | The Architecture section (a ChangeRequest: the Delta), Mermaid diagrams, new or changed services, endpoints, events, tables and externals marked as **pending**, decisions (`ADR-…`), traceability from each Requirement, and status `Approved`. Draft branch `wiki/arch-<Key>` |
| **Next** | Merge the design pull request, then [sdlc-plan-tasks](sdlc-plan-tasks.md) and [sdlc-design-tests](sdlc-design-tests.md), in either order or both at once |

## What the skill does

1. Checks readiness and reads what exists: the PRD, every Requirement, accepted
   decisions, and every design item the requirements touch (and, when
   available, the linked contracts of existing components).
2. Asks the first round with its recommendation for each choice that is yours:
   what is reused and what is new, how the parts talk, who owns new data, which
   choices become decisions. It also asks the **downstream freshness**
   question: which existing `Todo` Tasks have already been started.
3. **Intent gate** (design basis): the target, the systems reused or added, the
   decisions expected, drift found, and the Tasks or TestSuites the design will
   make out of date.
4. Prepares the **design packet**: context, a ledger of every concept (new,
   modified, removed or reused, with the reason), the high-level diagram, a
   sequence diagram per main flow with its failure branches, the contract of
   every new or changed concept, decisions with alternatives, traceability,
   drift/risks/rollout/rollback, and downstream freshness.
5. **Design gate:** shows the full packet and the Run plan.
6. Writes the files. New concepts are written as the full target with status
   `Planned`; changed ones as the target with `Modifying`; removed ones as
   `Removing` (the file stays). Each gets a pending entry, which stays until its
   Task is closed.
7. Self review, **Change-set gate**, commit.

## What you do

- Name the Feature or ChangeRequest (or accept the `ReqApproved` candidate the
  skill proposes).
- Decide the design choices and say which `Todo` Tasks have started.
- Read the full packet at the Design gate. Any edit reopens the gate.
- Merge the pull request.

## Scenarios

| What happens | What the skill does | What you do |
|---|---|---|
| **The requirements are `ReqApproved`** and the architecture is `None` | Goes on | Answer the rounds |
| **The requirements are `Draft` or `Proposed`** | Refuses: "ask its author to approve them with sdlc-write-spec" | Approve the requirements |
| **The spec is in an unmerged draft** | Refuses and names the draft | Merge it |
| **The Feature is already `Approved` or later** | Refuses: a change to the design is a new ChangeRequest | Run [sdlc-write-spec](sdlc-write-spec.md) |
| **You did not name a key and several are `ReqApproved`** | One question that names the candidates | Pick one |
| **The requirements contradict an accepted decision or a live contract** | Shows both sides with paths in the first round and asks how to proceed | Decide: change the requirement, supersede the decision, or accept the contract |
| **The wiki and the code disagree** (drift) | Classifies the difference. If it is material, stops before the Intent gate, shows both sides and asks which is true | Decide which is true. A correction of the wiki is [sdlc-import](sdlc-import.md); a change of design is a ChangeRequest |
| **An existing service could serve the need** | Reuses it, unless a different ownership or lifecycle boundary is proven. It never copies a concept to avoid changing it | Challenge the recommendation if you disagree |
| **A material, hard-to-reverse choice with a credible alternative** | Writes an architecture decision (`ADR-…`, `Accepted`) with its alternatives. Reuses an accepted decision that already covers it. A decision is replaced only by a new decision | Approve |
| **A Requirement has a user interface** | Names which web or mobile frontend owns each screen. It never invents a frontend | Confirm |
| **Tasks or TestSuites already exist** | Lists the ones the design makes out of date under "For other skills". It never edits them | Run [sdlc-plan-tasks](sdlc-plan-tasks.md) and [sdlc-design-tests](sdlc-design-tests.md) after the merge |
| **A `Todo` Task has already been started** | Asks you to acknowledge each started Task separately. The wiki cannot know | Tell it which Tasks started |
| **A ChangeRequest** | Fills its Delta and, in the **same** change, updates the target Feature's Requirements and Architecture to the new target | Check both |
| **The design removes a Requirement** that user stories or TestCases list | Fixes those stories and cases in the same draft and shows the edits at the Design gate | Check the edits |
| **A changed Requirement keeps its key** | Leaves its stories as they are | Nothing |
| **Requirements are missing or unclear** | Does not invent them. Routes to [sdlc-write-spec](sdlc-write-spec.md) | Fix the requirements first |
| **"Design this" could mean several things** | Asks one routing question | Say which |
| **Stories are being written at the same time** | No conflict. The stories skill checks the shared file before it commits | Merge both |
| **A run stops part-way** | The next run resumes from the file that holds the diagrams and decisions | Confirm the plan still stands |
| **You only want to see an existing architecture** | Routes to [sdlc-ask-wiki](sdlc-ask-wiki.md) | Ask there |

## Not this skill

| Request | Use |
|---|---|
| Show or explain an existing architecture | [sdlc-ask-wiki](sdlc-ask-wiki.md) |
| Requirements missing, unclear or not approved | [sdlc-write-spec](sdlc-write-spec.md) |
| User stories | [sdlc-write-stories](sdlc-write-stories.md) |
| Build tasks or test design | [sdlc-plan-tasks](sdlc-plan-tasks.md), [sdlc-design-tests](sdlc-design-tests.md) |
