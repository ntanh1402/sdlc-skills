---
type: TestCase
title: Redelivery is idempotent
description: Prove broker redelivery cannot duplicate customer contact.
risk: critical
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# Redelivery is idempotent

# Covers

* [REQ-order-notifications-failure-never-blocks](../../features/FEAT-order-notifications/overview.md#req-order-notifications-failure-never-blocks)

# Purpose

Prove broker redelivery cannot duplicate customer contact.

# Preconditions

Customer allows email; provider/table captures are empty.

# Test data

Two deliveries with identical event and message IDs.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Publish first delivery | Message is sent and recorded | One provider call and one row exist |
| 2 | Redeliver same message | Duplicate is acknowledged without sending | Provider/row counts remain one and broker sees no error |

# Postconditions and cleanup

Delete row and reset broker/provider fixtures.
