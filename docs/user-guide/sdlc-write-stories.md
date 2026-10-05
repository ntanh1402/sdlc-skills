# sdlc-write-stories

Break the approved Requirements of a Feature or ChangeRequest into user
stories. [Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | Business analyst, product owner |
| **Use when** | You want the Requirements as user stories ("As a …, I want …, so that …") with acceptance criteria, or want existing stories regrouped. Stories are optional |
| **Needs first** | The spec pull request is merged (`ReqApproved` or later). It runs **at the same time** as [sdlc-design-arch](sdlc-design-arch.md); neither waits for the other |
| **Say** | "Break gift cards into user stories", "Write the user stories for CR-sms-notifications" |
| **You get** | `STORY-…` files, one actor's goal each, with Given/When/Then criteria that cite the Requirements. Every Functional Requirement (that is not **Wont**) is in a story. At the end, each story is printed ready to paste into a ticket. Draft branch `wiki/stories-<Key>` |
| **Next** | Merge the stories pull request and create the tickets. After the design is merged, [sdlc-plan-tasks](sdlc-plan-tasks.md) links each Task to its stories. If Tasks are already planned, run it again to link them |

A story groups Requirements; it never adds behaviour. The Requirements stay the
testable unit.

## What the skill does

1. Checks the target's state (see the table below) and refuses unless it is ready.
2. Builds an inventory of the Requirements (each marked *needs a story* or
   *optional*) and the actors and goals the PRD names.
3. Asks the first round. It proposes the stories (key, actor, goal, the
   Requirements each lists) and asks only your choices: where one goal is cut
   into two stories, which actor when the PRD names several, each story's
   priority, and for a ChangeRequest which Feature stories it affects.
4. **Intent gate**, then writes each story in full.
5. **Design gate:** shows every story as it will be written, the coverage
   matrix (each Requirement to its stories), and the Run plan.
6. Writes the files, checks coverage, **Change-set gate**, commit, and prints
   the paste-ready copy of every story added or changed.

## What you do

- Say which Feature or ChangeRequest.
- Decide the cuts, the actor and the priority where the skill asks.
- Read every story at the Design gate.
- Merge the pull request, then paste each story into your tracker. To record the
  ticket link in the wiki, ask [sdlc-edit-wiki](sdlc-edit-wiki.md).

## Scenarios

| What happens | What the skill does | What you do |
|---|---|---|
| **The Feature is `ReqApproved`, `Approved` or `InDev`** (or a ChangeRequest `ReqApproved` or `Approved`) | Goes on | Answer the rounds |
| **The requirements are still `Draft` or `Proposed`** | Refuses and routes to [sdlc-write-spec](sdlc-write-spec.md) | Approve the requirements first |
| **The spec is in a draft that is not merged** | Refuses and names the draft | Merge it |
| **The Feature is `Released` or `Deprecated`, or the ChangeRequest `Implemented` or `Rejected`** | Refuses. A change to a Released Feature is a ChangeRequest | Run [sdlc-write-spec](sdlc-write-spec.md) |
| **Every Requirement is already in a story** and you ask for no change | Reports the stories and stops | Nothing |
| **You already have stories** written in a brief | Takes them as given, with your wording. It only proposes the tracing to Requirements and reports what they leave uncovered | Check the tracing |
| **You want a criterion that no Requirement supports** | Does not write it. It names the gap for [sdlc-write-spec](sdlc-write-spec.md). If the stories cannot be written without it, it stops before the Intent gate | Add the Requirement, then run again |
| **A ChangeRequest** | Writes ChangeRequest stories with an `# Affects` section pointing at the Feature stories the change touches. Reads those Feature stories first | Confirm which stories are affected |
| **You revise existing stories** | Keeps each story's key. Deletes a story whose Requirements were all removed, says why in the log, and drops the links to it from Tasks and other stories | Check the deletions |
| **The design merges while the stories draft is open** | Checks the Requirements of the shared file. If they are unchanged it goes on. If they changed it shows what changed and goes back to the Design gate | Re-approve |
| **A story would cover two goals, or is too big** | Splits it by the story rules and shows the split | Decide where to cut |
| **Tasks already exist** | Writes the stories but does not touch the Tasks | Run [sdlc-plan-tasks](sdlc-plan-tasks.md) again to link them |
| **You want tickets created in the tracker** | No skill does it. It prints a paste-ready copy of each story | Create the tickets and paste |
| **You want the paste-ready copy again later** | Not this skill | Ask [sdlc-ask-wiki](sdlc-ask-wiki.md) |
| **A run stops part-way** | Next time it resumes from the draft | Confirm the plan still stands |

## Not this skill

| Request | Use |
|---|---|
| New or changed Requirements | [sdlc-write-spec](sdlc-write-spec.md) |
| Architecture | [sdlc-design-arch](sdlc-design-arch.md) |
| Tasks, or linking Tasks to stories | [sdlc-plan-tasks](sdlc-plan-tasks.md) |
| Test cases (they link Requirements, never stories) | [sdlc-design-tests](sdlc-design-tests.md) |
| Show a story, or its paste-ready copy again | [sdlc-ask-wiki](sdlc-ask-wiki.md) |
| A typo in a story, or a ticket link | [sdlc-edit-wiki](sdlc-edit-wiki.md) |
