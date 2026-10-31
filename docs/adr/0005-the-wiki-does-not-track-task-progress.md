# The wiki does not track Task progress, and no skill talks to the Tracker

> Amended by [ADR 0006](0006-tasks-close-before-approval.md): a `Done` Task's file may still change after the merge, but only in the ways `task.md` lists.

Schema v2 gave a Task the statuses `Todo`, `InProgress`, `InReview` and `Done` and the fields `assignee`, `sprint`, `branch`, `prNumber`, `prStatus` and `ciStatus`, for a tracker-sync skill to fill from the Tracker and the hosting service. On 2026-10-03 the owner decided that people create a Task's ticket in the Tracker by hand and follow its progress there. The wiki records only that a Task is planned (`Todo`) and that its code is merged (`Done`), and it changes for a Task only once, when `sdlc-close-task` records the merge. The four progress statuses become two and the six fields are removed.

## Considered Options

- **A skill syncs the Tracker into the wiki.** Every status change of every ticket would need a Draft and a pull request, the skills would need credentials for a hosting service and a Tracker that differ per project, and the wiki would repeat what the Tracker already shows.
- **Keep the statuses and fields for people to fill by hand.** A field nobody updates ends up stating progress that is no longer true, and skills that read `InProgress` would act on it.

## Consequences

- `trackerKey`, `resource` and `prUrl` stay optional on a Task for a person to fill in; no skill asks for them.
- `mergedAt` and `mergeCommitSha` stay and are written by `sdlc-close-task`, which finds the merged code with git alone.
- The wiki cannot tell whether a `Todo` Task has started. `sdlc-plan-tasks` and `sdlc-design-arch` ask the person where they used to read `InProgress`.
- A skill's own progress within one run is kept in its Run plan, a file that is never committed, for the same reason: the Bundle holds what is agreed and built, not who is working on what.
- No skill sets a Feature `Released`: merged code is not deployed code. A person sets it with `sdlc-edit-wiki`.
