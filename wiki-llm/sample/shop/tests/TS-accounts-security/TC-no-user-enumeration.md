---
type: TestCase
title: No user enumeration
description: Prove login does not disclose whether an account exists.
risk: high
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# No user enumeration

# Covers

* [REQ-accounts-credential-safety](../../features/FEAT-accounts/overview.md#req-accounts-credential-safety)

# Purpose

Prove login does not disclose whether an account exists.

# Preconditions

One known account exists; timing capture is enabled.

# Test data

Known email with wrong password and unknown email with same password.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Run repeated known-email failures | Generic authentication failure | All statuses/bodies are identical within this cohort |
| 2 | Run repeated unknown-email failures | Same generic failure | Status/body matches known-email cohort byte for byte |
| 3 | Compare timing distributions | No statistically useful distinction | Timing threshold defined by suite policy is not exceeded |

# Postconditions and cleanup

Clear rate-limit state and timing samples.
