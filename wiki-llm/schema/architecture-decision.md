# ArchitectureDecision

[Common rules](schema.md) · [Example](../sample/shop/decisions/ADR-idempotent-checkout.md)

One material, hard-to-reverse design choice. All decisions of an application share one folder.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `ArchitectureDecision` |
| Phase | Design |
| Path | `<app>/decisions/ADR-<name>.md` |
| Shape | One file |
| Status | `Proposed`, `Accepted`, `Rejected`, `Superseded` |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `ArchitectureDecision` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Proposed`, `Accepted`, `Rejected`, `Superseded` |
| `ownerTeam` | yes | text |
| `decisionDate` | no | `YYYY-MM-DD` |
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
| `# Context` | required | author |  |  |  |
| `# Decision` | required | author |  |  |  |
| `# Alternatives` | required | author |  |  |  |
| `# Consequences` | required | author |  |  |  |
| `# Affected concepts` | required | author | any Design type, Feature, ChangeRequest (1 or more) |  |  |
| `# Supersedes` | optional | author | ArchitectureDecision (1 or more) |  |  |
| `# Superseded by` | when not empty | tool | mirrors ArchitectureDecision `# Supersedes` |  |  |
<!-- generated:schema end -->

## Rules

- Record a decision only when a credible alternative existed. Routine
  implementation detail belongs in the Design concept.
- `# Context` states the forces and constraints. `# Decision` states the choice
  and why. `# Alternatives` lists what was rejected and why. `# Consequences`
  covers benefits, costs, risks, and follow-up obligations.
- `# Affected concepts` links every Feature, ChangeRequest, or Design concept
  whose target changes because of this decision.
- The Feature or ChangeRequest that produced the decision links it under
  `## Decisions`. A decision for the whole application needs no such link.
- To replace a decision, write a new one with `# Supersedes` linking the old one,
  and set the old one's status to `Superseded`. Do not edit the old decision's
  content.
