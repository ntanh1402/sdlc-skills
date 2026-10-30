# TestCase format

A TestCase is one file in its suite's folder:
`wiki/<app>/tests/TS-<name>/TC-<name>.md`. Its key is its test case ID in
lower case followed by lower-case words from its title, for example
`TC-cpn-int-001-coupon-expired-rejected` for the ID `TC-CPN-INT-001`. Read
`.wiki-llm/schema/test-case.md` for the rules.

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

- `priority`, `testingType`, `category` and `polarity` take their values
  from `classification.md`.
- A negative case checks what "Polarity" in `classification.md` says: no
  business effect, and each record the design says a rejection writes,
  checked as written with its values. A negative case with a fallback that
  completes the operation checks the fallback's effect instead, as that
  section says.
- In feature mode, `# Covers` links the story and each `AC-<n>` whose
  criterion the case proves; a case no story's criterion is about links no
  story.
- Do not write `generated` or `verified`; `draft finish` does. It also
  writes the suite's `checklist.csv` from the cases' titles, descriptions,
  `# Covers` and `# Purpose`, so keep the `description` and `# Purpose`
  short and plain: they are the checklist's columns.
