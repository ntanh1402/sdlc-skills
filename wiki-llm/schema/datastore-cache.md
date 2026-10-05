# Cache

[Common rules](schema.md) · [Example](../sample/shop/datastores/CACHE-catalog/overview.md)

A key-value cache.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `Cache` |
| Phase | Design |
| Path | `<app>/datastores/CACHE-<slug>/` |
| Shape | Folder with `index.md`, `overview.md`, `log.md` |
| Status | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `Cache` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| `engine` | yes | text |
| `version` | no | text |
| `keyPattern` | no | text |
| `dataType` | no | `string`, `hash`, `set`, `zset`, `json` |
| `evictionPolicy` | no | text |
| `ttlSeconds` | no | whole number |
| `maxMemory` | no | text |
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
| `# Value` | required | author |  |  |  |
| `# Caches` | required | author | Table, Endpoint (any number) |  |  |
| `# Used by` | always | tool | mirrors Service `# Uses` |  |  |
| `# Pending changes` | conditional | author | Feature, ChangeRequest (1 or more) | `new`, `modified`, `removed` (required) |  |
<!-- generated:schema end -->

## Rules

- `# Value` describes the stored value, in prose or a `Field | Type | Required |
  Notes` table.
- `# Caches` links each Table or Endpoint whose data the cache holds, with how it
  is invalidated.
- `engine` is free text; common values are `redis` and `memcached`.
