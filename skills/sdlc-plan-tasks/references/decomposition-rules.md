# Decomposition rules

## Vertical slices

A good Task delivers one observable behaviour across the layers it needs.
Prefer "accept an order and persist it as pending" over separate endpoint and
table Tasks.

Split when parts have independent acceptance, owners, rollout or failure
modes, or can ship separately. Keep together when splitting leaves a half that
nobody can use.

## Order

1. Spikes that reduce risk, and decisions still to close.
2. Shared contracts and backward-compatible foundations.
3. Data and schema migrations, with rollback.
4. A producer before its consumer when the contract cannot deploy on its own.
5. Vertical behaviour slices.
6. Observability, rollout, removal and clean-up.

## Acceptance

Acceptance links the Requirements and contracts it satisfies and states
observable results, including failure behaviour, compatibility, telemetry and
rollback when they matter. It never repeats the title. The unit and component
tests a developer writes with the code belong in acceptance; full test design
belongs to `sdlc-design-tests`.

## Ownership

Every new, changed or removed concept in the design, every obligation of a
decision, every migration and every rollout duty has exactly one owning Task.
Other Tasks may take part, but ownership is single. A title that joins two
independent outcomes with "and" is two Tasks.

## Parallel waves

Wave 1 is every Task with no blocker. Wave n is every Task whose blockers are
all in earlier waves. Report the waves at the Design gate.
