---
type: ExternalService
title: Twilio
description: SMS delivery for customer order notifications.
resource: https://www.twilio.com
status: Planned
vendor: Twilio
apiUrl: https://api.twilio.com/2010-04-01
authType: apikey
costModel: per-call
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# Twilio

How this application depends on Twilio: SMS order confirmations, added by
[CR-sms-notifications](../../change-requests/CR-sms-notifications/overview.md). Per-message cost, so it is opt-in
and capped.

# Fallback

**Not** critical to [SVC-notifications](../../services/SVC-notifications/overview.md).
SMS degrades on its own: give up after 3 attempts and let email carry the
notification, which is what
[REQ-order-notifications-confirmation-sent](../../features/FEAT-order-notifications/overview.md#req-order-notifications-confirmation-sent) actually
requires. SMS only serves
[REQ-order-notifications-channel-opt-out](../../features/FEAT-order-notifications/overview.md#req-order-notifications-channel-opt-out), a `Should`.

# Pending changes

* [CR-sms-notifications](../../change-requests/CR-sms-notifications/overview.md) — new — the SMS provider is not called in production yet.
