# Convention

[Common rules](schema.md) · [Example](../sample/shop/conventions.md)

The engineering rules every repository of the application follows. Build and review skills read this before writing or judging code.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `Convention` |
| Phase | Plan |
| Path | `<app>/conventions.md` |
| Shape | One file |
| Status | None; this type has no `status` field |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `Convention` |
| `title` | yes | text |
| `description` | yes | text |
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

Any other headings are allowed.
<!-- generated:schema end -->

## Rules

- One file per application, named `conventions.md`.
- Suggested sections: `# Coding standards`, `# Branching and review`,
  `# Testing policy`, `# Definition of done`. Add others as needed.
- State rules that a reviewer can check. Leave out preferences nobody enforces.
- Do not restate a concept's contract here; link the concept.
