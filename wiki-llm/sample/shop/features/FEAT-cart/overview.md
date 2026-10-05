---
type: Feature
title: Cart
description: Let a customer collect items before checkout.
status: Released
ownerTeam: checkout
priority: P1
targetRelease: "2026.5"
releasedAt: 2026-05-20T00:00:00Z
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
sources:
  - id: cart-prd
    resource: https://acme.atlassian.net/wiki/spaces/SHOP/pages/12520
    title: Cart PRD
---

# Cart

The bridge between browsing and buying: add items, adjust quantities, and hold
them until checkout turns the cart into an order. Owned by `checkout`. Part of the
[Shop Platform](../../overview.md).

# Requirements

### REQ-cart-view-total

**Must** — A logged-in customer can view their cart with a running total.
Functional. Verified by test.

### REQ-cart-edit-items

**Must** — A customer can add, change the quantity of, and remove items.
Functional. Verified by test.

### REQ-cart-price-fixed-on-add

**Must** — The price of an item is fixed at the moment it is added, and a later
price change does not alter the cart. Constraint. Verified by test.

# Architecture

Approved target state.

## Context and constraints

Cart owns mutable pre-checkout state and snapshots product price when an item is
added. Checkout reads that snapshot without transferring ownership.

## High-level architecture

```mermaid
flowchart LR
  User --> Cart[SVC-cart]
  Cart --> Carts[TBL-carts]
  Cart --> Items[TBL-cart-items]
  Cart --> Products[TBL-products]
  Orders[SVC-orders] --> Carts
```

## Services

* [SVC-cart](../../services/SVC-cart/overview.md) — owns the cart until checkout.
* [SVC-orders](../../services/SVC-orders/overview.md) — reads the cart during checkout.

## Runtime sequences

```mermaid
sequenceDiagram
  actor User
  participant Cart as SVC-cart
  participant Products as TBL-products
  participant Carts as TBL-carts/TBL-cart-items
  User->>Cart: add product
  Cart->>Products: read current price
  Cart->>Carts: persist item and price snapshot
  Carts-->>Cart: saved cart
  Cart-->>User: updated cart
```

## Decisions

None recorded.

## Traceability

| Requirement | Target concepts |
|---|---|
| [REQ-cart-view-total](#req-cart-view-total) | [SVC-cart](../../services/SVC-cart/overview.md), [TBL-carts](../../datastores/DB-shop/TBL-carts.md) |
| [REQ-cart-edit-items](#req-cart-edit-items) | [SVC-cart](../../services/SVC-cart/overview.md), [TBL-cart-items](../../datastores/DB-shop/TBL-cart-items.md) |
| [REQ-cart-price-fixed-on-add](#req-cart-price-fixed-on-add) | [SVC-cart](../../services/SVC-cart/overview.md), [SVC-orders](../../services/SVC-orders/overview.md) |

# Change history

None
