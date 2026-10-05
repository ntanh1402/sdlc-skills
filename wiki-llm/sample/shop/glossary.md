---
type: Glossary
title: Shop glossary
description: Domain terms and user roles used across the shop bundle.
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
---

# Shop glossary

# Terms

| Term | Definition |
|---|---|
| Cart | The items a customer has collected before checkout, with each price fixed when the item was added. |
| Order | A purchase created from a cart. It is `pending_payment` until payment is authorized, then `confirmed`. |
| Authorization | The payment provider's promise to pay an amount. It must succeed before an order is confirmed. |
| Capture | Collecting an authorized amount, done at fulfilment. |
| Client token | A value the client sends with checkout so a retry returns the first order instead of creating a second. |
| Order event | The `order.created` message published once an order is confirmed. |
| Dead-letter queue | The channel a message goes to after a consumer has used all its retries. |

# Roles

| Role | Description |
|---|---|
| public | Anyone, without logging in. |
| authenticated | A logged-in customer acting on their own account, cart, and orders. |
