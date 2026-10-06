# ExternalService

[Common rules](schema.md) · [Example](../sample/shop/externals/EXT-stripe/overview.md)

A third-party service, or another application's service. It owns its Operations as files in its folder.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `ExternalService` |
| Phase | Design |
| Path | `<app>/externals/EXT-<slug>/` |
| Shape | Folder with `index.md`, `overview.md`, `log.md` |
| Status | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| Owns | Operation |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `ExternalService` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| `vendor` | yes | text |
| `apiUrl` | yes | URL or bundle path |
| `authType` | no | text |
| `slaTier` | no | text |
| `costModel` | no | lower-case words joined by `-`; common: `per-call`, `subscription` |
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
| `# Fallback` | required | author |  |  |  |
| `# References` | optional | author | Reference (any number) |  |  |
| `# Pending changes` | conditional | author | Feature, ChangeRequest (1 or more) | `new`, `modified`, `removed` (required) |  |
<!-- generated:schema end -->

## Rules

- Prose after the title says how this application depends on the service.
- `# Fallback` states what happens when the service is unavailable, and whether
  that stops a user-facing flow.
- When the target is another application's Service in the same bundle, `resource`
  links that Service's `overview.md`.
