---
type: TestCase
title: Authorize is idempotent
description: Prove repeated authorization cannot double charge.
risk: critical
testType: integration
testCategory: error-handling
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Authorize is idempotent

# Covers

* [REQ-payments-authorize-once](../../../features/FEAT-payments/overview.md#req-payments-authorize-once)

# Purpose

Prove repeated authorization cannot double charge.

# Preconditions

No payment exists for order; Stripe mock authorizes.

Data that must exist:

* order ID: one order ID, used by two identical calls

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call API `POST /payments/authorize` with the order id | Response POST /payments/authorize:<br>- status: 200<br>- payment status: authorized | Read the response; check **status** and **payment status** |
| 2 | Call API `POST /payments/authorize` again with the same order id and body | Response POST /payments/authorize:<br>- body: equal to the first response | Compare the bodies; check **body** |
| 3 | Read the Stripe mock's calls, query table `payments` and consume topic `payment.authorized` | Operation POST /v1/payment_intents:<br>- Calls received: 1<br>Table payments:<br>- Rows found: 1<br>Topic payment.authorized:<br>- Messages found: 1 | Count each; check **calls received**, **rows found** and **messages found** |

# Postconditions and cleanup

Reset mocks and repository.
