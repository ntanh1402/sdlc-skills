---
type: Task
title: Build the accounts service
description: Register, login, and session issuance with Argon2id and rate limits.
resource: https://acme.atlassian.net/browse/SHOP-100
status: Done
trackerKey: SHOP-100
taskType: dev
prUrl: https://github.com/acme/accounts-service/pull/19
mergedAt: 2026-02-28T10:20:00Z
generated: { by: human:sample-author, at: 2026-02-28T10:20:00Z }
verified: { by: human:sample-author, at: 2026-02-28T10:20:00Z }
---

# Build the accounts service

Jira `SHOP-100`. Broken out of
[FEAT-accounts](overview.md).

# Acceptance

Register with Argon2id hashing, log in with a rate limit and a 24-hour session,
and never reveal whether an email exists. Satisfies
[REQ-accounts-register](overview.md#req-accounts-register),
[REQ-accounts-login-session](overview.md#req-accounts-login-session), and
[REQ-accounts-credential-safety](overview.md#req-accounts-credential-safety).

# Planned scope

* [SVC-accounts](../../services/SVC-accounts/overview.md) — new — the service.
* [EP-accounts-register](../../services/SVC-accounts/EP-accounts-register.md) — new — register.
* [EP-accounts-login](../../services/SVC-accounts/EP-accounts-login.md) — new — login.
* [EP-accounts-me](../../services/SVC-accounts/EP-accounts-me.md) — new — profile.
* [CACHE-session](../../datastores/CACHE-session/overview.md) — new — the session store.

This is the **planned** scope. Actual scope is whatever PR #19 touched; the delta
is drift.
