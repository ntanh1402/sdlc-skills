---
type: Operation
title: Create payment intent
description: POST /v1/payment_intents — authorize a charge.
status: Active
method: POST
path: /v1/payment_intents
timeoutMs: 8000
rateLimit: 100/s
costPerCall: 0 USD (bundled in processing fee)
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Create payment intent

The call [SVC-payments](../../services/SVC-payments/overview.md) makes to
authorize a charge, from
[EP-payments-authorize](../../services/SVC-payments/EP-payments-authorize.md). We
create the intent with `capture_method=manual`, so this call **authorizes but
does not capture** — money is only taken later by
[OP-payment-intents-capture](OP-payment-intents-capture.md).

# Schema

| Direction | Field | Type | Required |
|---|---|---|---|
| Request | `amount` | integer (cents) | yes |
| Request | `currency` | string | yes |
| Request | `payment_method` | string (token from the browser) | yes |
| Request | `capture_method` | string (`manual`) | yes |
| Request | `Idempotency-Key` (header) | string (= our `order_id`) | yes |
| Response | `id` | string (`pi_…`) | yes |
| Response | `status` | string | yes |

# Failure handling

| Code | Meaning | What we do |
|---|---|---|
| 200 `requires_capture` | authorized | store `authorized`, proceed to confirm the order |
| 402 `card_declined` | issuer declined | store `declined` + `decline_code`, return 402 to the client — **do not retry** |
| 400 | bad request | our bug; store `failed`, alert |
| 401 | bad API key | page — all payments down |
| 429 | rate limited | back off and retry within the request deadline |
| 5xx | Stripe outage | retry once within the deadline, then fail the authorization |

The `Idempotency-Key` header carries our `order_id`, so a retried authorize for
the same order never double-authorizes: Stripe returns the original intent. A
decline is a **terminal business outcome**, not an error to retry — retrying a
declined card just annoys the issuer's fraud systems.
