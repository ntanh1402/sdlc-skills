# MessageChannel

[Common rules](schema.md) · [Example](../sample/shop/channels/CHAN-order-created/overview.md)

A topic or queue and the contract of the messages on it.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `MessageChannel` |
| Phase | Design |
| Path | `<app>/channels/CHAN-<slug>/` |
| Shape | Folder with `index.md`, `overview.md`, `log.md`, `payload.example.json` |
| Status | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `MessageChannel` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| `channelName` | yes | text |
| `kind` | yes | text |
| `channelType` | yes | `topic`, `queue` |
| `schemaFormat` | no | `avro`, `protobuf`, `json` |
| `schemaVersion` | no | text |
| `schemaRegistryUrl` | no | text |
| `partitions` | no | whole number |
| `retentionHours` | no | whole number |
| `ordering` | no | `true` or `false` |
| `deliveryGuarantee` | no | `at-least-once`, `exactly-once`, `at-most-once` |
| `generated` | yes | `{ by, at }` |
| `verified` | no | `{ by, at }`, or a list of them |
| `sources` | no | list of `{ id, resource, title }` |
| `resource` | no | URL or bundle path |
| `stale_after` | no | ISO 8601 timestamp with offset |
| `tags` | no | `[a, b]` |

### Headings

| Heading | Presence | Written by | Links to | Qualifier | Content |
|---|---|---|---|---|---|
| `# Overview` | required; first heading | author |  |  |  |
| `## Dead letter` | required | author |  |  |  |
| `# Payload` | required | author |  |  |  |
| `## Key` | required | author |  |  |  |
| `## Header` | required | author |  |  |  |
| `## Body` | required | author |  |  |  |
| `# Payload example` | required | author |  |  |  |
| `# Publishers` | always | tool | mirrors Service `# Publishes` |  |  |
| `# Subscribers` | always | tool | mirrors Subscription `# Consumes` |  |  |
| `# Pending changes` | conditional | author | Feature, ChangeRequest (1 or more) | `new`, `modified`, `removed` (required) |  |
<!-- generated:schema end -->

## Rules

- `# Overview` says what the channel carries and when a message is produced.
  `ordering` and `deliveryGuarantee` state what the broker provides.
- `## Dead letter` is the one place for the dead-letter destination, its
  retention, alerting, and how to drain it. Retry counts belong to each
  Subscription.
- `# Payload` describes the message: `## Key`, then `## Header` and `## Body`
  tables with `Name` or `Field`, `Required`, `Type`, and `Description` columns.
- `payload.example.json` is a real example with the keys `key`, `headers`, and
  `body`. Its fields must appear in the tables, and every required table field
  must appear in it.
- A contract change is logged in the channel's `log.md` with the schema version.
