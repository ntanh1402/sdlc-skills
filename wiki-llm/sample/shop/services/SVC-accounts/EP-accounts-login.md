---
type: Endpoint
title: Log in
description: POST /accounts/login — exchange credentials for a session.
status: Active
method: POST
path: /accounts/login
protocol: http
authType: none
rateLimit: 5/min per account
idempotent: false
version: "5"
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Log in

`POST /accounts/login`, exposed by
[SVC-accounts](overview.md). Verifies credentials and
returns a session token, which it writes into
[CACHE-session](../../datastores/CACHE-session/overview.md). Satisfies
[REQ-accounts-login-session](../../features/FEAT-accounts/overview.md#req-accounts-login-session).

# Request

| Field | Location | Type | Required | Description |
|---|---|---|---|---|
| `email` | body | string | yes | Account email. |
| `password` | body | string | yes | Account password. |

# Response

| Field | Status | Type | Required | Description |
|---|---|---|---|---|
| `token` | 200 | string | yes | Opaque session token. |
| `expiresIn` | 200 | integer | yes | Session lifetime in seconds. |

Responses `401` and `429` have no response body.

## Status codes

| Code | When |
|---|---|
| 200 | authenticated; token returned |
| 401 | bad credentials (indistinguishable for unknown email vs wrong password) |
| 429 | too many attempts for this account |

# Behavior

Verifies the Argon2id hash and, on success, writes a session hash to
[CACHE-session](../../datastores/CACHE-session/overview.md) with a 24-hour TTL. A
bad email and a bad password return the **same** `401` and take the same time —
no user enumeration. Login is rate-limited per account (5/min) to blunt
credential-stuffing.

# Sequence diagram

```mermaid
sequenceDiagram
    actor Caller
    participant Accounts as SVC-accounts
    participant Customers as TBL-customers
    participant Sessions as CACHE-session

    Caller->>Accounts: POST /accounts/login
    Accounts->>Accounts: Check per-account rate limit
    alt Rate limit exceeded
        Accounts-->>Caller: 429 Too Many Requests
    else Attempt allowed
        Accounts->>Customers: Read customer and password hash by email
        Accounts->>Accounts: Verify Argon2id hash with constant-time behavior
        alt Unknown email or wrong password
            Accounts-->>Caller: 401 Unauthorized
        else Credentials valid
            Accounts->>Sessions: Write session hash with 24-hour TTL
            Sessions-->>Accounts: Stored
            Accounts-->>Caller: 200 token, expiresIn
        end
    end
```
