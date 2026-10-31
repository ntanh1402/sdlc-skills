---
type: TestCase
title: Cache holds under load
description: Prove catalog cache protects database during checkout peak.
risk: high
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Cache holds under load

# Covers

* [REQ-catalog-browse-by-category](../../features/FEAT-catalog/overview.md#req-catalog-browse-by-category)

# Purpose

Prove catalog cache protects database during checkout peak.

# Preconditions

Representative catalog is warm; cache/database telemetry is enabled.

# Test data

| No | Input | Value |
|---|---|---|
| 1 | catalog reads | 5 times the checkout request volume |
| 2 | key distribution | production-like |

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Drive catalog workload | Cache hit rate stays above 95% | Cache telemetry reports threshold continuously after ramp |
| 2 | Observe database | Database avoids saturation | CPU, connections, locks, and latency stay below limits |

# Postconditions and cleanup

Stop workload and archive telemetry; last hit rate was 97%.
