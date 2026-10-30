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
| `testCaseId` | no | text |
| `risk` | yes | `low`, `med`, `high`, `critical` |
| `priority` | no | `high`, `medium`, `low` |
| `testingType` | no | `functional`, `non-functional` |
| `category` | no | `business-rule`, `field-validation`, `error-handling`, `data-integrity`, `idempotency`, `security`, `performance`, `reliability`, `usability`, `compatibility` |
| `polarity` | no | `positive`, `negative` |
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
| `# Covers` | required | author | Feature, ChangeRequest, UserStory, Requirement, any Design type, ArchitectureDecision (1 or more) |  |  |
| `# Purpose` | required | author |  |  |  |
| `# Preconditions` | required | author |  |  |  |
| `# Test data` | required | author |  |  |  |
| `# Steps` | required | author |  |  | table with columns `Step`, `Action`, `Expected result`, `Validation` |
| `# Postconditions and cleanup` | required | author |  |  |  |
| `# References` | optional | author | Reference (any number) |  |  |
<!-- generated:schema end -->

## Rules

### Classification fields

- `testCaseId` is in capitals (`TC-CPN-INT-001`); the key is the ID in lower
  case plus words from the title.
- `category` belongs to the `testingType`: `business-rule`,
  `field-validation`, `error-handling`, `data-integrity`, `idempotency` are
  `functional`; the rest are `non-functional`.
- A designed case fills all five fields; an imported case may leave them out.
  A case has no `tags`.

### Covers and Purpose

- `# Covers` links, in order: the Feature or ChangeRequest, the user story
  if any and Requirements by path and anchor, Design concepts, decisions. An
  imported case may cover only Design concepts.
- `# Purpose` is one or two sentences naming the `AC-<n>` and the technique.

### Preconditions and Test data

- `# Preconditions` is a list: each state the case needs and how it is
  reached, any stub with its answer, any clock or setting with its value.
- `# Test data` is a `No | Input | Value` table numbered 1, 2, 3, …; steps
  say "data 2". A value is `<field>: <value>`, fields of one input separated
  by commas, a note in brackets.
- Values with the same expected result (boundary values inside a limit) are
  one row each, and the step says `- Data 1 to 3, one run each`.

### Steps

- `# Steps` is a `Step | Action | Expected result | Validation` table, lines
  inside a cell joined with `<br>`. "Works" is never an expected result.
- **Action**: a verb phrase with its target, ending with `:` ("Apply the
  coupon `POST /carts/{id}/coupons`:"), then `- ` lines: the data and
  `- Request: see Step <n>`; `- Filter:`, `- Sort:`, `- Path:`, `- Query:`
  for a read; `- Wait: up to <n> s, checking every <m> s` for a late
  outcome.
- **Expected result**: one `<field>: <value>` per line, starting with the
  status code or the count found (`Rows found: 1`).
- **Validation**: the place in bold, then what is read there: **API
  response**, **Database**, **Message**, **Log**, **Cache**, **External
  system**, **Screen**, **File**, **Metric** or **Alert**.
- A step that calls an API or publishes a message has a `### Step <n>` block
  with a `Request` and an `Expected response` (status and checked fields
  only, then "Other fields are ignored."), taken from the Endpoint or the
  channel's `# Payload`.

### Postconditions and cleanup

- A list: the state the case leaves, then each clean-up action as a verb
  with its target ("Delete the rows of table `coupon_redemptions` with
  `cart_id` = `c-1`.").

### Results and removed Requirements

- A TestCase says what is tested and how. Whether it passes is not recorded in
  the wiki: the test runner and CI hold results.
- A step that removes a Requirement fixes the cases that cover it in the same
  change: it drops the Requirement from `# Covers`, and deletes a case left
  with nothing under `# Covers`. A deleted case is logged in its suite's
  `log.md`, and the suite's `index.md` is rewritten by `sync`. Nothing else in
  a case is rewritten by that step. The cases stay in a suite that may then
  hold none.
