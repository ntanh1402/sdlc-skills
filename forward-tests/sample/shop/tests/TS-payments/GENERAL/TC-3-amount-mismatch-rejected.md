---
type: TestCase
title: Amount mismatch rejected
description: Prove caller cannot authorize an amount different from order total.
risk: critical
testType: integration
testCategory: negative
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Amount mismatch rejected

# Covers

* [EP-payments-authorize](../../../services/SVC-payments/EP-payments-authorize.md)

# Purpose

Prove caller cannot authorize an amount different from order total.

# Preconditions

Order total is known; Stripe mock and repository are empty.

Data that must exist:

* order total: 100.00
* requested amount: 99.00

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call API `POST /payments/authorize` for the order of total 100.00 with amount 99.00 | Response POST /payments/authorize:<br>- status: 422<br>- error: amount mismatch | Read the response; check **status** and **error** |
| 2 | Read the Stripe mock's calls, query table `payments` and consume topic `payment.authorized` | Operation POST /v1/payment_intents:<br>- Calls received: 0<br>Table payments:<br>- Rows found: 0<br>Topic payment.authorized:<br>- Messages found: 0 | Count each; check **calls received**, **rows found** and **messages found** |

# Postconditions and cleanup

Reset fixtures.
