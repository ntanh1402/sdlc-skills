# TestCase

[Common rules](schema.md)

One test, written so a tester who did not design the system can run it.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `TestCase` |
| Phase | Verify |
| Path | `<app>/tests/TS-*/<STORY-* or GENERAL>/TC-<id>-<slug>.md` |
| Shape | One file |
| Status | None; this type has no `status` field |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `TestCase` |
| `title` | yes | text |
| `description` | yes | text |
| `risk` | yes | `low`, `med`, `high`, `critical` |
| `testType` | yes | `integration`, `e2e` |
| `testCategory` | no | `functional`, `field-validation`, `negative`, `error-handling`, `data-validation`, `security-validation`, `integration` |
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
| `# Covers` | required | author | Requirement, UserStory, any Design type, ArchitectureDecision (1 or more) |  |  |
| `# Purpose` | required | author |  |  |  |
| `# Preconditions` | required | author |  |  |  |
| `# Steps` | required | author |  |  | table with columns `Step`, `Action`, `Expected result`, `Validation` |
| `# Postconditions and cleanup` | required | author |  |  |  |
| `# References` | optional | author | Reference (any number) |  |  |
<!-- generated:schema end -->

## Rules

- `# Covers` links what the case proves: Requirements by full path and anchor,
  Design concepts, decisions, and user stories with the acceptance criteria
  proved (`* [STORY-coupons-apply](…/STORY-coupons-apply.md) — AC 1, 3`). A
  case in a `STORY-*` group links its story that way; a case in `GENERAL/`
  links no story. See [TestGroup](test-group.md). A case imported from existing tests may cover
  only Design concepts.
- The file is `TC-<id>-<name>.md` in a group of its suite; see
  [TestSuite](test-suite.md) for the id.
- `testType` says how the case runs: `integration` (one service and what it
  calls) or `e2e` (a flow across services, as the user sees it).
- `testCategory`, optional, says what the case checks: `functional` (happy
  paths, alternate flows, business rules, state transitions),
  `field-validation` (required and optional fields, format, length, enum,
  null or blank, boundaries), `negative` (invalid business conditions,
  ineligible customers, accounts or cards, invalid states), `error-handling`
  (downstream errors, timeouts, retries, duplicates, idempotency, partial
  failures), `data-validation` (stored records, relationships, event
  payloads, consistency, audit fields), `security-validation`
  (authorization, access control, sensitive-data exposure) or `integration`
  (calls to downstream systems: request and response mapping, correlation
  ids, downstream state, error propagation).
- `# Preconditions` holds the state before the test and the data that must
  exist then, with concrete values, including boundary values.
- `# Steps` is a `Step | Action | Expected result | Validation` table. Every step
  has an observable expected result and names what is inspected to confirm it.
- An Expected result is one checkpoint per table, topic, cache entry, page
  or group of API fields: its kind and real name and a colon, then one
  `- <field>: <value>` line per point, the lines joined with `<br>`, for
  example `Table orders:<br>- Rows found: 2<br>- status: DECLINED`.
- A Validation says how the result is checked and names each field it
  checks in bold: "Query table `orders` by order id; compare **status**".
- Each Action says by itself what to do, starting with the action and its
  target: "Call API `POST /carts/c-1/coupons`", "Publish message to topic
  `orders.created`", "Query table `coupon_redemptions` for cart `c-1`". It
  copies the values it needs; it never points at another step, the
  preconditions or other data.
- `# Preconditions`, `# Steps` and `# Postconditions and cleanup` use the real
  names from the design: a Table's `tableName`, a MessageChannel's
  `channelName`, an Endpoint's or Operation's `method` and `path`, a Cache's
  `keyPattern`, a BlobStore's `bucket`, a SearchIndex's `indexName`. They
  never use a wiki key such as `TBL-orders`.
- A step that calls an API or publishes to a channel has a `### Step <n>`
  block under the table with a `Request` code block (the method and path, or
  the channel; the headers; the body) and an `Expected response` code block
  (the status and only the fields the step checks), followed by "Other
  fields are ignored."
- A TestCase says what is tested and how. Whether it passes is not recorded in
  the wiki: the test runner and CI hold results.
- A step that removes a Requirement fixes the cases that cover it in the same
  change: it drops the Requirement from `# Covers`, and deletes a case left
  with nothing under `# Covers`. A case left in a `STORY-*` folder that covers
  none of that story's Requirements is reported as a warning, and the test
  skills move it to `GENERAL/`. A deleted case is logged in its group's
  `log.md`, and the indexes are rewritten by `sync`. Nothing else in
  a case is rewritten by that step. The cases stay in a suite that may then
  hold none.
