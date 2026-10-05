---
type: TestCase
title: Email sent
description: Prove one order event produces one recorded email delivery.
risk: high
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# Email sent

# Covers

* [REQ-order-notifications-confirmation-sent](../../features/FEAT-order-notifications/overview.md#req-order-notifications-confirmation-sent)

# Purpose

Prove one order event produces one recorded email delivery.

# Preconditions

Customer allows email; provider stub and notifications table are empty.

# Test data

One unique `order.created` event and matching customer.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Publish event | Consumer acknowledges within 60 seconds | Broker offset advances for message |
| 2 | Inspect provider | Exactly one email call exists | Stub count and order/customer payload match fixture |
| 3 | Inspect database | One sent email row exists | Row has channel=email and status=sent |

# Postconditions and cleanup

Delete notification row and reset provider stub.
