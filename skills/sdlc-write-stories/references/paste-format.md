# Paste-ready story

A person copies a story from the wiki into the tracker by hand. Print each
story as plain Markdown that pastes cleanly: no frontmatter, no wiki links
(they do not resolve outside the wiki), Requirement keys as plain text. The
copy is printed in the chat and never written to the wiki.

Print one block per story, separated by a line `---`:

```markdown
## Pay with a gift card

As a **customer**, I want to pay with my gift card balance, so that I can use
the card I was given.

**Acceptance criteria**

1. **Given** a card with a balance of 50, **when** the customer pays an order
   of 30 with it, **then** the order is paid and the card keeps 20.
   (REQ-gift-cards-redeem-at-checkout)
2. **Given** a card with a balance of 10, **when** the customer pays an order
   of 30, **then** they pay the other 20 by another method.
   (REQ-gift-cards-split-payment)

**Notes**: A card is entered by its 16-digit number; scanning is out of scope.

Priority: P1 · Wiki: `shop/features/FEAT-gift-cards/STORY-gift-cards-pay-with-card.md`
```

- The heading is the story's `title`; the sentence and criteria are copied
  as written, with each link replaced by its key.
- Leave out the Notes line when the story has no `# Notes`, and `Priority`
  when it has no `priority`.
- The wiki path is relative to the wiki's `wiki/` folder, so the ticket
  leads back to the story. When the story already has a `trackerKey`, add
  `· Ticket: <trackerKey>`.
