# Gift cards PRD

## Objective
A customer can pay part or all of an order with a gift card balance; the rest goes to the card on file.

## Users and actors
- Customer paying at checkout.
- Support, who issue gift cards (outside this Feature).

## Problem and evidence
Customers who hold a gift card cannot spend it at checkout. No evidence beyond the owner's request.

## Scope
Redeeming one gift card at checkout, rejecting an unknown or empty card with a message, and showing the remaining balance after payment.

## User and system flow
1. At checkout the customer enters a 16-character gift card code.
2. If the balance covers the order, the whole order is paid from the card; if not, the card pays what it can and the rest goes to the card on file.
3. After payment the customer sees the remaining balance.

Failure: the code matches no card, or the card has no balance. The customer sees a message and nothing is charged to that card.

## Business rules
- A gift card has a 16-character code and a balance in the order currency.
- A balance never goes below zero.
- One gift card per order.

## Functional requirements
- Redeem at checkout: pay part or all of an order with a gift card balance.
- Reject an unknown or empty card with a message.
- Show the remaining balance after payment.

## Nonfunctional requirements
None recorded.

## Data and events
A card's balance is reduced by the amount it paid. The code is a payment credential and is shown only to the customer who entered it.

## Success measures
5% of orders use a gift card within a quarter.

## Acceptance
- An order smaller than the balance is paid from the card and the reduced balance is shown.
- An order larger than the balance is paid in part from the card and in part with the card on file.
- An unknown code and an empty card are each refused with a message and charge nothing.

## Risks and constraints
Balances must never go below zero, including when two orders use one card at once.

## Assumptions and open questions
- Assumed: one gift card per order.

## Out of scope
- Buying or issuing gift cards.
- More than one gift card on one order.
- Expiry, refunds to a card and balance transfers.
