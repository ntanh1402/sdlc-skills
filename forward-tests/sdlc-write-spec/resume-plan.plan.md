# Run plan: sdlc-write-spec, FEAT-gift-cards
Intent approved 2026-10-03 · Design approved 2026-10-03

## Answers
1. Application `shop`; a new Feature `FEAT-gift-cards`, owner team checkout, priority P1.
2. A customer pays part or all of an order with a gift card balance; the rest goes to the card on file.
3. A gift card has a 16-character code and a balance in the order currency; a balance never goes below zero.
4. Buying or issuing gift cards is out of scope; cards are issued by support.
5. Three Requirements, all Must, functional, verified by test: redeem at checkout; reject an unknown or empty card with a message; show the remaining balance after payment.
6. Success measure: 5% of orders use a gift card within a quarter.
7. The requirements are approved for design (`ReqApproved`).
8. Nothing else in the wiki changes.

## Assumed
- One gift card per order.

## Files
- [ ] features/FEAT-gift-cards/overview.md (add: three Requirements, status ReqApproved, # Architecture None, # References the PRD)
- [ ] features/FEAT-gift-cards/log.md (add)
- [ ] references/REF-gift-cards-prd/overview.md (add: the summary)
- [x] references/REF-gift-cards-prd/prd.md (add: the PRD)
- [ ] references/REF-gift-cards-prd/log.md (add)
