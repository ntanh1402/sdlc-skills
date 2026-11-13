---
type: TestCase
title: Decline is terminal
description: Prove card decline is stable, visible, and not retried.
risk: critical
testType: integration
testCategory: negative
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Decline is terminal

# Covers

* [REQ-payments-authorize-once](../../../features/FEAT-payments/overview.md#req-payments-authorize-once)

# Purpose

Prove card decline is stable, visible, and not retried.

# Preconditions

Stripe mock returns `card_declined`; no payment row exists.

Data that must exist:

* order ID: a unique order ID
* decline code: `insufficient_funds`

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call API `POST /payments/authorize` with the order id while the Stripe mock declines with `insufficient_funds` | Response POST /payments/authorize:<br>- status: 402<br>- decline code: insufficient_funds | Read the response; check **status** and **decline code** |
| 2 | Query table `payments` for the order id | Table payments:<br>- status: declined<br>- decline_code: insufficient_funds | Read the row; check **status** and **decline_code** |
| 3 | Advance the retry scheduler past its next run | Operation POST /v1/payment_intents:<br>- Calls received: still 1<br>Topic payment.authorized:<br>- Messages found: 0 | Read the Stripe mock's calls and the captured messages; check **calls received** and **messages found** |

# Postconditions and cleanup

Reset mock/repository/scheduler.
