# Test design rules

## Coverage

- Requirement: at least one positive and one negative proof of each behaviour.
- User story: each acceptance criterion is a partition of the Requirement it
  cites, with at least one case. The case's `# Covers` links the
  Requirement, never the story; the tool lists the case on the story.
- User flow: one `e2e` case for each PRD user flow that spans two or more
  stories, walking the flow end to end.
- Endpoint: request partitions, validation, authentication, every status,
  side effects, idempotency, dependency failures, compatibility.
- Subscription and Channel: schema, ordering, duplicates, retry, exhaustion,
  dead letters, replay, poison messages, acknowledgement.
- Every exit of an Endpoint's or Subscription's `# Flowchart` and every rule
  of its `# Validations` is covered by at least one TestCase. The packet's
  coverage check lists them.
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

## Kinds of case to consider

A guideline to think with: for each endpoint and each story's acceptance
criterion, consider which of these apply, and write the cases that do.

- Functional: the rule does what it says on the main path.
- Field validation: each input's type, format, length and required rules.
- Negative: invalid, missing or unexpected input is refused cleanly.
- Error handling: dependency failures, timeouts and the error returned.
- Data validation: what is stored or emitted is correct and consistent.
- Security validation: access, authorization and the abuse the rule invites.

The kinds stay in your reasoning; a case carries no kind label.

## Techniques

Use equivalence partitioning, boundary analysis, state transitions, decision
tables, pairwise interaction, fault injection and risk-based priority. Name the
technique when it changes how complete the cases are.

## No false completeness

Coverage is measured against the chosen suite types. Record excluded types and
their risks. Never add placeholder "not applicable" cases to make a matrix look
complete.
