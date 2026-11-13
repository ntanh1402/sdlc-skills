# Run plan: sdlc-design-arch, CR-checkout-address-validation
Intent approved 2026-10-03 · Design approved 2026-10-03

## Answers
1. The target is `CR-checkout-address-validation` on `FEAT-checkout`, `ReqApproved`.
2. The address is checked inside `SVC-orders`, in the order-creation request, before the payment is authorized. No new service and no external address vendor: the rule is a list of postal codes the shop cannot deliver to, kept in the service's configuration.
3. `EP-orders-create` is the only concept that changes: `modified`. An undeliverable address is refused with `422` and the body field `reason` set to `address_undeliverable`; no order row is written and no payment is authorized.
4. No new decision: `ADR-idempotent-checkout` still holds, and a refused request stores no idempotency result.
5. Downstream: `TASK-order-creation-endpoint` is `Done`; `TS-checkout` lacks a case for the refusal. Neither is edited here.
6. Nothing else in the wiki changes.

## Assumed
- The list of postal codes is configuration, not a table, so no Table is added.

## Files
- [ ] change-requests/CR-checkout-address-validation/overview.md (change: # Delta filled, one sequence with the 422 branch, traceability; status Approved)
- [ ] features/FEAT-checkout/overview.md (change: REQ-checkout-deliverable-address added; # Architecture names the address check in the order-creation sequence)
- [ ] services/SVC-orders/EP-orders-create.md (change: 422 `address_undeliverable`; behaviour step before the payment; status Modifying; pending entry)
- [ ] change-requests/CR-checkout-address-validation/log.md (change)
- [ ] features/FEAT-checkout/log.md (change)
- [ ] services/SVC-orders/log.md (change)

## For other skills
- TS-checkout has no case for an undeliverable address: sdlc-design-story-tests
- The change to EP-orders-create has no Task: sdlc-plan-tasks
