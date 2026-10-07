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
| `# Validations` | required | author |  |  |  |
| `# Handler` | required | author |  |  |  |
| `# Flowchart` | required | author |  |  | Mermaid `flowchart` diagram |
| `# Sequence diagram` | required | author |  |  | Mermaid `sequenceDiagram` diagram |
| `# Idempotency` | required | author |  |  |  |
| `# Failure behavior` | required | author |  |  |  |
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
- A message ends in one of four outcomes: `ack` (processed), `drop` (acked
  without processing, and logged), `retry` (redelivered), or `dead letter`.
- `# Validations` lists every rule the handler checks on a message in a
  `Rule | Fails with` table: the payload fields it needs and the state
  checks of `# Handler`, one rule per row. "Fails with" is `drop`, `retry`
  or `dead letter`; for retry details link `# Failure behavior`. A
  redelivered message already processed is not a failed rule: it belongs in
  `# Idempotency`. With no rules, write `No validations.`
- `# Flowchart` is one Mermaid `flowchart` of every branch of `# Handler`,
  duplicates included, and every validation failure. Every path ends in one
  of the four outcomes.
- `# Sequence diagram` shows the channel, this service and every concept
  `# Handler` names, in order.
- Both diagrams agree with `# Handler`; the prose and tables are
  authoritative.
