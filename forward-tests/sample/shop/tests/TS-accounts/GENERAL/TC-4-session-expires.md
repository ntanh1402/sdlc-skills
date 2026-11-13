---
type: TestCase
title: Session expires
description: Prove expired sessions cannot authorize profile access.
risk: high
testType: integration
testCategory: security-validation
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Session expires

# Covers

* [REQ-accounts-login-session](../../../features/FEAT-accounts/overview.md#req-accounts-login-session)

# Purpose

Prove expired sessions cannot authorize profile access.

# Preconditions

Known account exists and test clock is controllable.

Data that must exist:

* session: one issued session
* clock: advanced 1 second beyond the TTL

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call API `POST /accounts/login` with the registered account's email and password | Response POST /accounts/login:<br>- status: 200<br>Cache session:{token}:<br>- Entry found: yes | Look up the returned token in the cache; check **status** and **entry found** |
| 2 | Advance the test clock 1 second beyond the session TTL | Cache session:{token}:<br>- Entry found: no | Look up the token in the cache; check **entry found** |
| 3 | Call API `GET /accounts/me` with the token the login returned | Response GET /accounts/me:<br>- status: 401<br>- profile fields: absent | Read the response; check **status** and that no **profile field** is returned |

# Postconditions and cleanup

Reset test clock and delete account/session.
