# Architecture checklist

## Boundaries and flow

- Map each Requirement and actor step to one owning Service, and each
  user-facing surface to one owning WebFrontend or MobileFrontend.
- Reuse an existing concept unless a different ownership or lifecycle boundary
  is proven.
- Show synchronous calls, asynchronous messages, data access and external
  dependencies.
- Name the transaction boundaries and the consistency model.

## Existing or new

For each concept the design needs, decide in this order:

1. An existing concept already does it: reuse it, unchanged.
2. An existing concept owns the data or behaviour and can be extended without
   breaking its consumers: modify it (`Modifying`, a pending entry).
3. A different owner, lifecycle, scaling or security boundary is proven: add a
   new concept (`Planned`, a pending entry).
4. The Requirement retires a concept: remove it (`Removing`, a pending entry,
   file kept until the Task that removes it is done).

## Quality attributes

- Authentication, authorization, secrets, audit, privacy, abuse protection.
- Latency, throughput, load shape, availability, recovery and cost.
- Idempotency, retry, timeout, circuit breaking, ordering, dead letters and
  fallback.
- Logging, metrics, traces, SLOs, alerts, dashboards and runbooks.
- Backward compatibility, migration, rollout, feature flags and rollback.

## Drift

When the code or a live contract disagrees with the wiki, classify the
difference. Drift is a difference that nothing in the wiki marks as not built
yet, so expected lag is not Drift.

| Class | Meaning | Do |
|---|---|---|
| Expected lag | The wiki marks exactly this difference as not built yet: a pending entry, or an `Approved` ChangeRequest on the Feature | Design on the wiki target |
| Minor Drift | Naming or documentation differences that do not change a decision | Report it in the packet; design on the wiki |
| Material Drift | The code behaves differently in a way that changes a design decision | Stop, show both with evidence, and ask which is true. Name the remedy: `sdlc-import` on that code when the wiki is wrong, a bugfix ChangeRequest with `sdlc-write-spec` when the code is wrong |

## Review packet

- Context and constraints.
- Concept ledger with a reason for every row.
- High-level and runtime Mermaid diagrams.
- Contract and data details.
- Decisions and the alternatives rejected.
- Requirement traceability, open risks and downstream freshness.
