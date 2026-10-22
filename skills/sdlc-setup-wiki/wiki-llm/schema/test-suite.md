# TestSuite

[Common rules](schema.md) · [Example](../sample/shop/tests/TS-checkout/overview.md)

A group of TestCases of one kind. It owns its TestCases as files in its folder.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `TestSuite` |
| Phase | Verify |
| Path | `<app>/tests/TS-<slug>/` |
| Shape | Folder with `index.md`, `overview.md`, `log.md`, `checklist.csv` |
| Status | `Draft`, `Approved`, `Implemented`, `Deprecated` |
| Owns | TestCase |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `TestSuite` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Draft`, `Approved`, `Implemented`, `Deprecated` |
| `suiteType` | yes | `unit`, `integration`, `e2e`, `load`, `security` |
| `basedOn` | yes | list of `{ id, version, at }`, one per target under `# Verifies` |
| `framework` | no | text |
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
| `# Verifies` | required | author | Feature, ChangeRequest (1 or more) |  |  |
| `# References` | optional | author | Reference (any number) |  |  |
<!-- generated:schema end -->

## Rules

- Prose after the title says what the suite exercises and against what
  environment.
- `basedOn` has one entry per Feature or ChangeRequest under `# Verifies`:
  its key as `id`, and the version the cases were designed from. See
  [Spec versions](schema.md#spec-versions).
- `checklist.csv` is written by the tool from the TestCases: columns `No`,
  `Title`, `Description`, `Covers`, `Purpose`; one row per case, highest
  `risk` first, then by title; `Covers` holds the keys of everything the case
  covers, joined by `; `. Nobody edits it.
- `status` is the suite's design lifecycle: `Draft` while cases are being written,
  `Approved` once reviewed, `Implemented` when runnable tests exist. The wiki
  does not record pass and fail results.
- `resource` is where the runnable tests live, once they exist.
- A test plan the suite was written from is a [Reference](reference.md),
  linked under `# References`.
