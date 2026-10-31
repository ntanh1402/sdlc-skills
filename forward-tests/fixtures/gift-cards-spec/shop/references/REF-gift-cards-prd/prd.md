# Gift cards PRD

## Objective

Let customers spend gift card balances at checkout, so gift cards sold by
partners turn into orders.

## Users and actors

Shoppers with a gift card code; the gift card issuer, which holds balances.

## Problem and evidence

Partners sell our gift cards, but customers cannot redeem them online; support
redeems them by hand, about 300 a week.

## Scope

Redeem at checkout, partial payment with the rest by card, balance check.

## User and system flow

At checkout the customer enters a code; the balance is shown; the customer
applies it; the rest is paid by card; the order is placed once.

## Business rules

A card may pay part of an order. A card can be used on many orders until its
balance is zero. Expired cards are refused.

## Functional requirements

Redeem, partial payment, refusal of invalid cards.

## Nonfunctional requirements

Balance checks within 200 ms at p95 under the checkout load profile.

## Data and events

The amount redeemed per order; no card numbers are stored in plain text.

## Success measures

80% of partner gift cards redeemed online within three months.

## Acceptance

See the Requirements in the Feature.

## Risks and constraints

Double redemption on retried submissions.

## Assumptions and open questions

The issuer offers a balance and redeem API.

## Out of scope

Selling gift cards; refunds to a gift card.
