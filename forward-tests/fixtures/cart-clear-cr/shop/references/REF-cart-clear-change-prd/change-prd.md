# Clear the cart PRD

## Target Feature

FEAT-cart.

## Reason

Removing items one by one is slow for customers who change their mind.

## Before and after

Before: one item at a time. After: one action removes all items.

## Changed flow

The cart page offers "Clear cart"; after confirming, the cart is empty.

## Changed and regression requirements

Adds REQ-cart-clear-all. Prices fixed on add are unaffected.

## Impact hypothesis

Fewer abandoned carts with stale items.

## Risk

Low: one service, reversible.

## Acceptance

See the Requirements in the ChangeRequest.

## Constraints and compatibility

The existing remove-item behaviour stays.

## Assumptions and open questions

None.

## Out of scope

Undoing a clear.
