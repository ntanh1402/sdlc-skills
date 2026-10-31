---
type: Task
title: Build the endpoint that reads a note
description: Add GET /orders/{id}/note to the orders service.
status: Todo
taskType: dev
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
basedOn: { version: 1, at: 2026-10-01 }
---

# Build the endpoint that reads a note

# Acceptance

- `GET /orders/{id}/note` returns 200 with the note's `text`.
- An order with no note, or an unknown order, returns 404.

Satisfies [REQ-order-notes-read](overview.md#req-order-notes-read).

# Planned scope

* [EP-orders-note-get](../../services/SVC-orders/EP-orders-note-get.md) — new — the endpoint.

# Blocked by

* [TASK-order-note-put](TASK-order-note-put.md) — the note must be stored before it can be read.
