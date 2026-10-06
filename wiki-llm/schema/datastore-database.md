# Database

[Common rules](schema.md) · [Example](../sample/shop/datastores/DB-shop/overview.md)

A relational database. It owns its Tables as files in its folder.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `Database` |
| Phase | Design |
| Path | `<app>/datastores/DB-<slug>/` |
| Shape | Folder with `index.md`, `overview.md`, `log.md` |
| Status | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| Owns | Table |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `Database` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| `engine` | yes | text |
| `version` | no | text |
| `schemaName` | no | text |
| `replication` | no | `true` or `false` |
| `backupPolicy` | no | text |
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
| `# References` | optional | author | Reference (any number) |  |  |
| `# Pending changes` | conditional | author | Feature, ChangeRequest (1 or more) | `new`, `modified`, `removed` (required) |  |
<!-- generated:schema end -->

## Rules

- Prose after the title describes the engine, schema layout, replication, and
  backup in as much detail as an on-call engineer needs.
- Tables are listed by the folder's `index.md`. Which services use them is shown
  on each Table.
