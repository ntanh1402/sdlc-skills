# WebFrontend

[Common rules](schema.md) · [Example](../sample/shop/frontends/WEB-storefront/overview.md)

A browser application.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `WebFrontend` |
| Phase | Design |
| Path | `<app>/frontends/WEB-<slug>/` |
| Shape | Folder with `index.md`, `overview.md`, `log.md` |
| Status | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `WebFrontend` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| `ownerTeam` | yes | text |
| `language` | no | text |
| `framework` | no | text |
| `renderingMode` | no | `csr`, `ssr`, `ssg`, `hybrid` |
| `buildTool` | no | text |
| `packageManager` | no | text |
| `deployTarget` | no | `static-host`, `edge`, `container`, `serverless` |
| `baseUrl` | no | text |
| `version` | no | text |
| `browserSupport` | no | text |
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
| `# Routes` | required | author |  |  |  |
| `# Architecture` | required | author |  |  | Mermaid `flowchart` diagram |
| `# Calls` | required | author | Endpoint, Operation (any number) |  |  |
| `# Depends on` | optional | author | ExternalService (any number) | `critical` (optional) |  |
| `# Runtime behavior` | required | author |  |  |  |
| `# Quality constraints` | required | author |  |  |  |
| `# Delivery` | optional | author |  |  |  |
| `# Observability` | optional | author |  |  |  |
| `# Pending changes` | conditional | author | Feature, ChangeRequest (1 or more) | `new`, `modified`, `removed` (required) |  |
<!-- generated:schema end -->

## Rules

- `# Routes` lists every user-addressable route, in a `Route | Surface | Access | Description` table with parameters in braces. `Access` names a role from the
  [glossary](glossary.md).
- `# Architecture` describes major UI modules and state ownership. Its diagram
  shows the frontend and every concept listed under `# Calls` and `# Depends on`.
- Each `# Calls` item says why the call is made and how loading, success, and
  failure change what the user sees.
- `# Depends on` lists an ExternalService only when no Operation under `# Calls`
  already covers it, such as an embedded SDK or third-party script.
- `# Quality constraints` are measurable: supported browsers and viewports, an accessibility target, and performance budgets.
- `resource` is the frontend's repository.
- `# Runtime behavior` covers navigation, rendering, client and server state, caching, session handling, and empty, loading, and error states.
