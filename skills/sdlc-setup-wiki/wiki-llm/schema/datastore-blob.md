# BlobStore

[Common rules](schema.md) · [Example](../sample/shop/datastores/BLOB-product-images/overview.md)

An object or file store.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `BlobStore` |
| Phase | Design |
| Path | `<app>/datastores/BLOB-<slug>/` |
| Shape | Folder with `index.md`, `overview.md`, `log.md` |
| Status | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `BlobStore` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| `provider` | yes | text |
| `bucket` | no | text |
| `pathPattern` | no | text |
| `region` | no | text |
| `publicAccess` | no | `true` or `false` |
| `encryption` | no | `true` or `false` |
| `lifecyclePolicy` | no | text |
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
| `# Content types` | required | author |  |  |  |
| `# Used by` | always | tool | mirrors Service `# Uses` |  |  |
| `# Pending changes` | conditional | author | Feature, ChangeRequest (1 or more) | `new`, `modified`, `removed` (required) |  |
<!-- generated:schema end -->

## Rules

- `# Content types` lists the stored media types and any size limits.
- `provider` is free text; common values are `s3`, `gcs`, `azure-blob`, `minio`.
