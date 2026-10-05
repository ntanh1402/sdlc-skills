# Source document (`Reference`)

[Common rules](schema.md) · [Example](../sample/shop/features/FEAT-checkout/prd.md)

Human-approved source material kept beside the concept it belongs to: a PRD in a Feature folder, a change brief in a ChangeRequest folder, an architecture document in the Application folder, a test plan in a TestSuite folder.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `Reference` |
| Phase | Source |
| Path | `<app>/<name>.md, <app>/features/FEAT-*/<name>.md, <app>/change-requests/CR-*/<name>.md or <app>/tests/TS-*/<name>.md` |
| Shape | One file |
| Status | None; this type has no `status` field |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `Reference` |
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

Any other headings are allowed.
<!-- generated:schema end -->

## Rules

- A Reference lives in one of four folders: the Application folder, a Feature
  folder, a ChangeRequest folder or a TestSuite folder.
- The filename is chosen by a person, for example `prd.md` or `change-prd.md`.
  It is never a name the folder keeps for itself: `index`, `overview`, `log`,
  and in the Application folder `conventions` and `glossary`.
- An agent may draft the document, but it enters the bundle only after a person
  approves the complete body. That approval is the `verified` entry with a
  `human:` actor, which the tool requires.
- Any change to the body invalidates the approval: update `generated`, and
  replace `verified` only after the person approves again.
- The body is free. Images and other files it links may sit beside it.
- The owning concept, or each file written from the document, lists it in
  `sources`.
