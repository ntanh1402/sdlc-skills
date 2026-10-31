---
type: ArchitectureDecision
title: Use Twilio for SMS delivery
description: Use Twilio behind the notification provider boundary for transactional SMS.
status: Accepted
ownerTeam: engagement
decisionDate: 2026-07-13
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# Use Twilio for SMS delivery

# Context

Order notifications need opt-in transactional SMS without coupling checkout to
a second provider. The existing asynchronous notification boundary, retry
policy, and per-channel idempotency record must remain authoritative.

# Decision

Use Twilio through an ExternalService and owned `messages` Operation. Keep
provider invocation inside SVC-notifications after preference and idempotency
checks, so checkout and CHAN-order-created remain unchanged.

# Alternatives

* SendGrid SMS was rejected because the existing account and contract cover
  email only.
* Direct carrier integrations were rejected because their operational and
  compliance cost is disproportionate to the first transactional use case.
* Push notifications were rejected because most shoppers do not have the app.

# Consequences

The team owns Twilio credentials, delivery telemetry, error mapping, and
provider fallback behavior. SMS delivery can fail independently without
blocking checkout. A future provider change remains isolated behind the same
service boundary.

# Affected concepts

* [FEAT-order-notifications](../features/FEAT-order-notifications/overview.md)
* [SVC-notifications](../services/SVC-notifications/overview.md)
* [SUB-order-created](../services/SVC-notifications/SUB-order-created.md)
* [EXT-twilio](../externals/EXT-twilio/overview.md)
* [OP-messages-create](../externals/EXT-twilio/OP-messages-create.md)
