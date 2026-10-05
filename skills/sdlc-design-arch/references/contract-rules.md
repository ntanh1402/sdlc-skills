# Contract rules

The schema page of each type says which headings its file must have. These
rules say what a good contract puts in them.

## Frontends

- Every user-addressable route or screen, with its access rule.
- `# Calls` states, for each Endpoint or Operation, why the call happens and how
  loading, success and failure change what the user sees.
- An ExternalService reached through a listed Operation is not repeated under
  `# Depends on`.
- Runtime behaviour covers sessions, caching, and empty, loading and error
  states; a mobile app adds lifecycle, offline use and recovery.
- Quality constraints are measurable, not adjectives.

## Endpoints

- A resource-oriented path and correct protocol semantics.
- Complete request and response field tables, with conditional rules.
- Authentication, validation, idempotency, errors, compatibility and rate
  limits.
- Behaviour and the sequence diagram cover every outcome.

## Calls between services

- A Service's or Subscription's `# Calls` links each Endpoint or Operation it
  calls, with why. The reverse view is written by the tool; never write it.

## Events and subscriptions

- Key, headers, body, an example payload, schema version, ordering, retention.
- Publishers and subscribers come from the Service and Subscription files;
  the Channel's `# Publishers` and `# Subscribers` are written by the tool.
- Consumer group, delivery guarantee, idempotency, retry, dead letters and
  replay safety.

## Data

- One clear owner and source of truth.
- Required fields and nullability, indexes, PII, retention, migration and
  rollback.
- A Service links the tables it reads and writes; the Table's `# Used by` is
  written by the tool.

## Externals

- The exact Operations, authentication, timeout, rate and cost, and the
  validation boundary.
- Error mapping, retry policy, fallback and criticality.

Prefer additive changes. A breaking change needs an explicit migration and a
decision; never hide it in prose.
