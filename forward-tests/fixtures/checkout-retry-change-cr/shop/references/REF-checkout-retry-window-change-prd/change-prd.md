# Retry window for checkout PRD

## Objective

A shopper who retries a checkout, now or the next day, is charged once and
gets one order. A shopper whose payment is slow is told it is in progress.

## Changes

- `REQ-checkout-pay-before-confirm` changes: the protection against a second
  order or charge lasts 24 hours for the same client token, not one session.
- `REQ-checkout-retry-status` is new.

## Out of scope

Retries with a new client token; partial payments.
