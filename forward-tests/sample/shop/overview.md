---
type: Application
title: Shop Platform
description: Top-level application container for the shop.
status: Active
appType: platform
ownerTeam: payments
criticality: tier-0
resource: https://github.com/acme/shop
generated: { by: human:sample-author, at: 2026-06-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-06-01T09:00:00Z }
---

# Shop Platform

The customer-facing shop. Customers register and log in
([accounts](features/FEAT-accounts/overview.md)), browse and search a
catalog ([catalog](features/FEAT-catalog/overview.md)), fill a cart
([cart](features/FEAT-cart/overview.md)), and check out
([checkout](features/FEAT-checkout/overview.md)) — which takes payment
([payments](features/FEAT-payments/overview.md)) and, on success, publishes
an order event that drives customer
[notifications](features/FEAT-order-notifications/overview.md).

Web and mobile frontends call seven services over one Postgres database, a Redis
session cache, a Redis catalog cache, an S3 image bucket, and an OpenSearch
index; three Kafka topics carry the async seams. The load-bearing rule
throughout: **the event boundary decouples the money path from everything
optional** — a notification or search-index outage can never fail a purchase,
and only a Stripe outage can.

# Architecture

Two frontends call seven services. Synchronous calls are solid arrows; the three
Kafka topics are dashed. Every API service shares one PostgreSQL schema.

```mermaid
flowchart LR
  Web[WEB-storefront] --> Accounts[SVC-accounts]
  Web --> Catalog[SVC-catalog]
  Web --> Cart[SVC-cart]
  Web --> Orders[SVC-orders]
  Mobile[MB-shop] --> Accounts
  Mobile --> Catalog
  Mobile --> Cart
  Mobile --> Orders
  Orders --> Payments[SVC-payments]
  Payments --> Stripe[EXT-stripe]
  Orders -. order.created .-> Notifications[SVC-notifications]
  Payments -. payment.authorized .-> Notifications
  Catalog -. product.updated .-> Indexer[SVC-search-indexer]
  Notifications --> SendGrid[EXT-sendgrid]
  Notifications --> Twilio[EXT-twilio]
  Accounts --> Sessions[(CACHE-session)]
  Cart --> Sessions
  Catalog --> CatalogCache[(CACHE-catalog)]
  Catalog --> Images[(BLOB-product-images)]
  Catalog --> Search[(IDX-products)]
  Indexer --> Search
  Accounts --> Database[(DB-shop)]
  Catalog --> Database
  Cart --> Database
  Orders --> Database
  Payments --> Database
  Notifications --> Database
  Indexer --> Database
```
