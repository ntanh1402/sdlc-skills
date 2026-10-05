---
type: TestCase
title: Login rate limited
description: Prove repeated failed authentication is throttled.
risk: high
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Login rate limited

# Covers

* [EP-accounts-login](../../services/SVC-accounts/EP-accounts-login.md)

# Purpose

Prove repeated failed authentication is throttled.

# Preconditions

Known account exists and rate-limit state is empty.

# Test data

Six wrong-password attempts for one account inside 60 seconds.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Submit five failed logins | Each request is rejected without lockout response | Each status is 401 and no session exists |
| 2 | Submit sixth failed login | Request is rate limited | Status is 429 and retry metadata is present |

# Postconditions and cleanup

Clear account rate-limit state.
