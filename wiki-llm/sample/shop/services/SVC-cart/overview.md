---
type: Service
title: Cart Service
description: Manages the customer's shopping cart until checkout.
resource: https://github.com/acme/cart-service
status: Active
serviceType: api
ownerTeam: checkout
language: typescript
framework: fastify
runtime: node20
deployTarget: k8s
slaTier: tier-1
version: "2.1.0"
port: 8080
healthcheckPath: /healthz
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Cart Service

Owns the shopping cart: add, change quantity, remove, and read the cart the
checkout will turn into an order. Every request is authenticated by resolving the
session token against
[CACHE-session](../../datastores/CACHE-session/overview.md); the cart belongs to
the customer that token identifies.

When an item is added, the service snapshots the current price from
[products](../../datastores/DB-shop/TBL-products.md) into the cart line, so a later
price change does not silently re-price a shopper mid-visit — the pricing
decision is made once, at add time.

# Reads

* [TBL-products](../../datastores/DB-shop/TBL-products.md) — price and stock at add time.

# Writes

* [TBL-carts](../../datastores/DB-shop/TBL-carts.md) — the open cart per customer.
* [TBL-cart_items](../../datastores/DB-shop/TBL-cart-items.md) — the cart lines.

# Uses

* [CACHE-session](../../datastores/CACHE-session/overview.md) — read — resolves the caller's session to a customer.
