# Glossary

[Common rules](schema.md) · [Example](../sample/shop/glossary.md)

The domain terms and user roles of the application, defined once.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `Glossary` |
| Phase | Plan |
| Path | `<app>/glossary.md` |
| Shape | One file |
| Status | None; this type has no `status` field |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `Glossary` |
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
| `# Terms` | required; may be `None` | author |  |  | table with columns `Term`, `Definition` |
| `# Roles` | required; may be `None` | author |  |  | table with columns `Role`, `Description` |
| `# References` | optional | author | Reference (any number) |  |  |
<!-- generated:schema end -->

## Rules

- One file per application, named `glossary.md`.
- `# Terms` defines words that carry a specific meaning in this domain. Use the
  same word everywhere for the same thing.
- `# Roles` defines every role that an `Access` column on a frontend route or
  screen may name.
- Write `None` under a heading that has no entries yet.
