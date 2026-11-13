---
type: TestCase
title: Password never plaintext
description: Prove credentials never persist or appear in logs as plaintext.
risk: critical
testType: integration
testCategory: security-validation
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Password never plaintext

# Covers

* [REQ-accounts-credential-safety](../../../features/FEAT-accounts/overview.md#req-accounts-credential-safety)
* [TBL-customers](../../../datastores/DB-shop/TBL-customers.md)

# Purpose

Prove credentials never persist or appear in logs as plaintext.

# Preconditions

Accounts service and test database are isolated; logs are captured.

Data that must exist:

* email: a unique email
* password: `NeverStore-Me-42!` (a marker to search for)

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call API `POST /accounts` with a unique email and password `NeverStore-Me-42!` | Response POST /accounts:<br>- status: 201<br>Table customers:<br>- Rows found for the email: 1 | Read the response and query table `customers` by email; check **status** and **rows found** |
| 2 | Read the stored password of that email from the accounts password store | Password store:<br>- stored value: starts with `$argon2id$`<br>- stored value: not `NeverStore-Me-42!` | Read the stored value; check its **prefix** and that it **differs** from the password |
| 3 | Search a dump of the test database and the captured service logs for `NeverStore-Me-42!` | Database dump and logs:<br>- Matches found: 0 | Run an exact text search; check **matches found** |

# Postconditions and cleanup

Delete customer and captured logs.
