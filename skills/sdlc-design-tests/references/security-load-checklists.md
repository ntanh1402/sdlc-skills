# Security and load checklists

## Security suite

- Missing, expired and revoked authentication; session fixation.
- Horizontal and vertical authorization; tenant isolation.
- Injection, malformed payloads, unsafe deserialization, file and path abuse.
- Rate and abuse controls, replay, CSRF where relevant, leaked secrets or
  tokens.
- PII minimization, encryption, retention and deletion, audit evidence.
- External and webhook signature checks; failures at trust boundaries.

## Load suite

- Baseline, target, peak, spike, soak and recovery profiles, when required.
- Latency percentiles, throughput, error rate, saturation, queue lag and cost.
- Hot keys and partitions, connection pools, back pressure, autoscaling and
  retry amplification.
- An explicit workload model, dataset size, ramp, duration, thresholds and
  abort conditions.

Create these suites only when the user chooses them. Every threshold comes from
a Requirement, a decision, an SLO or an assumption the user approved.
