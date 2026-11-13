---
type: TestCase
title: Login rate limited
description: Prove repeated failed authentication is throttled.
risk: high
testType: integration
testCategory: security-validation
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Login rate limited

# Covers

* [EP-accounts-login](../../../services/SVC-accounts/EP-accounts-login.md)

# Purpose

Prove repeated failed authentication is throttled.

# Preconditions

Known account exists and rate-limit state is empty.

Data that must exist:

* account: one registered account
* attempts: 6 wrong passwords inside 60 seconds

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call API `POST /accounts/login` five times within 60 seconds with the registered account's email and a wrong password | Response POST /accounts/login:<br>- status: 401 each time<br>Cache session:{token}:<br>- Entries found for the account: 0 | Read each response and look up the session cache; check **status** and **entries found** |
| 2 | Call API `POST /accounts/login` a sixth time within the same 60 seconds with the same email and a wrong password | Response POST /accounts/login:<br>- status: 429<br>- Retry-After header: present | Read the response; check **status** and **Retry-After** |

# Postconditions and cleanup

Clear account rate-limit state.
