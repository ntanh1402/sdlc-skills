# TestSuite

[Common rules](schema.md)

The container of the test design of one Feature or ChangeRequest. It owns
its [TestGroups](test-group.md): one `STORY-<name>/` folder for each user
story whose cases are written, and `GENERAL/` for the cases that prove no
single story. Each group owns its TestCases:

```text
TS-coupons/
  overview.md  checklist.csv  index.md
  STORY-coupons-apply/
    overview.md  log.md  index.md
    TC-1-valid-coupon-reduces-total.md
    TC-2-expired-coupon-rejected.md
  GENERAL/
    overview.md  log.md  index.md
    TC-3-checkout-with-coupon-end-to-end.md
```

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `TestSuite` |
| Phase | Verify |
| Path | `<app>/tests/TS-<slug>/` |
| Shape | Folder with `index.md`, `overview.md`, `checklist.csv` |
| Status | None; this type has no `status` field |
| Owns | TestGroup |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `TestSuite` |
| `title` | yes | text |
| `description` | yes | text |
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
| `# Verifies` | required | author | Feature, ChangeRequest (exactly 1) |  |  |
| `# References` | optional | author | Reference (any number) |  |  |
<!-- generated:schema end -->

## Rules

- One suite per Feature or ChangeRequest: `TS-<name>`, the target's key
  without its prefix (`FEAT-coupons` → `TS-coupons`). `# Verifies` links that
  one target.
- Prose after the title says what the suite exercises and against what
  environment.
- A suite has no status, no spec version and no log: each group has its own.
- A case's id, the number in `TC-<id>-<name>`, is unique in the suite across
  its groups, counts from 1, and is never reused after a case is deleted: a
  new case takes the highest id + 1.
- `checklist.csv` is written by the tool from the TestCases: columns `No`,
  `Group`, `Title`, `Description`, `Category`, `Covers`, `Purpose`; one row
  per case, highest `risk` first, then by title. `No` is the case id,
  `Group` its folder, `Category` its `testCategory`, and `Covers` the
  acceptance criteria of the group's story it proves (`AC 1, 3`), empty in
  `GENERAL`. Nobody edits it.
- `resource` is where the runnable tests live, once they exist.
- A suite has no type: each case has its own `testType`. A developer's unit
  tests are written with the code (`sdlc-build-task`); load tests are not
  kept in the wiki.
- A test plan the suite was written from is a [Reference](reference.md),
  linked under `# References`.
