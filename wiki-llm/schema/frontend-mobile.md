# MobileFrontend

[Common rules](schema.md) · [Example](../sample/shop/frontends/MB-shop/overview.md)

A native or cross-platform mobile application.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `MobileFrontend` |
| Phase | Design |
| Path | `<app>/frontends/MB-<slug>/` |
| Shape | Folder with `index.md`, `overview.md`, `log.md` |
| Status | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `MobileFrontend` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| `ownerTeam` | yes | text |
| `platform` | yes | `ios`, `android`, `cross-platform` |
| `language` | no | text |
| `framework` | no | text |
| `minimumOsVersion` | no | text |
| `applicationId` | no | text |
| `bundleId` | no | text |
| `distribution` | no | `app-store`, `enterprise`, `internal`, `sideload` |
| `buildTool` | no | text |
| `version` | no | text |
| `offlineCapable` | no | `true` or `false` |
| `generated` | yes | `{ by, at }` |
| `verified` | no | `{ by, at }`, or a list of them |
| `sources` | no | list of `{ id, resource, title }` |
| `resource` | yes | URL or bundle path |
| `stale_after` | no | ISO 8601 timestamp with offset |
| `tags` | no | `[a, b]` |

### Headings

| Heading | Presence | Written by | Links to | Qualifier | Content |
|---|---|---|---|---|---|
| `# <title>` | required; first heading | author |  |  |  |
| `# Screens and navigation` | required | author |  |  |  |
| `# Architecture` | required | author |  |  | Mermaid `flowchart` diagram |
| `# Calls` | required | author | Endpoint, Operation (any number) |  |  |
| `# Depends on` | optional | author | ExternalService (any number) | `critical` (optional) |  |
| `# Runtime behavior` | required | author |  |  |  |
| `# Platform integrations` | required | author |  |  |  |
| `# Deep links` | optional | author |  |  |  |
| `# Quality constraints` | required | author |  |  |  |
| `# Delivery` | optional | author |  |  |  |
| `# Observability` | optional | author |  |  |  |
| `# Pending changes` | conditional | author | Feature, ChangeRequest (1 or more) | `new`, `modified`, `removed` (required) |  |
<!-- generated:schema end -->

## Rules

- `# Screens and navigation` lists every user-addressable screen, in a `Screen | Navigation path | Access | Description` table. `Access` names a role from the
  [glossary](glossary.md).
- `# Architecture` describes major UI modules and state ownership. Its diagram
  shows the frontend and every concept listed under `# Calls` and `# Depends on`.
- Each `# Calls` item says why the call is made and how loading, success, and
  failure change what the user sees.
- `# Depends on` lists an ExternalService only when no Operation under `# Calls`
  already covers it, such as an embedded SDK or third-party script.
- `# Quality constraints` are measurable: supported OS versions and device classes, an accessibility target, and startup, responsiveness, network, and resource budgets.
- `resource` is the frontend's repository.
- `# Runtime behavior` covers app lifecycle, navigation, state, networking, session handling, caching, offline behavior, synchronisation, and recovery.
- `# Platform integrations` lists each native capability in a `Capability | Platform | Permission | Failure behavior` table, or `None`.
