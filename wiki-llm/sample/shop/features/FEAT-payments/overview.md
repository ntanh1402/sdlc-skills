---
type: Feature
title: Payments
description: Take card payment for an order without touching card data.
status: Released
ownerTeam: payments
priority: P0
targetRelease: "2026.4"
releasedAt: 2026-04-15T00:00:00Z
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
sources:
  - id: payments-prd
    resource: https://acme.atlassian.net/wiki/spaces/SHOP/pages/12480
    title: Payments PRD
  - id: pci-dss-saq-a-scope-note
    resource: https://acme.atlassian.net/wiki/spaces/SEC/pages/9001
    title: PCI-DSS SAQ-A scope note
---

# Payments

Charge the customer's card during checkout, and capture the charge when the order
ships — all without card data ever entering the platform. Owned by `payments`.
Part of the [Shop Platform](../../overview.md).

# Requirements

### REQ-payments-no-card-data

**Must** — Card details never reach the platform; only a provider token is
handled. Constraint. Verified by inspection.

### REQ-payments-authorize-once

**Must** — A charge is authorized during checkout, and a retried checkout never
double-charges. Functional. Verified by test.

### REQ-payments-capture-at-fulfilment

**Should** — A charge is captured only at fulfilment; a cancelled order releases
the authorization. Functional. Verified by test.

# Architecture

Approved target state.

## Context and constraints

Card details never enter application services. `order_id` is the idempotency key
and Stripe failures must map to stable internal outcomes.

## High-level architecture

```mermaid
flowchart LR
  Browser --> Stripe[EXT-stripe]
  Orders[SVC-orders] --> Payments[SVC-payments]
  Payments --> Stripe
  Payments --> PaymentTable[TBL-payments]
  Payments --> Authorized[CHAN-payment-authorized]
```

## Services

* [SVC-payments](../../services/SVC-payments/overview.md) — authorizes and captures through Stripe.
* [SVC-orders](../../services/SVC-orders/overview.md) — requests authorization during checkout.

## Runtime sequences

```mermaid
sequenceDiagram
  participant Orders as SVC-orders
  participant Payments as SVC-payments
  participant Stripe as EXT-stripe
  participant DB as TBL-payments
  participant Events as CHAN-payment-authorized
  Orders->>Payments: authorize(order_id, token, amount)
  Payments->>DB: reserve idempotency record
  Payments->>Stripe: create/confirm PaymentIntent
  alt authorized
    Stripe-->>Payments: authorized
    Payments->>DB: record authorization
    Payments->>Events: publish payment.authorized
    Payments-->>Orders: authorization
  else declined or unavailable
    Stripe-->>Payments: failure
    Payments->>DB: record terminal/retryable outcome
    Payments-->>Orders: mapped failure
  end
```

## Decisions

None recorded.

## Traceability

| Requirement | Target concepts |
|---|---|
| [REQ-payments-no-card-data](#req-payments-no-card-data) | [SVC-payments](../../services/SVC-payments/overview.md), [EXT-stripe](../../externals/EXT-stripe/overview.md) |
| [REQ-payments-authorize-once](#req-payments-authorize-once) | [TBL-payments](../../datastores/DB-shop/TBL-payments.md), [CHAN-payment-authorized](../../channels/CHAN-payment-authorized/overview.md) |
| [REQ-payments-capture-at-fulfilment](#req-payments-capture-at-fulfilment) | [SVC-payments](../../services/SVC-payments/overview.md), [SVC-orders](../../services/SVC-orders/overview.md) |

# Change history

None
