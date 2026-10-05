# Feature

[Common rules](schema.md) · [Example](../sample/shop/features/FEAT-checkout/overview.md)

A capability a user or the business can recognise, with its requirements and approved target architecture.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `Feature` |
| Phase | Plan |
| Path | `<app>/features/FEAT-<slug>/` |
| Shape | Folder with `index.md`, `overview.md`, `log.md` |
| Status | `Draft`, `ReqApproved`, `Approved`, `InDev`, `Released`, `Deprecated` |
| Owns | Reference, UserStory, Task |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `Feature` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Draft`, `ReqApproved`, `Approved`, `InDev`, `Released`, `Deprecated` |
| `ownerTeam` | yes | text |
| `priority` | no | `P0`, `P1`, `P2`, `P3` |
| `targetRelease` | no | text |
| `epicKey` | no | text |
| `flagKey` | no | text |
| `releasedAt` | no | ISO 8601 timestamp with offset |
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
| `# Requirements` | required | author |  |  | 1 or more `### REQ-*` entries |
| `# Architecture` | required; may be `None` | author |  |  | `None` only while status is `Draft` or `ReqApproved` |
| `## Context and constraints` | required | author |  |  |  |
| `## High-level architecture` | required | author |  |  | Mermaid `flowchart` diagram |
| `## Services` | required | author | Service (1 or more) |  |  |
| `## Frontends` | optional | author | WebFrontend, MobileFrontend (1 or more) |  |  |
| `## Runtime sequences` | required | author |  |  | Mermaid `sequenceDiagram` diagram |
| `## Decisions` | required | author | ArchitectureDecision (any number) |  |  |
| `## Traceability` | required | author |  |  |  |
| `# Change history` | always | tool | mirrors ChangeRequest `# Changes` |  |  |
<!-- generated:schema end -->

## Rules

- A Requirement is a `### REQ-<feature-name>-<name>` entry, where
  `<feature-name>` is the Feature key without `FEAT-` and `<name>` is
  lower-case words joined by `-` (`REQ-cart-edit-items`). It states, exactly once each:
  a MoSCoW priority in bold (`**Must**`, `**Should**`, `**Could**`, `**Wont**`),
  the requirement text, a type (`Functional.`, `Nonfunctional.`, or
  `Constraint.`), and a verification method (`Verified by test.`, `inspection.`,
  or `demo.`).
- One Requirement is one independently testable behavior or constraint. It does
  not prescribe architecture.
- Requirement keys are never reused for a different Requirement. A
  ChangeRequest that adds a Requirement gives it a name that neither the Feature
  nor another open ChangeRequest on it uses (`ids.requirement-collision`).
- `# Architecture` is the approved target, not the deployed state. Design
  concept statuses and their `# Pending changes` sections show what is not built.
- `## High-level architecture` shows every concept named in `## Services` and
  `## Frontends`. `## Runtime sequences` covers each Requirement's main flow and
  its failure branches. `## Traceability` maps every Requirement to the Design
  concepts that satisfy it.
- `## Frontends` appears only when the Feature has a user interface.
- Status is `Draft` while the Requirements are written, `ReqApproved` once they
  are approved for design, and `Approved` once the Architecture is approved.
  `# Architecture` is `None` only while `Draft` or `ReqApproved`. Editing a
  `ReqApproved` Feature sets it back to `Draft`. From `Approved` on, the
  Requirements change only through a ChangeRequest or, once `Released`, a
  [correction](schema.md#corrections).
- A new Draft Feature has at least one Requirement.
- Source documents are listed in `sources`. A local one is a
  [Reference](source-document.md) file in this folder.
- Tasks for the Feature's first build are files in this folder.
