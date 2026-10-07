# Endpoint

[Common rules](schema.md) · [Example](../sample/shop/services/SVC-orders/EP-orders-create.md)

One synchronous operation a Service exposes.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `Endpoint` |
| Phase | Design |
| Path | `<app>/services/SVC-*/EP-<slug>.md` |
| Shape | One file |
| Status | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `Endpoint` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| `method` | yes | text |
| `path` | yes | text |
| `protocol` | yes | `http`, `grpc`, `graphql` |
| `authType` | no | lower-case words joined by `-`; common: `none`, `apikey`, `jwt`, `oauth` |
| `rateLimit` | no | text |
| `idempotent` | no | `true` or `false` |
| `version` | no | text |
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
| `# Request` | required | author |  |  |  |
| `# Response` | required | author |  |  |  |
| `## Status codes` | required | author |  |  |  |
| `# Validations` | required | author |  |  |  |
| `# Behavior` | required | author |  |  |  |
| `# Flowchart` | required | author |  |  | Mermaid `flowchart` diagram |
| `# Sequence diagram` | required | author |  |  | Mermaid `sequenceDiagram` diagram |
| `# References` | optional | author | Reference (any number) |  |  |
| `# Pending changes` | conditional | author | Feature, ChangeRequest (1 or more) | `new`, `modified`, `removed` (required) |  |
<!-- generated:schema end -->

## Rules

- `# Request` documents every field in a `Field | Location | Type | Required |
  Description` table. `Location` is `path`, `query`, `header`, or `body`.
  `Required` is `yes`, `no`, or `conditional` with the condition in the
  description. With no fields, write `No request fields.`
- `# Response` documents success and error fields in a `Field | Status | Type |
  Required | Description` table. Its `## Status codes` table lists every status
  code or protocol outcome with when it occurs. State explicitly when an
  outcome has no body.
- `# Behavior` lists the processing steps in order, with their branches.
- `# Validations` lists every rule the endpoint enforces in a `Rule | Fails
  with` table: required fields, types and formats from `# Request`, and the
  state checks of `# Behavior`, one rule per row. "Fails with" is one status
  code from `## Status codes`. A rule that cannot fail (a default, a clamp)
  belongs in `# Behavior`, and a duplicate request answered from earlier
  work belongs in `# Behavior`'s idempotency, not here. With no rules, write
  `No validations.`
- `# Flowchart` is one Mermaid `flowchart` of every branch of `# Behavior`
  and every validation failure. Every path ends in a status code, and every
  code in `## Status codes` is an exit of the flowchart.
- `# Sequence diagram` shows the caller, this service and every concept
  `# Behavior` names, in order.
- Both diagrams agree with `# Behavior`; the prose and tables are
  authoritative.
- `resource` points at the handler in code, or at the operation in an OpenAPI
  document, when known.
