---
type: Feature
title: Order notes
description: Let support attach a note to an order and read it back.
status: Approved
ownerTeam: checkout
priority: P3
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
version: 1
versionDate: 2026-10-01
designBasedOn: { version: 1, at: 2026-10-01 }
---

# Order notes

Support attaches a short note to an order ("customer asked for a call before
delivery") and reads it later. Owned by `checkout`. Part of the
[Shop Platform](../../overview.md).

# Requirements

### REQ-order-notes-add

**Should** — Support can attach one note of 1 to 500 characters to an order;
a second note replaces the first. Functional. Verified by test.

### REQ-order-notes-read

**Should** — Support can read the note of an order; an order with no note
answers 404. Functional. Verified by test.

# Architecture

Approved target state.

## Context and constraints

Both operations belong to the orders service, which owns the order. No new
service and no new store: the note is a column of the orders table.

## High-level architecture

```mermaid
flowchart LR
  Support --> Orders[SVC-orders]
  Orders --> OrderRows[TBL-orders]
```

## Services

* [SVC-orders](../../services/SVC-orders/overview.md) — gains two endpoints for the note.

## Runtime sequences

```mermaid
sequenceDiagram
  participant Support
  participant Orders as SVC-orders
  Support->>Orders: PUT /orders/{id}/note
  Orders-->>Support: 204
  Support->>Orders: GET /orders/{id}/note
  alt no note
    Orders-->>Support: 404
  else note present
    Orders-->>Support: 200 note
  end
```

## Decisions

None.

## Traceability

| Requirement | Target concepts |
|---|---|
| [REQ-order-notes-add](#req-order-notes-add) | [EP-orders-note-put](../../services/SVC-orders/EP-orders-note-put.md), [TBL-orders](../../datastores/DB-shop/TBL-orders.md) |
| [REQ-order-notes-read](#req-order-notes-read) | [EP-orders-note-get](../../services/SVC-orders/EP-orders-note-get.md) |
