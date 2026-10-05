---
type: Cache
title: Session Cache
description: Redis store for login sessions and the auth token lookup.
status: Active
engine: redis
version: "7"
keyPattern: session:{token}
dataType: hash
evictionPolicy: volatile-ttl
ttlSeconds: 86400
maxMemory: 2gb
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Session Cache

Redis holding one hash per active login session, keyed by the opaque session
token the client presents. It is the **authority for whether a token is valid** —
there is no session row in Postgres. A session simply expiring from Redis *is* a
logout; the 24-hour TTL is the maximum session length.

Losing this cache logs everyone out but loses no durable data: accounts,
passwords, and orders all live in [DB-shop](../DB-shop/overview.md).
That is the deliberate trade — sessions are cheap to rebuild by re-login, so they
never touch the primary database.

# Value

| Field | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | string (uuid) | yes | who the token belongs to |
| `issued_at` | string (ISO 8601) | yes | when the session started |
| `scopes` | string | yes | space-separated permission scopes |

# Caches

* [EP-accounts-login](../../services/SVC-accounts/EP-accounts-login.md) — writes the session on a successful login.
* [EP-accounts-me](../../services/SVC-accounts/EP-accounts-me.md) — reads the session to authenticate every account request.
* [EP-cart-get](../../services/SVC-cart/EP-cart-get.md) — reads the session to resolve the caller's customer.

# Used by

* [Accounts Service](../../services/SVC-accounts/overview.md) — rw
* [Cart Service](../../services/SVC-cart/overview.md) — read
