# Service

[Common rules](schema.md) · [Example](../sample/shop/services/SVC-orders/overview.md)

A deployable backend unit. It owns its Endpoints and Subscriptions as files in its folder.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `Service` |
| Phase | Design |
| Path | `<app>/services/SVC-<slug>/` |
| Shape | Folder with `index.md`, `overview.md`, `log.md` |
| Status | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| Owns | Endpoint, Subscription |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `Service` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Planned`, `Active`, `Modifying`, `Removing`, `Deprecated` |
| `serviceType` | yes | `api`, `worker`, `cron`, `consumer`, `gateway` |
| `ownerTeam` | yes | text |
| `language` | no | text |
| `framework` | no | text |
| `runtime` | no | text |
| `deployTarget` | no | `k8s`, `lambda`, `vm` |
| `slaTier` | no | text |
| `version` | no | text |
| `port` | no | whole number |
| `healthcheckPath` | no | text |
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
| `# Publishes` | optional | author | MessageChannel (any number) |  |  |
| `# Calls` | optional | author | Endpoint, Operation (any number) |  |  |
| `# Reads` | optional | author | Table (any number) |  |  |
| `# Writes` | optional | author | Table (any number) |  |  |
| `# Uses` | optional | author | Cache, BlobStore, SearchIndex (any number) | `read`, `write`, `rw` (required) |  |
| `# Depends on` | optional | author | ExternalService (any number) | `critical` (optional) |  |
| `# Pending changes` | conditional | author | Feature, ChangeRequest (1 or more) | `new`, `modified`, `removed` (required) |  |
<!-- generated:schema end -->

## Rules

- Summary prose after the title says what the service is responsible for.
- `resource` is the service's repository, or its directory in a monorepo.
- `# Calls` lists every Endpoint of another Service and every external Operation
  this service calls synchronously.
- `# Depends on` lists an ExternalService only when no Operation under `# Calls`
  already covers it, for example an embedded SDK. Qualify `critical` when its
  outage stops this service.
- `# Uses` qualifies each datastore `read`, `write`, or `rw`.
- The Feature that uses a service links it under `## Services`; the service does
  not link back.
