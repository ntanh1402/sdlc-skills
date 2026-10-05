---
type: Feature
title: Accounts
description: Let customers register, log in, and manage their profile.
status: Released
ownerTeam: accounts
priority: P0
targetRelease: "2026.3"
releasedAt: 2026-03-10T00:00:00Z
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
sources:
  - id: accounts-prd
    resource: https://acme.atlassian.net/wiki/spaces/SHOP/pages/12440
    title: Accounts PRD
---

# Accounts

Customer identity for the whole platform: register, log in, and hold the session
every other service authenticates against. Owned by `accounts`. Part of the
[Shop Platform](../../overview.md).

# Requirements

### REQ-accounts-register

**Must** — A visitor can register with an email and a strong password.
Functional. Verified by test.

### REQ-accounts-login-session

**Must** — A registered customer can log in and receive a session valid for 24
hours. Functional. Verified by test.

### REQ-accounts-credential-safety

**Must** — Passwords are stored only as salted hashes, login is rate-limited, and
errors do not reveal whether an email is registered. Non-functional. Verified by
test.

# Architecture

Approved target state.

## Context and constraints

Credentials and profiles stay in the customer table; session validity has one
cache authority shared by authenticated services.

## High-level architecture

```mermaid
flowchart LR
  User --> Accounts[SVC-accounts]
  Accounts --> Customers[TBL-customers]
  Accounts --> Sessions[CACHE-session]
```

## Services

* [SVC-accounts](../../services/SVC-accounts/overview.md) — registration, login, profile, and session issuance.

## Runtime sequences

```mermaid
sequenceDiagram
  actor User
  participant Accounts as SVC-accounts
  participant Customers as TBL-customers
  participant Sessions as CACHE-session
  User->>Accounts: register or log in
  Accounts->>Customers: validate/store identity
  Accounts->>Sessions: issue session
  Sessions-->>Accounts: session token
  Accounts-->>User: authenticated response
```

## Decisions

None recorded.

## Traceability

| Requirement | Target concepts |
|---|---|
| [REQ-accounts-register](#req-accounts-register) | [SVC-accounts](../../services/SVC-accounts/overview.md), [TBL-customers](../../datastores/DB-shop/TBL-customers.md) |
| [REQ-accounts-login-session](#req-accounts-login-session) | [SVC-accounts](../../services/SVC-accounts/overview.md), [CACHE-session](../../datastores/CACHE-session/overview.md) |
| [REQ-accounts-credential-safety](#req-accounts-credential-safety) | [SVC-accounts](../../services/SVC-accounts/overview.md), [TBL-customers](../../datastores/DB-shop/TBL-customers.md) |

# Change history

None
