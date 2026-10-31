# Validate the delivery address at checkout PRD

## Target Feature

FEAT-checkout.

## Reason

Undeliverable addresses cause returned parcels; operations wants them caught when the order is created. Rejected alternative: checking after the order.

## Before and after

Before: any address is accepted when the order is created. After: the order-creation request checks the address and refuses an undeliverable one.

## Changed flow

See Before and after.

## Changed and regression requirements

Adds REQ-checkout-deliverable-address.

## Impact hypothesis

See Reason.

## Risk

Med.

## Acceptance

See the Requirements in the ChangeRequest.

## Constraints and compatibility

None beyond the Feature's existing Requirements.

## Assumptions and open questions

None.

## Out of scope

Anything not in Before and after.
