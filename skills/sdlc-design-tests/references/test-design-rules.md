# Test design rules

## Coverage

- Requirement: at least one positive and one negative proof of each behaviour.
- Endpoint: request partitions, validation, authentication, every status,
  side effects, idempotency, dependency failures, compatibility.
- Subscription and Channel: schema, ordering, duplicates, retry, exhaustion,
  dead letters, replay, poison messages, acknowledgement.
- Data: constraints, transactions, concurrency, migration, rollback, retention.
- External: timeout, rate limit, malformed response, retry, fallback, recovery.
- Decision or quality target: prove the promised quality, or say which suite
  owns it.

## Required types

The evidence makes a suite type required:

| Evidence | Required type |
|---|---|
| A Requirement with verification "test" on behaviour an actor sees | `e2e` or `integration` |
| A Nonfunctional Requirement with a latency, throughput or capacity target | `load` |
| A Requirement or decision about authentication, authorization, PII or audit, or `changeType: security` | `security` |
| A new or changed Endpoint, Subscription or External Operation | `integration` |

A required type is declined only with the user's explicit acceptance of the
residual risk.

## Techniques

Use equivalence partitioning, boundary analysis, state transitions, decision
tables, pairwise interaction, fault injection and risk-based priority. Name the
technique when it changes how complete the cases are.

## No false completeness

Coverage is measured against the chosen suite types. Record excluded types and
their risks. Never add placeholder "not applicable" cases to make a matrix look
complete.
