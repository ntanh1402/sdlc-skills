# TestCase format

A TestCase is one file in its suite's folder:
`wiki/<app>/tests/TS-<name>/TC-<name>.md`, its key lower-case words from its
title, for example `TC-coupon-expired-rejected`. Read
`.wiki-llm/schema/test-case.md` for the rules.

````markdown
---
type: TestCase
title: Expired coupon is rejected
description: Prove an expired coupon never reduces the order total.
risk: high
---

# Expired coupon is rejected

# Covers

* [REQ-coupons-reject-expired](../../features/FEAT-coupons/overview.md#req-coupons-reject-expired)
* [EP-coupon-apply](../../services/SVC-checkout/EP-coupon-apply.md)

# Purpose

Prove an expired coupon is refused and leaves the cart unchanged.

# Preconditions

A cart with one item at 20.00; coupon `SPRING10` expired yesterday.

# Test data

| No | Input | Value |
|---|---|---|
| 1 | coupon | `SPRING10` (expired 1 day ago); boundary: expiring this second |
| 2 | cart total | 20.00 |

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Apply data 1 to the cart. Request: see Step 1 | 422 with code `coupon_expired` | Response status and body |
| 2 | Read the cart | Total is still data 2 | `GET /carts/{id}` total field |
| 3 | Check the coupon ledger | No redemption row | Query `TBL-coupon-redemptions` for the cart id |

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

The cart is unchanged; delete the test cart.
````

A step that publishes to a channel shows the message the same way: the
channel name, then the key, the headers and the body, as the channel's
`# Payload` defines them. The expected result of a consumer is then what it
writes or publishes, shown the same way when it is a message.

- `# Covers` links Requirements by full path and anchor (a Requirement key is
  unique only inside its Feature), and the Design concepts and decisions the
  case proves.
- `# Test data` is a `No | Input | Value` table. `No` counts 1, 2, 3, … in
  order; a step refers to data by its number ("data 2").
- Every step has an observable expected result and names what is inspected.
  "Works" is never a validation.
- A step that calls an API or publishes to a channel says "Request: see Step
  <n>" in its Action cell, and has a `### Step <n>` block under the table
  with its `Request` (method and path or channel, headers, body, with the
  values of the test data) and its `Expected response` (the status and only
  the fields the step checks, then "Other fields are ignored."). Take the
  fields from the Endpoint's `# Request` and `# Response` or the channel's
  `# Payload`; never invent one. A response with no body shows the status
  only.
- Include negative checks, such as no row, no event or no external call, when
  they matter.
- A case never records a test result; the wiki holds none.
- Do not write `generated` or `verified`; `draft finish` does. It also
  writes the suite's `checklist.csv` from the cases' titles, descriptions,
  `# Covers` and `# Purpose`, so keep the `description` and `# Purpose`
  short and plain: they are the checklist's columns.
