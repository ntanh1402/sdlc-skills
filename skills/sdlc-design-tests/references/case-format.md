# TestCase format

A TestCase is one file in its suite's folder:
`wiki/<app>/tests/TS-<name>/TC-<name>.md`. Its key is its test case ID in
lower case followed by lower-case words from its title, for example
`TC-cpn-int-001-coupon-expired-rejected` for the ID `TC-CPN-INT-001`. Read
`.wiki-llm/schema/test-case.md` for its fields and headings, then write it
as the example and the rules below show.

````markdown
---
type: TestCase
title: Expired coupon is rejected
description: Prove an expired coupon never reduces the order total.
testCaseId: TC-CPN-INT-001
risk: high
priority: high
testingType: functional
category: business-rule
polarity: negative
---

# Expired coupon is rejected

# Covers

* [FEAT-coupons](../../features/FEAT-coupons/overview.md)
* [STORY-coupons-apply-code](../../features/FEAT-coupons/STORY-coupons-apply-code.md), AC-2
* [REQ-coupons-reject-expired](../../features/FEAT-coupons/overview.md#req-coupons-reject-expired)
* [EP-coupon-apply](../../services/SVC-checkout/EP-coupon-apply.md)

# Purpose

AC-2, boundary value analysis: an expired coupon is refused and leaves the
cart total unchanged.

# Preconditions

- A cart with one item at 20.00, created with `POST /carts`.
- Coupon `SPRING10` with an expiry date of yesterday, seeded in table
  `coupons`.
- `SVC-checkout` runs against the coupon store of the test environment; no
  stub.

# Test data

| No | Input | Value |
|---|---|---|
| 1 | Coupon | `code`: `SPRING10` (expired 1 day ago; boundary: a coupon expiring this second) |
| 2 | Cart | `id`: `c-1`, `total`: `20.00` |

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Apply the coupon `POST /carts/{id}/coupons`:<br>- Data 1 on the cart of data 2<br>- Request: see Step 1 | Status code: `422`<br>`code`: `coupon_expired` | **API response**: `POST /carts/c-1/coupons` |
| 2 | Read the cart `GET /carts/{id}`:<br>- Path: `id` = `c-1` | `total`: `20.00` (data 2)<br>`couponCode`: null | **API response**: `GET /carts/c-1` |
| 3 | Query table `coupon_redemptions`:<br>- Filter: `cart_id` = `c-1` | Rows found: 0 | **Database**: `coupon_redemptions` |
| 4 | Search the log of `SVC-checkout`:<br>- Filter: `correlationId` = the one of step 1<br>- Filter: level `WARN` | Lines found: 1<br>`message`: `coupon rejected`<br>`reason`: `expired` | **Log**: `SVC-checkout` |

### Step 1

Request:

```http
POST /carts/c-1/coupons
Authorization: Bearer <shopper token>
Content-Type: application/json

{ "code": "SPRING10" }
```

Expected response:

```http
422 Unprocessable Entity

{ "code": "coupon_expired" }
```

Other fields are ignored.

# Postconditions and cleanup

- The cart total is still `20.00` and no coupon is applied.
- Delete the test cart `DELETE /carts/{id}` with `id` = `c-1`.
````

## Rules

### Classification fields

- Every case has `testCaseId`, `priority`, `testingType`, `category` and
  `polarity`; the last four take their values from `classification.md`.
- `testCaseId` is in capitals (`TC-CPN-INT-001`).
- `category` belongs to the `testingType`: `business-rule`,
  `field-validation`, `error-handling`, `data-integrity`, `idempotency` are
  `functional`; the rest are `non-functional`.
- A case has no `tags`.
- A negative case checks what "Polarity" in `classification.md` says: no
  business effect, and each record the design says a rejection writes,
  checked as written with its values. A negative case with a fallback that
  completes the operation checks the fallback's effect instead, as that
  section says.

### Covers and Purpose

- `# Covers` links, in order: the Feature or ChangeRequest, the user story
  if any and Requirements by path and anchor, Design concepts, decisions.
- In feature mode, `# Covers` links the story and each `AC-<n>` whose
  criterion the case proves; a case no story's criterion is about links no
  story.
- `# Purpose` is one or two sentences naming the `AC-<n>` the case proves,
  if any, and the technique of `classification.md` that chose it.

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

### Generated parts

- Do not write `generated` or `verified`; `draft finish` does. It also
  writes the suite's `checklist.csv` from the cases' titles, descriptions,
  `# Covers` and `# Purpose`, so keep the `description` and `# Purpose`
  short and plain: they are the checklist's columns.
