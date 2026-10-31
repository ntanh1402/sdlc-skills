# Tasks may close before their spec is approved, and an approved spec has no outdated Task

ADR 0005 says the wiki changes for a Task only once, when `sdlc-close-task` records the merge, and `sdlc-close-task` used to wait until the parent Feature or ChangeRequest was `Approved`. Since spec versions let Tasks be planned and built from a draft spec, the owner decided on 2026-10-30 that a Task may also be closed while its parent is `Draft`, `Proposed` or `ReqApproved`. Closing it then changes only the Task; the parent's status and the Design files' pending entries stay until `sdlc-design-arch` approves the parent. On 2026-10-31 the owner added the rule that keeps this consistent: an approved parent never has an outdated Task. `sdlc-design-arch` refuses to approve a target while any of its Tasks is outdated, and the tool reports one as `basis.approved-task`.

This amends ADR 0005: a `Done` Task's file may change after the merge, but only in the ways `task.md` lists.

## Considered Options

- **Approve anyway, keep the affected pending entries, and replan later.** The first time `sdlc-plan-tasks` or `sdlc-edit-wiki` updated a `Done` Task's `basedOn` under an approved parent, the pending entries that Task covered would become `pending.leftover`, and no skill may edit Design files at that step.
- **Let `sdlc-plan-tasks` and `sdlc-edit-wiki` remove pending entries when they update `basedOn`.** The cleanup of pending entries would then live in four skills instead of two, and two narrow skills would gain Design-file edits.
- **Remove pending entries without checking the Task's version.** An entry would be removed before the changed design is built.

## Consequences

- A `Done` Task changes after the merge only in three ways: its `# Stories` and `# References` links; its `basedOn`, once checked against a newer version of a parent that is not approved yet; and a removed Requirement's anchor in `# Acceptance`, unlinked to plain text.
- Requirements change only before approval, so updating a `basedOn` always happens while the parent is unapproved, where pending entries are never reported. Pending entries are removed by exactly two skills: `sdlc-close-task` when code merges, and `sdlc-design-arch` when it approves a parent whose Tasks are already `Done`.
- A team that builds before the spec is agreed pays one `sdlc-plan-tasks` run before approval, so every Task can be brought to the current version.
- `pending.approved_parents` in `schema.json` names the approved statuses (`Approved`, a Feature `InDev`) for both `basis.approved-task` and the pending rules.
