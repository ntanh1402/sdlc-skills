# Run plan: sdlc-write-stories, FEAT-gift-cards
Intent approved 2026-10-05 · Design approved 2026-10-05

## Answers
1. The target is `FEAT-gift-cards`, `ReqApproved`. `REQ-gift-cards-redeem-at-checkout` and `REQ-gift-cards-reject-invalid` need a story; the Constraint and the Nonfunctional Requirement are left to the Tasks.
2. `STORY-gift-cards-pay-with-card`, priority P1: as a customer, I want to pay with my gift card balance, so that I can use the card I was given. Criteria: a balance of 50.00 pays an order of 30.00 and keeps 20.00; a balance of 10.00 pays 10.00 of an order of 30.00 and the customer pays 20.00 another way. Lists `REQ-gift-cards-redeem-at-checkout`.
3. `STORY-gift-cards-refused-card`, priority P1: as a customer, I want to be told when my gift card cannot pay, so that I can pay another way. Criteria: an expired card and an unknown card are each refused with the reason, and the order total is unchanged. Lists `REQ-gift-cards-reject-invalid`.
4. Nothing else in the wiki changes.

## Files
- [ ] features/FEAT-gift-cards/STORY-gift-cards-pay-with-card.md (add: pay with a balance)
- [ ] features/FEAT-gift-cards/STORY-gift-cards-refused-card.md (add: a refused card)
- [ ] features/FEAT-gift-cards/log.md (change)
