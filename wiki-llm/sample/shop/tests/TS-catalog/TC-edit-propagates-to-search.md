---
type: TestCase
title: Edit propagates to search
description: Prove catalog edits reach search within the consistency SLA.
risk: high
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Edit propagates to search

# Covers

* [REQ-catalog-keyword-search](../../features/FEAT-catalog/overview.md#req-catalog-keyword-search)

# Purpose

Prove catalog edits reach search within the consistency SLA.

# Preconditions

Indexed product exists and event-lag timer is enabled.

# Test data

Unique old and new product titles.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Rename product | Source record changes and event is published | Database and captured event carry new title/version |
| 2 | Wait for consumer acknowledgement | Projection is updated inside SLA | Lag timer stays below SLA and consumer reports success |
| 3 | Search new and old titles | New title resolves; old title does not | Search IDs and titles match expected product |

# Postconditions and cleanup

Delete source and search fixtures.
