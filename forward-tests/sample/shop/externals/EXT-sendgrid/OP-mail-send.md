---
type: Operation
title: Send mail
description: POST /v3/mail/send — send one transactional email.
status: Active
method: POST
path: /v3/mail/send
timeoutMs: 5000
rateLimit: 600/min
costPerCall: 0.0008 USD
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Send mail

The one [SendGrid](overview.md) call this application
makes, from
[SUB-order-created](../../services/SVC-notifications/SUB-order-created.md).
Uses a stored template; the shop does not send raw HTML.

# Schema

| Direction | Field | Type | Required |
|---|---|---|---|
| Request | `personalizations` | array | yes |
| Request | `from` | object | yes |
| Request | `template_id` | string | yes |
| Request | `dynamic_template_data` | object | yes |
| Response | `message_id` | string | yes |

# Failure handling

| Code | Meaning | What we do |
|---|---|---|
| 400 / 413 | malformed or oversized payload | **Our bug.** Mark `failed`, do not retry, alert. |
| 401 | bad API key | Mark `failed`, page — every email is down. |
| 429 | rate limited | Back off and retry; the row stays `pending`. |
| 5xx / 503 | SendGrid outage | Back off and retry to the subscription's max attempts, then dead-letter. |

Retry: exponential backoff on 429 and 5xx only. A 4xx is **never** retried —
retrying a request the provider already rejected as malformed just burns the
attempt budget a real outage would need.

Fallback: leave the notification row `pending` and retry. Never fail the order.
