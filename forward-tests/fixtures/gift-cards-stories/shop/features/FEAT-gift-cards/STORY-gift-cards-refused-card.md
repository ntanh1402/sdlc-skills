---
type: UserStory
title: Learn why a gift card is refused
description: A customer whose gift card cannot pay sees why and keeps the order total.
priority: P1
generated: { by: human:sample-author, at: 2026-10-02T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-02T09:00:00Z }
basedOn: { version: 1, at: 2026-10-01 }
---

# Learn why a gift card is refused

As a **customer**, I want to be told when my gift card cannot pay, so that I
can pay another way.

# Acceptance criteria

1. **Given** a card that expired yesterday, **when** the customer enters it at
   checkout, **then** checkout says it has expired and the order total is
   unchanged.
   ([REQ-gift-cards-reject-invalid](overview.md#req-gift-cards-reject-invalid))
2. **Given** a card number that does not exist, **when** the customer enters
   it, **then** checkout says the card is unknown and the order total is
   unchanged.
   ([REQ-gift-cards-reject-invalid](overview.md#req-gift-cards-reject-invalid))

# Requirements

* [REQ-gift-cards-reject-invalid](overview.md#req-gift-cards-reject-invalid)
