# Application

[Common rules](schema.md) · [Example](../sample/shop/overview.md)

One product or system. Its folder holds everything known about it.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `Application` |
| Phase | Plan |
| Path | `<app>/` |
| Shape | Folder with `index.md`, `overview.md` |
| Status | `Active`, `Archived` |
| Owns | Convention, Glossary, Reference |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `Application` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Active`, `Archived` |
| `ownerTeam` | yes | text |
| `appType` | no | `web`, `mobile`, `platform`, `internal` |
| `criticality` | no | text |
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
| `# Architecture` | required; may be `None` | author |  |  | Mermaid `flowchart` diagram |
<!-- generated:schema end -->

## Rules

- `# Architecture` is the system-level picture: how frontends, services, datastores,
  channels, and externals fit together, with one Mermaid `flowchart`. It names
  concepts by key but does not restate their contracts. Write `None` only before
  any design exists.
- The Application lists nothing by hand. Its `index.md` lists its collections.
- `resource` is the application's main repository or organisation URL.
- Optional files: [conventions](convention.md), a [glossary](glossary.md), and
  [source documents](source-document.md) about the whole application, such as an
  architecture document.
