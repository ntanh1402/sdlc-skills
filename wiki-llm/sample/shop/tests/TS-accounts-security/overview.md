---
type: TestSuite
title: Accounts Security Suite
description: Security tests for hashing, rate limiting, and enumeration.
resource: https://github.com/acme/accounts-service/tree/main/tests/security
status: Implemented
suiteType: security
framework: pytest
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Accounts Security Suite

Adversarial tests for the auth surface: password storage, login rate limiting,
account enumeration, and session expiry. These assert the non-functional
guarantees of [REQ-accounts-credential-safety](../../features/FEAT-accounts/overview.md#req-accounts-credential-safety), which a
functional test would pass while still being insecure.

# Verifies

* [FEAT-accounts](../../features/FEAT-accounts/overview.md) — registration, login, sessions.
