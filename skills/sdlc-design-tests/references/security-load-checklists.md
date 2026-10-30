# Security and load checklists

## Security cases

- Missing, expired and revoked authentication; session fixation.
- Horizontal and vertical authorization, access to another actor's data;
  tenant isolation.
- Injection, malformed payloads, unsafe deserialization, file and path abuse.
- Rate and abuse controls, replay, CSRF where relevant, leaked secrets or
  tokens.
- Sensitive data: minimization, masking in responses, messages, files and
  logs, encryption, retention and deletion; audit evidence.
- External and webhook signature checks; failures at trust boundaries.

## Performance cases

- Baseline, target, peak, spike, soak and recovery profiles, when required.
- Latency percentiles, throughput, error rate, saturation, queue lag and cost.
- Hot keys and partitions, connection pools, back pressure, autoscaling and
  retry amplification.
- An explicit workload model, dataset size, ramp, duration, thresholds and
  abort conditions.

`security` cases are written for every entry point that needs identity or
a role, or handles sensitive data (`classification.md`, "Coverage rules"),
unless the user declines them and accepts the residual risk. `performance`
cases are written only when the user chooses that category. Every threshold
comes from a Requirement, a decision, an SLO or an assumption the user
approved.
