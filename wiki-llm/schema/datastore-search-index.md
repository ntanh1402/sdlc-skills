# SearchIndex

[Common rules](schema.md) · [Example](../sample/shop/datastores/IDX-products/overview.md)

A search index. It is a derived read model, not a source of truth.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `SearchIndex` |
| Phase | Design |
| Path | `<app>/datastores/IDX-<slug>/` |
| Shape | Folder with `index.md`, `overview.md`, `log.md` |
| Status | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `SearchIndex` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| `engine` | yes | text |
| `indexName` | no | text |
| `shards` | no | whole number |
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
| `# Indexed fields` | required | author |  |  |  |
| `# References` | optional | author | Reference (any number) |  |  |
| `# Used by` | always | tool | mirrors Service `# Uses` |  |  |
| `# Pending changes` | conditional | author | Feature, ChangeRequest (1 or more) | `new`, `modified`, `removed` (required) |  |
<!-- generated:schema end -->

## Rules

- Prose after the title names the source of truth the index is built from and how
  it is rebuilt.
- `# Indexed fields` lists each field and how it is indexed.
- `engine` is free text; common values are `opensearch` and `elastic`.
