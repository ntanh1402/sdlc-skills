---
type: Endpoint
title: Register account
description: POST /accounts — create an account.
status: Active
method: POST
path: /accounts
protocol: http
authType: none
rateLimit: 10/min per IP
idempotent: false
version: "5"
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Register account

`POST /accounts`, exposed by
[SVC-accounts](overview.md). Creates a customer with
an email and a password. Satisfies
[REQ-accounts-register](../../features/FEAT-accounts/overview.md#req-accounts-register).

# Request

| Field | Location | Type | Required | Description |
|---|---|---|---|---|
| `email` | body | string | yes | New account email. |
| `password` | body | string | yes | New account password. |

# Response

| Field | Status | Type | Required | Description |
|---|---|---|---|---|
| `customerId` | 201 | string (uuid) | yes | Created customer. |

Responses `409`, `422`, and `429` have no response body.

## Status codes

| Code | When |
|---|---|
| 201 | account created |
| 409 | email already registered |
| 422 | weak or breached password |
| 429 | too many attempts from this IP |

# Validations

| Rule | Fails with |
|---|---|
| Fewer than the allowed attempts from this IP | `429` |
| `password` has at least 12 characters and is not on the breached-password list | `422` |
| `email` is not already in [customers](../../datastores/DB-shop/TBL-customers.md) | `409` |

# Behavior

Hashes the password with Argon2id and writes the row. On a duplicate email it
returns `409` **without** revealing whether the address was already registered in
the response timing — the same work is done either way, so registration cannot be
used to enumerate accounts.

# Flowchart

```mermaid
flowchart TD
    A[POST /accounts] --> B{Under the attempt limit for this IP?}
    B -- no --> X429[429]
    B -- yes --> C{Password at least 12 chars and not breached?}
    C -- no --> X422[422]
    C -- yes --> D[Hash with Argon2id, same work either way]
    D --> E{Email already registered?}
    E -- yes --> X409[409]
    E -- no --> F[Write customer row]
    F --> X201[201 customerId]
```

# Sequence diagram

```mermaid
sequenceDiagram
    actor Caller
    participant Accounts as SVC-accounts
    participant Customers as TBL-customers

    Caller->>Accounts: POST /accounts
    Accounts->>Accounts: Check per-IP rate limit and validate fields
    alt Rate limit exceeded
        Accounts-->>Caller: 429 Too Many Requests
    else Password weak or breached
        Accounts-->>Caller: 422 Unprocessable Entity
    else Input accepted
        Accounts->>Accounts: Hash password with Argon2id
        Accounts->>Customers: Insert customer by unique email
        alt Email already registered
            Customers-->>Accounts: Unique constraint violation
            Accounts-->>Caller: 409 Conflict
        else Customer created
            Customers-->>Accounts: customerId
            Accounts-->>Caller: 201 customerId
        end
    end
```
