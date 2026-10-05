---
type: TestCase
title: Password never plaintext
description: Prove credentials never persist or appear in logs as plaintext.
risk: critical
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Password never plaintext

# Covers

* [REQ-accounts-credential-safety](../../features/FEAT-accounts/overview.md#req-accounts-credential-safety)
* [TBL-customers](../../datastores/DB-shop/TBL-customers.md)

# Purpose

Prove credentials never persist or appear in logs as plaintext.

# Preconditions

Accounts service and test database are isolated; logs are captured.

# Test data

Unique email and marker password `NeverStore-Me-42!`.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Register with marker password | Account is created | Response is successful and customer row exists |
| 2 | Read password field | Argon2id hash is stored | Value starts with Argon2id marker and differs from input |
| 3 | Search database and captured logs for marker | Plaintext is absent | Exact marker search returns zero matches outside test input |

# Postconditions and cleanup

Delete customer and captured logs.
