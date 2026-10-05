---
type: Operation
title: Capture payment intent
description: POST /v1/payment_intents/{id}/capture — capture an authorized charge.
status: Active
method: POST
path: /v1/payment_intents/{id}/capture
timeoutMs: 8000
rateLimit: 100/s
costPerCall: 0 USD (bundled in processing fee)
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Capture payment intent

Captures a previously authorized intent, called by
[EP-payments-capture](../../services/SVC-payments/EP-payments-capture.md) once
the order is ready to ship. Splitting authorize from capture means the customer's
card is only charged for goods that actually go out; an order cancelled before
fulfilment releases the authorization instead of triggering a refund.

# Schema

| Direction | Field | Type | Required |
|---|---|---|---|
| Request | `id` (path) | string (`pi_…`) | yes |
| Request | `amount_to_capture` | integer (cents) | no |
| Response | `id` | string | yes |
| Response | `status` | string (`succeeded`) | yes |

# Failure handling

| Code | Meaning | What we do |
|---|---|---|
| 200 `succeeded` | captured | store `captured` |
| 400 `payment_intent_unexpected_state` | already captured or expired auth | reconcile against our `payments` row; never re-capture |
| 429 | rate limited | back off and retry |
| 5xx | Stripe outage | retry with backoff; capture is not time-critical |

Capture is idempotent on Stripe's side per intent, so a retry after an ambiguous
timeout is safe. Unlike authorize, capture is **not** on the checkout hot path,
so it can retry patiently.
