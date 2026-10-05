# TestCase format

A TestCase is one file in its suite's folder:
`wiki/<app>/tests/TS-<name>/TC-<name>.md`, its key lower-case words from its
title, for example `TC-coupon-expired-rejected`. Read
`.wiki-llm/schema/test-case.md` for the rules.

```markdown
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

| Input | Value |
|---|---|
| coupon | `SPRING10` (expired 1 day ago); boundary: expiring this second |
| cart total | 20.00 |

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Apply `SPRING10` to the cart | 422 with code `coupon_expired` | Response status and body |
| 2 | Read the cart | Total is still 20.00 | `GET /carts/{id}` total field |
| 3 | Check the coupon ledger | No redemption row | Query `TBL-coupon-redemptions` for the cart id |

# Postconditions and cleanup

The cart is unchanged; delete the test cart.
```

- `# Covers` links Requirements by full path and anchor (a Requirement key is
  unique only inside its Feature), and the Design concepts and decisions the
  case proves.
- Every step has an observable expected result and names what is inspected.
  "Works" is never a validation.
- Include negative checks, such as no row, no event or no external call, when
  they matter.
- A case never records a test result; the wiki holds none.
- Do not write `generated` or `verified`; `draft finish` does.
