---
type: Task
title: Build the endpoint that attaches a note
description: Add PUT /orders/{id}/note to the orders service.
status: Todo
taskType: dev
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
basedOn: { version: 1, at: 2026-10-01 }
---

# Build the endpoint that attaches a note

# Acceptance

- `PUT /orders/{id}/note` with a `text` of 1 to 500 characters stores the note
  and returns 204; a second call replaces the note.
- A `text` that is empty or longer than 500 characters returns 422.
- An unknown order returns 404.

Satisfies [REQ-order-notes-add](overview.md#req-order-notes-add).

# Planned scope

* [EP-orders-note-put](../../services/SVC-orders/EP-orders-note-put.md) — new — the endpoint.
* [TBL-orders](../../datastores/DB-shop/TBL-orders.md) — modified — the column `support_note`.
