---
type: TestCase
title: Provider outage does not fail checkout
description: Prove notification outage is isolated from checkout and retried.
risk: critical
testType: integration
testCategory: error-handling
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# Provider outage does not fail checkout

# Covers

* [REQ-order-notifications-failure-never-blocks](../../../features/FEAT-order-notifications/overview.md#req-order-notifications-failure-never-blocks)
* [EP-orders-create](../../../services/SVC-orders/EP-orders-create.md)

# Purpose

Prove notification outage is isolated from checkout and retried.

# Preconditions

SendGrid stub returns 503; notification retry scheduler is active.

Data that must exist:

* checkout: one valid checkout
* event: its resulting order event

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call API `POST /orders` with a valid cart and payment method `tok_visa` | Response POST /orders:<br>- status: 201<br>- order status: confirmed | Read the response; check **status** and **order status** |
| 2 | Let the notifications service consume the resulting message on topic `order.created` while the SendGrid stub returns 503 | Table notifications:<br>- status: pending<br>- attempts: one more after each retry | Query the row after each retry; check **status** and **attempts** |
| 3 | Call API `GET /orders/{id}` with the order id after the retries | Response GET /orders/{id}:<br>- status: 200<br>- order status: confirmed | Read the response; check **status** and **order status** |

# Postconditions and cleanup

Restore provider stub and delete fixtures.
