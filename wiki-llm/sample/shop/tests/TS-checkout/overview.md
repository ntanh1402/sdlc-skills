---
type: TestSuite
title: Checkout E2E Suite
description: End-to-end tests for the browse-to-order journey.
resource: https://github.com/acme/e2e-tests/tree/main/checkout
status: Implemented
suiteType: e2e
framework: playwright
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Checkout E2E Suite

Drives a real browser against a full stack with Stripe in test mode: log in, add
to cart, check out, and land on the confirmation page. Payment uses Stripe's test
tokens (`tok_visa`, `tok_chargeDeclined`), so the authorize path is exercised for
real, not stubbed.

# Verifies

* [FEAT-checkout](../../features/FEAT-checkout/overview.md) — the whole purchase journey.
