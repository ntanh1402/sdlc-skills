---
type: TestCase
title: No user enumeration
description: Prove login does not disclose whether an account exists.
risk: high
testType: integration
testCategory: security-validation
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# No user enumeration

# Covers

* [REQ-accounts-credential-safety](../../../features/FEAT-accounts/overview.md#req-accounts-credential-safety)

# Purpose

Prove login does not disclose whether an account exists.

# Preconditions

One known account exists; timing capture is enabled.

Data that must exist:

* known email: a registered email with a wrong password
* unknown email: an unregistered email with the same password

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call API `POST /accounts/login` 20 times with the registered email and a wrong password | Response POST /accounts/login:<br>- status: 401<br>- body: the generic authentication error | Compare the 20 responses; check **status** and **body** are the same each time |
| 2 | Call API `POST /accounts/login` 20 times with the unregistered email and the same wrong password | Response POST /accounts/login:<br>- status: 401<br>- body: the generic authentication error, byte for byte | Compare with the registered-email responses; check **status** and **body** |
| 3 | Compare the response times of the registered-email and the unregistered-email calls | Response times:<br>- Difference of the medians: under 10 ms | Compute the median of each set of 20; check the **difference of the medians** |

# Postconditions and cleanup

Clear rate-limit state and timing samples.
