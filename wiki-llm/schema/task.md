# Task

[Common rules](schema.md)

One unit of build work. It lives in the folder of the Feature or ChangeRequest that caused it.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `Task` |
| Phase | Build |
| Path | `<app>/features/FEAT-*/TASK-<name>.md or <app>/change-requests/CR-*/TASK-<name>.md` |
| Shape | One file |
| Status | `Todo`, `Done` |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `Task` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Todo`, `Done` |
| `basedOn` | yes | `{ version, at }`: a spec version and its `YYYY-MM-DD` |
| `trackerKey` | no | text |
| `taskType` | no | `dev`, `test`, `design`, `spike` |
| `estimate` | no | text |
| `priority` | no | `P0`, `P1`, `P2`, `P3` |
| `prUrl` | no | URL or bundle path |
| `mergedAt` | no | ISO 8601 timestamp with offset |
| `mergeCommitSha` | no | text |
| `generated` | yes | `{ by, at }` |
| `verified` | no | `{ by, at }`, or a list of them |
| `sources` | no | list of `{ id, resource, title }` |
| `resource` | no | URL or bundle path |
| `stale_after` | no | ISO 8601 timestamp with offset |
| `tags` | no | `[a, b]` |

### Headings

| Heading | Presence | Written by | Links to | Qualifier | Content |
|---|---|---|---|---|---|
| `# <title>` | required; first heading | author |  |  |  |
| `# Acceptance` | required | author |  |  |  |
| `# Stories` | optional | author | UserStory (any number) |  |  |
| `# Planned scope` | required | author | any Design type (any number) | `new`, `modified`, `removed` (required) |  |
| `# Blocked by` | optional | author | Task (any number) |  |  |
| `# Reviewers` | optional | author |  |  |  |
| `# References` | optional | author | Reference (any number) |  |  |
<!-- generated:schema end -->

## Rules

- A Task has exactly one parent: the folder it is in. Work caused by a
  ChangeRequest goes in the ChangeRequest folder.
- `# Acceptance` states observable results and links the Requirements it
  satisfies. Do not repeat the title.
- `# Stories` links the user stories this Task serves, in its own folder. A
  Task with no story (a migration, a spike, a Task for a Nonfunctional
  Requirement) has none. A link may be added to a `Done` Task: it is
  traceability, not scope.
- `# Planned scope` links every Design concept the Task will create, change, or
  remove, qualified `new`, `modified`, or `removed`, matching the parent's design.
- While the Task is not `Done`, or while its parent is not `Approved` yet
  (`Draft`, `Proposed`, `ReqApproved`), each concept in its scope carries a
  pending entry for the parent. Once the parent is `Approved` (or `InDev`) and
  every Task of the parent covering a concept is `Done` and current, the entry
  is removed.
- A Task changes one code repository. Work in two repositories is two Tasks.
- The status is `Todo` until the Task's code is merged, then `Done`. Progress
  in between is followed in the tracker, not here. `resource` is the tracker
  ticket URL and `trackerKey` its key; a person adds them, and no skill reads
  or writes the tracker.
- `mergedAt` and `mergeCommitSha` are written when the Task is closed. A
  person may add `prUrl`.
- `basedOn` is the version of the parent the Task was planned or confirmed
  from. A Task may be closed while its parent is still a draft or at a newer
  version; when the parent's version changes after a Task is built or closed, a
  new Task is planned for any difference and the earlier Task's `basedOn` is
  updated to the current version. An approved parent (`Approved`, a Feature
  `InDev`) has no outdated Task (`basis.approved-task`): its Tasks catch up
  with the current version before it is approved, since its Requirements do not
  change afterwards. See [Spec versions](schema.md#spec-versions).
- A `Done` Task records what was built, so after the merge it changes only in
  three ways: a `# Stories` or `# References` link added or dropped; its
  `basedOn` updated once it was checked against a newer version of a parent
  that is not approved yet; and, when a step removes a Requirement, that
  Requirement's anchor in `# Acceptance` unlinked to plain text, so the prose
  stays as built.
