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
belongs to `sdlc-design-story-tests` and `sdlc-design-feature-tests`.

## Stories and coverage

A Task serves at most one story, so in any tracker it can be that story's
sub-task. A Task with no story sits under the Feature or ChangeRequest. Cut
the plan by story first: each story gets the Tasks that deliver its
acceptance criteria end to end.

- Every new, changed or removed concept in the design, every obligation of a
  decision, every migration and every rollout duty is covered by at least
  one Task.
- Two stories that change one concept (both add to `WEB-storefront`) each
  get their own Task listing it, with a note naming the part it builds
  ("— modified — the gift card field").
- An `orders` table that the pay story creates and the order-history story
  only reads is built by the pay story's Task; the history Task is
  `# Blocked by` it.
- A table or contract two stories both use and neither owns is built by one
  foundation Task with no story; the Tasks that use it are `# Blocked by` it.
- A title that joins two independent outcomes with "and" is two Tasks.

## Parallel waves

There is no fixed wave layout: each Task's `# Blocked by` sets the order.
Wave 1 is every Task with no blocker. Wave n is every Task whose blockers are
all in earlier waves. Report the computed waves at the Design gate.
