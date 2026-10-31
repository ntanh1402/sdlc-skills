# Paste-ready story output

Before the summary of `sdlc-write-stories`, print each story added or changed
in this run as plain Markdown that pastes cleanly into the tracker by hand: no
frontmatter, no wiki links (they do not resolve outside the wiki), Requirement
keys as plain text. This copy is printed in the chat and never written to the
wiki.

Print one block per story, separated by a line `---`:

```markdown
## Pay with a gift card

As a **customer**, I want to pay with my gift card balance, so that I can use
the card I was given.

**Acceptance criteria**

1. A card with a balance of 50 pays an order of 30 in full and keeps a
   balance of 20. (REQ-gift-cards-redeem-at-checkout)
2. A card with a balance of 10 pays 10 of an order of 30, and the customer
   pays the other 20 by another method. (REQ-gift-cards-split-payment)
3. A card never pays more than its balance, and its balance never goes below
   0. (REQ-gift-cards-redeem-at-checkout)

**Notes**: A card is entered by its 16-digit number; scanning is out of scope.

Priority: P1 · Wiki: `shop/features/FEAT-gift-cards/STORY-gift-cards-pay-with-card.md`
```

- The heading is the story's `title`; the sentence and criteria are copied
  as written, with each link replaced by its key.
- Leave out the Notes line when the story has no `# Notes`, and `Priority`
  when it has no `priority`.
- The wiki path is relative to the wiki's `wiki/` folder, so the ticket
  leads back to the story and to its `# Test cases`. When a revised story
  already has a `trackerKey`, add `· Ticket: <trackerKey>`.
