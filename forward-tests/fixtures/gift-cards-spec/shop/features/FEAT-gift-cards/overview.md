---
type: Feature
title: Gift cards
description: Let a customer pay for an order with a gift card balance.
status: ReqApproved
ownerTeam: checkout
priority: P1
generated: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-01T09:00:00Z }
version: 1
versionDate: 2026-10-01
---

# Gift cards

Customers pay part or all of an order with the balance of a gift card bought
elsewhere. Owned by `checkout`.

# Requirements

### REQ-gift-cards-redeem-at-checkout

**Must** — A customer can pay part or all of an order with a gift card balance,
and the balance drops by the amount used. Functional. Verified by test.

### REQ-gift-cards-reject-invalid

**Must** — An unknown, expired or empty gift card is refused at checkout and the
order total is unchanged. Functional. Verified by test.

### REQ-gift-cards-single-use-per-order

**Must** — Submitting the same order twice never charges a gift card twice.
Constraint. Verified by test.

### REQ-gift-cards-fast-balance

**Should** — Checking a gift card balance completes within 200 ms at p95 under
the checkout load profile. Nonfunctional. Verified by test.

# Architecture

None

# References

* [REF-gift-cards-prd](../../references/REF-gift-cards-prd/overview.md) — the PRD this Feature was written from.
