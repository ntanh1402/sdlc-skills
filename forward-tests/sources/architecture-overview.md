# Shop architecture overview

Written by the platform team. Last reviewed 2026-03-10.

## The system

![The shop's services and how they connect](architecture-overview.svg)

The shop takes orders and payments with two services.

- The **orders service** owns the order lifecycle. It builds an order from a
  customer's cart, asks the payments service to authorize the payment, and
  only then confirms the order and announces it on the `order.created` topic.
- The **payments service** talks to Stripe. It authorizes a payment during
  checkout and captures it when the order ships.

Both services share one PostgreSQL database. The web storefront calls the
orders service; nothing but the orders service calls the payments service.
Everything optional to a purchase, such as the confirmation email, happens
after the `order.created` event, so that it can never fail a purchase.

## Decisions

### Charge at checkout (2025-02-03, replaced)

We first captured the full amount inside the checkout request. It was simple,
but a customer was charged for an order that could still fail to ship, and
every such failure became a refund. Replaced by the next decision.

### Authorize at checkout, capture at fulfilment (2025-09-18)

The orders service has the payments service authorize the amount before it
confirms an order; the payments service captures it when the order ships.

We considered keeping the charge at checkout and refunding failures (rejected:
refunds cost a fee and take days to reach the customer) and charging only at
shipping with no authorization (rejected: an order could be confirmed that
can never be paid).

It means an authorization can expire before an order ships, so the payments
service must re-authorize orders older than seven days. This replaces "Charge
at checkout".

## Rules we follow

- An endpoint that creates an order or moves money takes a client token and
  returns the first result on a retry.
- A service writes only its own tables.
- Card data never reaches our services; only Stripe tokens do.

## Terms

| Term | Meaning |
|---|---|
| Order | A purchase created from a cart. It is `pending_payment` until payment is authorized, then `confirmed` |
| Authorization | Stripe's promise to pay an amount |
| Capture | Collecting an authorized amount, when the order ships |
| Client token | A value the client sends with checkout so that a retry returns the first order |

| Role | Who |
|---|---|
| shopper | A logged-in customer acting on their own cart and orders |

## Planned

A loyalty points service will award points for each confirmed order. It is
not built yet.
