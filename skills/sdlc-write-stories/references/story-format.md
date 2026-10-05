# Story format

A story is one file in its parent's folder:
`wiki/<app>/features/FEAT-<name>/STORY-<feature-name>-<name>.md` or
`wiki/<app>/change-requests/CR-<name>/STORY-<feature-name>-<name>.md`, where
`<feature-name>` is the Feature key without `FEAT-` (the changed Feature's,
for a ChangeRequest). Read `.wiki-llm/schema/user-story.md` for the rules.

## In a Feature's folder

```markdown
---
type: UserStory
title: Pay with a gift card
description: A customer pays part or all of an order with a gift card.
priority: P1
---

# Pay with a gift card

As a **customer**, I want to pay with my gift card balance, so that I can use
the card I was given.

# Acceptance criteria

1. **Given** a card with a balance of 50, **when** the customer pays an order
   of 30 with it, **then** the order is paid and the card keeps 20.
   ([REQ-gift-cards-redeem-at-checkout](overview.md#req-gift-cards-redeem-at-checkout))
2. **Given** a card with a balance of 10, **when** the customer pays an order
   of 30, **then** they pay the other 20 by another method.
   ([REQ-gift-cards-split-payment](overview.md#req-gift-cards-split-payment))

# Requirements

* [REQ-gift-cards-redeem-at-checkout](overview.md#req-gift-cards-redeem-at-checkout)
* [REQ-gift-cards-split-payment](overview.md#req-gift-cards-split-payment)

# Notes

A card is entered by its 16-digit number; scanning is out of scope.
```

## In a ChangeRequest's folder

```markdown
---
type: UserStory
title: Pay with an expired gift card balance
description: A customer learns that an expired card cannot pay.
---

# Pay with an expired gift card balance

As a **customer**, I want to be told when my gift card has expired, so that
I can pay another way before I lose my cart.

# Acceptance criteria

1. **Given** a card that expired yesterday with a balance of 50, **when** the
   customer pays with it, **then** checkout says the card has expired and
   offers the other payment methods.
   ([REQ-gift-cards-expiry](overview.md#req-gift-cards-expiry))

# Requirements

* [REQ-gift-cards-expiry](overview.md#req-gift-cards-expiry)

# Affects

* [STORY-gift-cards-pay-with-card](../../features/FEAT-gift-cards/STORY-gift-cards-pay-with-card.md) — an expired card no longer pays.
```

- `# Requirements` links the `overview.md` of the story's own folder. In a
  ChangeRequest, that is the ChangeRequest's copy, never the Feature's.
- Leave out `trackerKey` and `resource`; a person adds them after making the
  ticket. Leave out `# Notes` and `# Affects` when they have nothing to say.
- `generated` and `verified` are written by `draft finish`; `# Changed by`
  and `index.md` by the tool.
