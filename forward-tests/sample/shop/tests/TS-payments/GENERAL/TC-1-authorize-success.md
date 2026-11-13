---
type: TestCase
title: Authorize success
description: Prove successful authorization persists and emits once.
risk: critical
testType: integration
testCategory: integration
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Authorize success

# Covers

* [REQ-payments-authorize-once](../../../features/FEAT-payments/overview.md#req-payments-authorize-once)

# Purpose

Prove successful authorization persists and emits once.

# Preconditions

Order exists; payment repository/event publisher are isolated; Stripe mock authorizes.

Data that must exist:

* order ID: a unique order ID
* amount: the order's expected amount
* payment token: a valid token

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call API `POST /payments/authorize` with the order id, the order's amount and a valid token | Operation POST /v1/payment_intents:<br>- Calls received: 1<br>- Idempotency-Key: the order id | Read the Stripe mock's calls; check **calls received** and **Idempotency-Key** |
| 2 | Query table `payments` for the order id | Table payments:<br>- Rows found: 1<br>- amount_usd: the order's amount<br>- status: authorized | Read the rows; check **rows found**, **amount_usd** and **status** |
| 3 | Consume topic `payment.authorized` | Topic payment.authorized:<br>- Messages found: 1<br>- order id: the order id<br>- payment id: the row's `payment_id` | Read the captured messages; check **messages found**, **order id** and **payment id** |

# Postconditions and cleanup

Reset mocks and repository.
