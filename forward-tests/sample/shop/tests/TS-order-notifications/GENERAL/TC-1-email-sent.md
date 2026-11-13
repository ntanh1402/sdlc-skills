---
type: TestCase
title: Email sent
description: Prove one order event produces one recorded email delivery.
risk: high
testType: integration
testCategory: integration
generated: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-13T10:00:00Z }
---

# Email sent

# Covers

* [REQ-order-notifications-confirmation-sent](../../../features/FEAT-order-notifications/overview.md#req-order-notifications-confirmation-sent)

# Purpose

Prove one order event produces one recorded email delivery.

# Preconditions

Customer allows email; provider stub and notifications table are empty.

Data that must exist:

* event: one unique `order.created` event
* customer: the matching customer

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Publish message to topic `order.created` for an order of the customer who allows email | Topic order.created:<br>- Consumer offset: past the message within 60 seconds | Read the consumer group's offset; check **consumer offset** |
| 2 | Read the calls the SendGrid stub received | Operation POST /v3/mail/send:<br>- Calls received: 1<br>- recipient: the customer's email<br>- order id: the message's order id | Read the stub's calls; check **calls received**, **recipient** and **order id** |
| 3 | Query table `notifications` for the order | Table notifications:<br>- Rows found: 1<br>- channel: email<br>- status: sent | Read the rows; check **rows found**, **channel** and **status** |

# Postconditions and cleanup

Delete notification row and reset provider stub.
