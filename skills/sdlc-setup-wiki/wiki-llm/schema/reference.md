# Reference

[Common rules](schema.md) · [Example](../sample/shop/references/REF-checkout-prd/overview.md)

Material a person approved for others to read while working: a PRD, a change brief, an architecture document, a test plan, a page explaining a domain term, a vendor's API documentation, or an existing implementation to follow. Any concept links it under `# References`.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `Reference` |
| Phase | Source |
| Path | `<app>/references/REF-<name>/` |
| Shape | Folder with `index.md`, `overview.md`, `log.md`, and any content files and folders |
| Status | `Active`, `Deprecated` |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `Reference` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Active`, `Deprecated` |
| `generated` | yes | `{ by, at }` |
| `verified` | yes, by a `human:` actor | `{ by, at }`, or a list of them |
| `sources` | no | list of `{ id, resource, title }` |
| `resource` | no | URL or bundle path |
| `stale_after` | no | ISO 8601 timestamp with offset |
| `tags` | no | `[a, b]` |

### Headings

| Heading | Presence | Written by | Links to | Qualifier | Content |
|---|---|---|---|---|---|
| `# <title>` | required; first heading | author |  |  |  |
| `# Contents` | required; may be `None` | author |  |  |  |
| `# References` | optional | author | Reference (any number) |  |  |
| `# Referenced by` | always | tool | mirrors any type `# References` |  |  |
<!-- generated:schema end -->

## Rules

- A Reference is a folder in the Application's `references` collection. Its
  key is `REF-<name>`, taken from the title.
- `overview.md` summarises the material: what it is and when to consult it.
  It does not hold the whole material.
- `description` names the subject and when to consult it. Skills find
  References by their title and description.
- `# Contents` lists the main files of the folder, one entry each:
  `* [prd.md](prd.md) — the full PRD as approved`. Images and attachments need
  no entry. It is `None` when the material is entirely at `resource`.
- Any file may sit in the folder beside `overview.md`, in subfolders too: the
  material as Markdown, images, the original `.pdf` or `.docx` it was converted
  from. A content file has no frontmatter and free headings; its internal links
  must resolve. Nothing below the folder's `index.md` needs an index.
- `resource` is the material the Reference points to, when it lives outside
  the bundle. Code is named at a commit or tag, never a branch, and is not
  pasted in; the overview says what to follow and what not to copy.
- `stale_after` suits material that moves, such as code and vendor
  documentation.
- An agent may draft a Reference, but it enters the bundle only after a person
  approves the whole folder. That approval is the `verified` entry with a
  `human:` actor, which the tool requires.
- Any change to a file of the folder invalidates the approval: update
  `generated`, add a `log.md` entry, and replace `verified` only after the
  person approves again. Adding or removing a `# References` entry is the
  exception (see [References](schema.md#references)).
- A Reference is never deleted, because links to it would break. When it no
  longer applies, its status becomes `Deprecated`.
- A Reference belongs to one Application. Another Application that needs the
  same material adds its own Reference.
