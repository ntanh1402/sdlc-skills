---
type: Task
title: Record who refunded an order
description: Write an audit line for every refund.
status: Todo
taskType: dev
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
basedOn: { version: 1, at: 2026-10-01 }
---

# Record who refunded an order

# Acceptance

Every successful refund writes the support agent's id and the reason to the
audit log.

# Planned scope

* [EP-orders-refund](../../services/SVC-orders/EP-orders-refund.md) — new — the audit line.
