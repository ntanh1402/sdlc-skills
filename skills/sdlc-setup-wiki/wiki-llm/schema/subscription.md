# Subscription

[Common rules](schema.md) · [Example](../sample/shop/services/SVC-notifications/SUB-order-created.md)

One consumer of a MessageChannel, owned by a Service.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `Subscription` |
| Phase | Design |
| Path | `<app>/services/SVC-*/SUB-<slug>.md` |
| Shape | One file |
| Status | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `Subscription` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| `consumerGroup` | yes | text |
| `maxAttempts` | no | whole number |
| `concurrency` | no | whole number |
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
| `# Consumes` | required | author | MessageChannel (exactly 1) |  |  |
| `# Handler` | required | author |  |  |  |
| `# Idempotency` | required | author |  |  |  |
| `# Failure behavior` | required | author |  |  |  |
| `# Sequence diagram` | optional | author |  |  | Mermaid `sequenceDiagram` diagram |
| `# References` | optional | author | Reference (any number) |  |  |
| `# Pending changes` | conditional | author | Feature, ChangeRequest (1 or more) | `new`, `modified`, `removed` (required) |  |
<!-- generated:schema end -->

## Rules

- `# Consumes` links the one MessageChannel this subscription reads.
- `# Handler` lists the handler steps in order.
- `# Idempotency` names the idempotency key and how it is enforced, and says how
  the handler copes with redelivery and out-of-order messages.
- `# Failure behavior` states retry count and backoff. For what happens after the
  last retry, link the channel's dead-letter policy instead of repeating it.
- The channel states what the broker guarantees. Write here only what this
  consumer does differently or additionally.
