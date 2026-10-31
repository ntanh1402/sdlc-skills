---
type: ChangeRequest
title: Card provider checks gift cards
description: Leave refusing invalid gift cards to the card provider.
status: ReqApproved
changeType: refactor
riskLevel: low
priority: P2
requestedBy: payments
generated: { by: human:sample-author, at: 2026-10-03T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-03T09:00:00Z }
version: 1
versionDate: 2026-10-03
---

# Card provider checks gift cards

# Changes

* [FEAT-gift-cards](../../features/FEAT-gift-cards/overview.md)

# Reason

The gift card provider now refuses unknown, expired and empty cards itself,
with its own message, so the shop's own check duplicates it. Rejected
alternative: keeping both checks.

# Requirements

None.

# Delta

None — pending architecture

# References

* [REF-gift-cards-provider-checks-change-prd](../../references/REF-gift-cards-provider-checks-change-prd/overview.md) — the PRD this ChangeRequest was written from.
