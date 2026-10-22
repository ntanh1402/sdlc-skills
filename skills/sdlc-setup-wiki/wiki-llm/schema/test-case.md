# TestCase

[Common rules](schema.md) · [Example](../sample/shop/tests/TS-checkout/TC-happy-path.md)

One test, written so a tester who did not design the system can run it.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `TestCase` |
| Phase | Verify |
| Path | `<app>/tests/TS-*/TC-<slug>.md` |
| Shape | One file |
| Status | None; this type has no `status` field |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `TestCase` |
| `title` | yes | text |
| `description` | yes | text |
| `risk` | yes | `low`, `med`, `high`, `critical` |
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
| `# Covers` | required | author | Requirement, any Design type, ArchitectureDecision (1 or more) |  |  |
| `# Purpose` | required | author |  |  |  |
| `# Preconditions` | required | author |  |  |  |
| `# Test data` | required | author |  |  | table with columns `No`, `Input`, `Value`; `No` counts 1, 2, 3, … in order |
| `# Steps` | required | author |  |  | table with columns `Step`, `Action`, `Expected result`, `Validation` |
| `# Postconditions and cleanup` | required | author |  |  |  |
| `# References` | optional | author | Reference (any number) |  |  |
<!-- generated:schema end -->

## Rules

- `# Covers` links what the case proves: Requirements by full path and anchor,
  Design concepts, decisions. A case imported from existing tests may cover only
  Design concepts.
- `# Steps` is a `Step | Action | Expected result | Validation` table. Every step
  has an observable expected result and names what is inspected to confirm it.
- A step that calls an API or publishes to a channel says "Request: see Step
  <n>" in its Action cell. A `### Step <n>` block under the table then holds
  a `Request` code block (the method and path, or the channel; the headers;
  the body) and an `Expected response` code block (the status and only the
  fields the step checks), followed by "Other fields are ignored."
- `# Test data` is a `No | Input | Value` table of concrete values, including
  boundary values. `No` counts 1, 2, 3, … in order, and steps refer to data by
  its number.
- A TestCase says what is tested and how. Whether it passes is not recorded in
  the wiki: the test runner and CI hold results.
- A step that removes a Requirement fixes the cases that cover it in the same
  change: it drops the Requirement from `# Covers`, and deletes a case left
  with nothing under `# Covers`. A deleted case is logged in its suite's
  `log.md`, and the suite's `index.md` is rewritten by `sync`. Nothing else in
  a case is rewritten by that step. The cases stay in a suite that may then
  hold none.
