---
type: TestCase
title: Peak throughput
description: Prove checkout sustains modelled peak within latency/error budgets.
risk: critical
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Peak throughput

# Covers

* [EP-orders-create](../../services/SVC-orders/EP-orders-create.md)

# Purpose

Prove checkout sustains modelled peak within latency/error budgets.

# Preconditions

Production-like staging is healthy, monitoring enabled, and test data preloaded.

# Test data

Ramp from baseline to 3,000 checkouts/min; hold peak for 10 minutes.

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Ramp workload to target | Services scale without sustained errors | Throughput reaches 3,000/min and health checks remain passing |
| 2 | Hold peak for 10 minutes | p99 stays below 800 ms and errors below 0.1% | k6/telemetry aggregates satisfy both thresholds |
| 3 | Stop load | System returns to baseline | Queue lag, saturation, and latency recover inside agreed window |

# Postconditions and cleanup

Remove load fixtures and archive telemetry; last p99 was 620 ms.
