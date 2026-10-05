# ChangeRequest

[Common rules](schema.md) · [Example](../sample/shop/change-requests/CR-sms-notifications/overview.md)

A requested change to exactly one existing Feature: new behavior, a fix, a refactor, a security or performance change.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `ChangeRequest` |
| Phase | Plan |
| Path | `<app>/change-requests/CR-<name>/` |
| Shape | Folder with `index.md`, `overview.md`, `log.md` |
| Status | `Proposed`, `ReqApproved`, `Approved`, `Implemented`, `Rejected` |
| Owns | Reference, UserStory, Task |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `ChangeRequest` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Proposed`, `ReqApproved`, `Approved`, `Implemented`, `Rejected` |
| `changeType` | yes | `feature`, `bugfix`, `refactor`, `security`, `perf` |
| `riskLevel` | yes | `low`, `med`, `high`, `critical` |
| `priority` | no | `P0`, `P1`, `P2`, `P3` |
| `targetRelease` | no | text |
| `requestedBy` | no | text |
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
| `# Changes` | required | author | Feature (exactly 1) |  |  |
| `# Reason` | required | author |  |  |  |
| `# Requirements` | required | author |  |  | any number of `### REQ-*` entries |
| `# Delta` | required; may be `None` | author |  |  | `None` only while status is `Proposed` or `ReqApproved` or `Rejected` |
| `## Target delta` | required | author | any Design type (1 or more) | `new`, `modified`, `removed` (required) |  |
| `## Runtime sequences` | required | author |  |  | Mermaid `sequenceDiagram` diagram |
| `## Decisions` | required | author | ArchitectureDecision (any number) |  |  |
| `## Traceability` | required | author |  |  |  |
<!-- generated:schema end -->

## Rules

- `# Reason` states why the change is wanted, in prose.
- `# Requirements` holds the Requirements this request adds or changes, in the
  Feature's format. A changed Requirement reuses the Feature's key; a new one
  gets a new name. A removed Requirement is described in the source
  document, not rewritten as a new positive Requirement.
- The Feature's copy of a Requirement is the current text. This request's copy
  records what was asked for and is not updated afterwards.
- Status is `Proposed` while the request is written, and `ReqApproved` once its
  Requirements are approved for design. Only a `ReqApproved` request is
  designed. A `Proposed` or `ReqApproved` request may be edited; editing a
  `ReqApproved` one sets it back to `Proposed`. An `Approved` request is not
  edited; a further change is another request.
- Before design approval, `# Delta` is `None — pending architecture`.
- When the design is approved, in one change: `# Delta` gets its four sections,
  status becomes `Approved`, the Feature's Requirements and Architecture are
  updated to the new target, every concept in `## Target delta` is rewritten to
  the target and gets a pending entry, and decisions are recorded.
- `## Target delta` lists every Design concept this request creates, changes, or
  removes, each qualified `new`, `modified`, or `removed`.
- Status becomes `Implemented` when every Task is `Done` and no pending entry
  names this request.
- Tasks and user stories for this request are files in this folder, never
  in the Feature's.
