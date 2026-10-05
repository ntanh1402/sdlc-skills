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
| `authType` | no | `none`, `apikey`, `jwt`, `oauth` |
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
| `# Validations` | optional | author |  |  |  |
| `# Behavior` | required | author |  |  |  |
| `# Sequence diagram` | optional | author |  |  | Mermaid `sequenceDiagram` diagram |
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
- `# Sequence diagram` is worth adding when the behavior involves two or more
  other concepts. When present it must agree with `# Behavior`; the prose and
  tables are authoritative.
- `resource` points at the handler in code, or at the operation in an OpenAPI
  document, when known.
