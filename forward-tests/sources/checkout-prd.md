# Checkout: product requirements

Owner: the payments team. Version of 2025-11-20.

## Objective

A shopper turns the cart into a paid order in one step, and is never charged
twice or charged for an order that was not created.

## Users

A logged-in shopper with at least one item in the cart.

## Requirements

1. **Complete a purchase.** A shopper submits the cart with a payment method
   and gets an order confirmation with the order's number. Must have.
2. **Pay before confirming.** The payment is authorized before the order is
   confirmed. A declined payment leaves the order unconfirmed and the cart as
   it was. Must have.
3. **One order per checkout.** Submitting the same checkout again, for example
   after a double click or a lost connection, returns the first order. It
   never creates a second order or a second charge. Must have.
4. **Gift note.** A shopper may add a note of up to 200 characters that is
   printed on the packing slip. Should have.
5. **Saved cards.** A shopper may pay with a card saved on an earlier order,
   without typing it again. Should have.

## Out of scope

Guest checkout, and paying with more than one payment method.

## Success measure

Fewer than 1 in 10,000 checkouts ends with two orders or two charges.
