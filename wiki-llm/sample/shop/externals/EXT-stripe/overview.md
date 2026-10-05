---
type: ExternalService
title: Stripe
description: Card payment authorization and capture for checkout.
resource: https://stripe.com
status: Active
vendor: Stripe
apiUrl: https://api.stripe.com/v1
authType: apikey
slaTier: critical
costModel: per-call
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Stripe

How this application depends on Stripe: it is the payment rail. The card number
never reaches the shop — the browser tokenizes the card directly with Stripe, and
[SVC-payments](../../services/SVC-payments/overview.md) only ever sends the
resulting token and a `PaymentIntent`. That is what keeps the shop out of
PCI-DSS scope for cardholder data.

# Fallback

**Critical** to [SVC-payments](../../services/SVC-payments/overview.md), and
therefore to [Checkout](../../features/FEAT-checkout/overview.md): unlike email
or SMS, there is no queue-and-retry that lets the order proceed. If Stripe is
down, authorization fails and the order stays `pending_payment` — the customer
sees a "payment could not be processed" error and is asked to try again. There is
no second provider; a Stripe outage is a checkout outage, which is why it is the
one dependency whose health pages on-call.
