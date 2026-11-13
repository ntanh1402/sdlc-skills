# Test design rules

## Coverage

- Requirement: at least one positive and one negative proof of each behaviour.
- User story: its acceptance criteria are proved in its own group by
  `sdlc-design-story-tests`; here, only flows that span stories.
- User flow: one `e2e` case in `GENERAL/` for each PRD user flow that spans
  two or more stories, walking the flow end to end.
- Endpoint: request partitions, validation, authentication, every status,
  side effects, idempotency, dependency failures, compatibility.
- Subscription and Channel: schema, ordering, duplicates, retry, exhaustion,
  dead letters, replay, poison messages, acknowledgement.
- Every exit of an Endpoint's or Subscription's `# Flowchart` and every rule
  of its `# Validations` is covered by at least one TestCase. List the exits
  and rules in the coverage matrix by hand.
- Data: constraints, transactions, concurrency, migration, rollback, retention.
- External: timeout, rate limit, malformed response, retry, fallback, recovery.
- Decision or quality target: prove the promised quality, or say that it is
  not covered here (a latency, throughput or capacity target is a load test,
  which the wiki does not keep).

## Required categories

The evidence makes a category required:

| Evidence | Required category |
|---|---|
| A Requirement with verification "test" on behaviour an actor sees | `functional` |
| A Requirement or decision about authentication, authorization, PII or audit, or `changeType: security` | `security-validation` |
| A new or changed Endpoint, Subscription or External Operation | `field-validation` and `error-handling` |
| A call to an External Operation or a message to another service | `integration` |

A required category is declined only with the user's explicit acceptance of
the residual risk.

## Categories to consider

For each endpoint and each acceptance criterion, consider which categories
apply, and write the cases that do. Each case carries one `testCategory`:

- `functional`: happy paths, alternate flows, business rules, state
  transitions.
- `field-validation`: required and optional fields, format, length, enum,
  null or blank, boundaries.
- `negative`: invalid business conditions, ineligible customers, accounts or
  cards, invalid states.
- `error-handling`: downstream errors, timeouts, retries, duplicates,
  idempotency and partial failures, where specified.
- `data-validation`: stored records, relationships, event payloads,
  consistency and audit fields, where observable.
- `security-validation`: authorization, access control and sensitive-data
  exposure within the documented scope (`security-checklist.md`).
- `integration`: calls to downstream systems: request and response mapping,
  correlation ids, downstream state and error propagation.

## Techniques

Use equivalence partitioning, boundary analysis, state transitions, decision
tables, pairwise interaction, fault injection and risk-based priority. Name the
technique when it changes how complete the cases are.

## No false completeness

Coverage is measured against the chosen categories. Record excluded
categories and their risks. Never add placeholder "not applicable" cases to make a matrix look
complete.
