# Table

[Common rules](schema.md) · [Example](../sample/shop/datastores/DB-shop/TBL-orders.md)

One table of a Database.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `Table` |
| Phase | Design |
| Path | `<app>/datastores/DB-*/TBL-<slug>.md` |
| Shape | One file |
| Status | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `Table` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| `tableName` | yes | text |
| `pii` | no | `true` or `false` |
| `rowCountEstimate` | no | whole number |
| `partitionKey` | no | text |
| `retentionPolicy` | no | text |
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
| `# Indexes` | optional | author |  |  |  |
| `# References` | optional | author | Reference (any number) |  |  |
| `# Used by` | always | tool | mirrors Service `# Reads`, Service `# Writes` |  |  |
| `# Pending changes` | conditional | author | Feature, ChangeRequest (1 or more) | `new`, `modified`, `removed` (required) |  |
<!-- generated:schema end -->

## Rules

- `# Schema` is a `Column | Type | Required | Notes` table. `Required` is `yes`,
  `no`, or `conditional`.
- `# Indexes` lists indexes when they matter to correctness or performance.
- Set `pii: true` when any column holds personal data.
- `resource` points at the migration or model that defines the table, when known.
