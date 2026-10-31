---
type: Service
title: Payments Service
description: Authorizes and captures card payments via Stripe.
resource: https://github.com/acme/payments-service
status: Active
serviceType: api
ownerTeam: payments
language: java
framework: spring-boot
runtime: jdk21
deployTarget: k8s
slaTier: tier-0
version: "4.0.2"
port: 8080
healthcheckPath: /actuator/health
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Payments Service

The money boundary. It authorizes a charge during checkout and captures it at
fulfilment, talking to [EXT-stripe](../../externals/EXT-stripe/overview.md) and
recording every attempt in [payments](../../datastores/DB-shop/TBL-payments.md).
No card data ever lands here — the browser tokenizes the card with Stripe, and
this service only handles the resulting token and intent id.

It is `tier-0`: a checkout cannot complete without it, and unlike notifications
there is no degrade-and-continue path. On a successful authorization it publishes
[CHAN-payment-authorized](../../channels/CHAN-payment-authorized/overview.md) so
finance and the receipt email can react without coupling to checkout.

# Publishes

* [CHAN-payment-authorized](../../channels/CHAN-payment-authorized/overview.md) — emitted after an authorization is stored.

# Calls

* [OP-payment-intents-create](../../externals/EXT-stripe/OP-payment-intents-create.md) — authorizes a charge. Stripe is the payment rail: its outage stops checkout and there is no fallback provider.
* [OP-payment-intents-capture](../../externals/EXT-stripe/OP-payment-intents-capture.md) — captures an authorized charge at fulfilment.

# Writes

* [TBL-payments](../../datastores/DB-shop/TBL-payments.md) — one row per authorization attempt.

