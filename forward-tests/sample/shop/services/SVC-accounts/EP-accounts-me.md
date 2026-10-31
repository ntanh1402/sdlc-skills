---
type: Endpoint
title: Get profile
description: GET /accounts/me — the authenticated profile.
status: Active
method: GET
path: /accounts/me
protocol: http
authType: jwt
idempotent: true
version: "5"
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Get profile

`GET /accounts/me`, exposed by
[SVC-accounts](overview.md). Returns the profile of
the session holder. This is the endpoint that turns a token into an identity, so
it is the read path
[CACHE-session](../../datastores/CACHE-session/overview.md) exists to serve.

# Request

| Field | Location | Type | Required | Description |
|---|---|---|---|---|
| `Authorization` | header | bearer token | yes | Session token. |

# Response

| Field | Status | Type | Required | Description |
|---|---|---|---|---|
| `customerId` | 200 | string (uuid) | yes | Authenticated customer. |
| `email` | 200 | string | yes | Customer email. |
| `emailOptOut` | 200 | boolean | yes | Email notification preference. |
| `smsOptOut` | 200 | boolean | yes | SMS notification preference. |

Response `401` has no response body.

## Status codes

| Code | When |
|---|---|
| 200 | profile returned |
| 401 | missing or expired session |

# Validations

| Rule | Fails with |
|---|---|
| `Authorization` carries a session token present in CACHE-session | `401` |

# Behavior

Reads the session from
[CACHE-session](../../datastores/CACHE-session/overview.md); a missing key is an
expired or revoked session and returns `401`. The password hash is **never** in
the response.

# Flowchart

```mermaid
flowchart TD
    A[GET /accounts/me] --> B{Session key in CACHE-session?}
    B -- no --> X401[401]
    B -- yes --> C[Build profile without the password hash]
    C --> X200[200 profile]
```

# Sequence diagram

```mermaid
sequenceDiagram
    actor Caller
    participant Accounts as SVC-accounts
    participant Sessions as CACHE-session
    participant Customers as TBL-customers

    Caller->>Accounts: GET /accounts/me with bearer token
    Accounts->>Sessions: Resolve session token
    alt Session missing or expired
        Sessions-->>Accounts: No active session
        Accounts-->>Caller: 401 Unauthorized
    else Session active
        Sessions-->>Accounts: customerId
        Accounts->>Customers: Read customer profile
        Customers-->>Accounts: Profile without password hash
        Accounts-->>Caller: 200 profile
    end
```
