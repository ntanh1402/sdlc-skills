# Resubmitted checkout places a new order PRD

## Target Feature

FEAT-checkout.

## Reason

Sales wants a customer who presses "Place order" twice to get two orders, for quick repeat purchases. Rejected alternative: a separate "buy again" button.

## Before and after

Before: a retried checkout returns the first order. After: every submission creates an order.

## Changed flow

See Before and after.

## Changed and regression requirements

Adds REQ-checkout-resubmit-new-order.

## Impact hypothesis

See Reason.

## Risk

High.

## Acceptance

See the Requirements in the ChangeRequest.

## Constraints and compatibility

None beyond the Feature's existing Requirements.

## Assumptions and open questions

None.

## Out of scope

Anything not in Before and after.
