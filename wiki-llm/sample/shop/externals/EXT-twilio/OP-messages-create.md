---
type: Operation
title: Create message
description: POST /Accounts/{sid}/Messages.json — send one SMS.
status: Planned
method: POST
path: /2010-04-01/Accounts/{AccountSid}/Messages.json
timeoutMs: 5000
rateLimit: 100/s
costPerCall: 0.0079 USD
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Create message

The one [Twilio](overview.md) call this application
makes, from
[SUB-order-created](../../services/SVC-notifications/SUB-order-created.md).

# Schema

| Direction | Field | Type | Required |
|---|---|---|---|
| Request | `To` | string (E.164) | yes |
| Request | `From` | string (E.164) | yes |
| Request | `Body` | string | yes |
| Response | `sid` | string | yes |
| Response | `status` | string | yes |

# Failure handling

| Code | Meaning | What we do |
|---|---|---|
| 21211 | invalid `To` number | **Data problem, not an outage.** Mark `failed`, do not retry. |
| 21610 | recipient replied STOP | Mark `failed` **and** set `sms_opt_out` on [customers](../../datastores/DB-shop/TBL-customers.md) — a carrier-level opt-out is an opt-out. |
| 400 / 401 | malformed request or bad credentials | Mark `failed`, alert. |
| 429 | rate limited | Back off and retry. |
| 5xx | Twilio outage | Back off, retry up to 3 attempts, then give up. |

Fallback: **give up after 3 attempts.** That is acceptable here and not for email —
SMS is a `Should`
([REQ-order-notifications-channel-opt-out](../../features/FEAT-order-notifications/overview.md#req-order-notifications-channel-opt-out)), email is a
`Must` ([REQ-order-notifications-confirmation-sent](../../features/FEAT-order-notifications/overview.md#req-order-notifications-confirmation-sent)). The
per-message cost is the other reason we cap at 3 rather than the subscription's 5.

# Pending changes

* [CR-sms-notifications](../../change-requests/CR-sms-notifications/overview.md) — new — the one call made on Twilio; not live yet.
