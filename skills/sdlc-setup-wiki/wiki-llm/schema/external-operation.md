# Operation

[Common rules](schema.md) · [Example](../sample/shop/externals/EXT-stripe/OP-payment-intents-create.md)

One call this application makes on an ExternalService.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `Operation` |
| Phase | Design |
| Path | `<app>/externals/EXT-*/OP-<slug>.md` |
| Shape | One file |
| Status | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `Operation` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| `method` | yes | text |
| `path` | yes | text |
| `timeoutMs` | no | whole number |
| `rateLimit` | no | text |
| `costPerCall` | no | text |
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
| `# Schema` | required | author |  |  |  |
| `# Failure handling` | required | author |  |  |  |
| `# References` | optional | author | Reference (any number) |  |  |
| `# Pending changes` | conditional | author | Feature, ChangeRequest (1 or more) | `new`, `modified`, `removed` (required) |  |
<!-- generated:schema end -->

## Rules

- `# Schema` documents request and response fields in a `Direction | Field | Type
  | Required` table.
- `# Failure handling` documents error codes, retry policy, and fallback.
- Record only operations the application actually calls.
