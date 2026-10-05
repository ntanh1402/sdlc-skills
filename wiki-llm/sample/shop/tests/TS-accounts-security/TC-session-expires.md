---
type: TestCase
title: Session expires
description: Prove expired sessions cannot authorize profile access.
risk: high
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Session expires

# Covers

* [REQ-accounts-login-session](../../features/FEAT-accounts/overview.md#req-accounts-login-session)

# Purpose

Prove expired sessions cannot authorize profile access.

# Preconditions

Known account exists and test clock is controllable.

# Test data

One issued session and clock advanced one second beyond TTL.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Log in | Session is issued | Token exists in session cache |
| 2 | Advance clock beyond TTL | Session becomes invalid | Cache lookup reports expired/absent token |
| 3 | Call `GET /accounts/me` | Request is unauthorized | Status is 401 and no profile data is returned |

# Postconditions and cleanup

Reset test clock and delete account/session.
