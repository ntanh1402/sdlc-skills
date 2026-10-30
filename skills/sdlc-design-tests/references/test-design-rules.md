# Test design rules

What a case must cover, concept by concept, is in `classification.md`,
"Coverage rules" and "Field validation"; the techniques, risk and priority
are in the same file. This file holds the types the evidence makes required
and the rule on gaps.

## Required types

The evidence makes a suite type, or a category of cases, required:

| Evidence | Required type |
|---|---|
| A Requirement with verification "test" on behaviour an actor sees | `e2e` or `integration` |
| A Nonfunctional Requirement with a latency, throughput or capacity target | `performance` cases in `integration` or `e2e` |
| A Requirement or decision about authentication, authorization, PII or audit, or `changeType: security` | `security` cases at the level they test |
| A new or changed Endpoint, Subscription or External Operation | `integration` |
| An entry point with input fields | `field-validation` cases in `integration` |

A required type is declined only with the user's explicit acceptance of the
residual risk.

## No false completeness

Coverage is measured against the chosen suite types. Record excluded types and
their risks. Never add placeholder "not applicable" cases to make a matrix look
complete; list each gap as uncovered, with its reason.
