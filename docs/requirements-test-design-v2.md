# Requirements: test design v2 (schema 2, release 2.0.0)

The requirements and decisions behind the test design changes on branch
`test-suite-per-feature`. They were agreed in two question-and-answer sessions;
each decision below names the question it settled. The reasons are in
[ADR 0001](adr/0001-one-test-suite-per-feature-grouped-by-story.md); the
terms are in [CONTEXT.md](../CONTEXT.md).

## 1. Suite and folders

- One test suite per Feature **or** ChangeRequest, named `TS-<name>`: the
  target's key without its prefix (`FEAT-coupons` → `TS-coupons`).
- The suite is only a container: `overview.md` with `# Verifies` (exactly one
  Feature or ChangeRequest), and the tool-written `index.md` and
  `checklist.csv`. It has **no status, no `basedOn`, no `log.md`** (decision:
  remove approval status from the suite; keep `# Verifies`).
- Inside the suite, test groups:
  - `STORY-<name>/`: the cases that prove one user story, named exactly as
    the story.
  - `GENERAL/`: every case tied to no single story, of any type (decision:
    the folder first called `E2E` is named `GENERAL`, because it also holds
    integration and security-category cases).
- Each group (new type **TestGroup**) has its own `overview.md`, `log.md`
  and tool-written `index.md`:
  - `status`: `Draft`, `Approved`, `Implemented` or `Deprecated`; each group
    is approved on its own.
  - `basedOn: { version, at }`: the spec version of the suite's target the
    cases were designed from (decision: `basedOn` moves from the suite to
    the group; `outdated` lists groups).
  - `# Story` linking its story (a `STORY-*` group), or `# Scope` saying
    which flows it covers (`GENERAL`).
  - optional `# Open questions` (see section 5).

## 2. Test cases

- File name `TC-<id>-<name>.md` (decision: the id is in the file name).
- The id is a number from 1, unique across the whole suite (all groups),
  never reused after a case is deleted; a new case takes the highest id + 1.
- `testType`: `integration` or `e2e`. Load tests are removed and are not
  imported; unit tests come with the code (`sdlc-build-task`). Security is
  no longer a type (decision: security is a category).
- `testCategory`, optional, one value (decision: the user's seven
  categories, written lower-case):
  - `functional`: happy paths, alternate flows, business rules, state
    transitions.
  - `field-validation`: required and optional fields, format, length, enum,
    null or blank, boundaries.
  - `negative`: invalid business conditions, ineligible customers, accounts
    or cards, invalid states.
  - `error-handling`: downstream errors, timeouts, retries, duplicates,
    idempotency and partial failures where specified.
  - `data-validation`: stored records, relationships, event payloads,
    consistency and audit fields where observable.
  - `security-validation`: authorization, access control and sensitive-data
    exposure within the documented scope.
  - `integration`: downstream interactions, request and response mapping,
    correlation ids, downstream state and error propagation.
- No `# Test data` heading (decision: removed). `# Preconditions` holds the
  state before the test and the predefined data that must exist, with
  concrete values.

## 3. Covers and acceptance criteria

- `# Covers` links Requirements (full path and anchor), Design concepts and
  decisions.
- A case in a `STORY-*` group links its story first, with the acceptance
  criteria it proves after the link:
  `* [STORY-coupons-apply](…/STORY-coupons-apply.md) — AC 1, 3`
  (decision: a qualifier on the story link; stories are not changed, no
  anchors are added to criteria). It also keeps its Requirement links.
- A case in `GENERAL/` never links a user story.
- Every acceptance criterion of a story is proved by at least one case of its
  group.

## 4. Steps

- Steps never refer to test data, other steps or anything else ("data 2",
  "see Step 1", "the cart above"); each Action copies the values it needs.
- Each Action says clearly what to do and its target: "Call API
  `POST /orders`", "Publish message to topic `order.created`", "Query table
  `orders`", "Open page".
- Preconditions, Steps and Postconditions use the **real names** from the
  design (a table's `tableName`, a channel's exact topic `channelName`, an
  endpoint's `method` and `path`, a cache `keyPattern`, a `bucket`, an
  `indexName`), never a wiki key such as `TBL-account`.
- When the design lacks a real name a case needs, the test skill stops before
  the Intent gate and routes to `sdlc-design-arch` (decision: never fall
  back to the wiki key or a made-up name).
- **Expected result**: one checkpoint per table, topic, cache entry, page or
  group of API fields, headed by its kind and real name and a colon, then one
  `- <field>: <value>` line per point, joined with `<br>` (decision: `<br>`;
  the tool does not enforce the format):
  `Table orders:<br>- Rows found: 2<br>- status: DECLINED<br>Table order_events:<br>- Rows found: 1 per order`
- **Validation**: says how the result is checked and names each checked
  field in **bold** (decision: the tool reports a Validation with no bold
  field).
- A step that calls an API or publishes a message keeps its `### Step <n>`
  block with the request and the expected response.

## 5. Open questions

- A group's `overview.md` may have `# Open questions`: a numbered list of
  questions about the Feature, the acceptance criteria or the system design
  that the cases cannot settle; each item links what it is about.
- A group with open questions stays `Draft`. The run that applies an answer
  removes the question and logs the answer.

## 6. Checklist

`checklist.csv` per suite, written by the tool: columns `No, Group, Title,
Description, Category, Covers, Purpose`, highest risk first, then by title.
`No` is the case id; `Covers` shows only the criteria for a story case
(`AC 1, 3`) and is empty for a `GENERAL` case (decision).

## 7. Skills

`sdlc-design-tests` is replaced by two skills (decision):

- **`sdlc-design-feature-tests`**: one Feature or ChangeRequest per run;
  writes only `GENERAL/`: end-to-end flows across stories and cases tied to
  no single story (nonfunctional Requirements, cross-endpoint checks). A
  Functional Requirement no story lists gets no case; it is named for
  `sdlc-write-stories`. It empties a group whose story is gone (cases move
  to `GENERAL/` with their ids). Draft `tests-<Key>`.
- **`sdlc-design-story-tests`**: one user story per run; writes only that
  story's `STORY-<name>/` group, proving every criterion; fixes the story
  drift warnings of its group, and moves a case that covers none of the
  story's Requirements to `GENERAL/`. Draft `tests-<story key>`.
- Both create the suite when it is missing, approve only their own group,
  and may run at the same time.
- `sdlc-write-stories` does not change test files (decision: it stays as it
  was before schema 2).
- `sdlc-import` imports integration, e2e and security-category tests into
  groups, never unit or load tests.

## 8. Tool checks

- Errors: duplicate case id in a suite; a `STORY-*` group without `# Story`
  linking its story, or `GENERAL` with one; a story case without its AC link;
  a `GENERAL` case linking a story; a Validation without bold; wiki keys or
  "see Step n" in steps; open questions in a group that is not `Draft`.
- Warnings, so `sdlc-write-stories` can always finish (decision): a story
  group whose story is gone (and the broken links to it), an AC number that
  does not exist, a criterion no case proves, a story case covering none of
  the story's Requirements. The test skills fix them before approving.

## 9. Migration

- Schema version 2 (decision: all of this is in one schema version and
  release 2.0.0, as 2.0.0 was never released).
- No automatic conversion of old suites: `migrate` from 1 to 2 deletes every
  schema 1 suite and reports the Features and ChangeRequests whose tests must
  be designed again (decision: regenerate the test cases).
