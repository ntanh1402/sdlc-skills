---
type: ExternalService
title: SendGrid
description: Transactional email delivery for customer notifications.
resource: https://sendgrid.com
status: Active
vendor: Twilio SendGrid
apiUrl: https://api.sendgrid.com/v3
authType: apikey
costModel: per-call
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# SendGrid

How this application depends on SendGrid: it is the only path by which a customer
learns their order was placed by email.

# Fallback

Critical to [SVC-notifications](../../services/SVC-notifications/overview.md) — if
SendGrid is down, no email goes out at all.

It is **not** critical to the shop. Checkout completes regardless: sends queue in
[notifications](../../datastores/DB-shop/TBL-notifications.md) as
`pending` and drain on recovery. Never fail an order because an email failed.
