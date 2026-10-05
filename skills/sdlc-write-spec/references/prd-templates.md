# PRD templates and quality checks

Use this after part 2 of the Intent gate, to write the PRD and its Requirement
mapping for the Design gate.

## Feature PRD (`prd.md`)

Use these headings, in this order, under the `# <Feature> PRD` title:

```markdown
## Objective
## Users and actors
## Problem and evidence
## Scope
## User and system flow
## Business rules
## Functional requirements
## Nonfunctional requirements
## Data and events
## Success measures
## Acceptance
## Risks and constraints
## Assumptions and open questions
## Out of scope
```

## Change PRD (`change-prd.md`)

Under the `# <Change> PRD` title:

```markdown
## Target Feature
## Reason
## Before and after
## Changed flow
## Changed and regression requirements
## Impact hypothesis
## Risk
## Acceptance
## Constraints and compatibility
## Assumptions and open questions
## Out of scope
```

## Content quality

- State a user or business objective, not a solution summary.
- Name actors, triggers, happy, alternate and failure behaviour, boundaries
  and business rules precisely enough to derive testable Requirements.
- Separate evidence from assumptions. Keep open decisions visible.
- Describe data, events and external interactions only as behaviour, with
  sensitivity, retention, ordering or delivery constraints when they matter.
- Give measurable success and quality targets when known. Never invent a
  number; name the missing decision.
- For a change: current against desired behaviour, the guarantees that must
  not regress, the rejected no-change option, compatibility constraints, and
  the Requirements added, changed and removed.
- Make exclusions explicit; keep the smallest useful scope.

Leave the solution out: service boundaries, endpoints, schemas, tables,
vendors, deployment, migrations, code, commands, diagrams, decisions,
implementation plans, Tasks and TestSuites. An open architecture concern may
appear as an open question, never as a decision.

## Requirements and the mapping

Write one independently testable behaviour or constraint per Requirement, in
the grammar of the schema page `feature.md`: a `### REQ-<feature>-<name>`
heading, then the priority in bold, the text, the type and the verification
method. Split outcomes that can ship separately.

```markdown
### REQ-wishlist-save-product

**Must** — A signed-in shopper can save a product to a named wishlist.
Functional. Verified by test.

### REQ-wishlist-save-fast

**Should** — Saving a product completes within 300 ms at p95 under the agreed
load profile. Nonfunctional. Verified by test.

### REQ-wishlist-owner-only

**Must** — Wishlist contents are visible only to their owner.
Constraint. Verified by inspection.
```

After the PRD, show one mapping row per Requirement:

```markdown
| Requirement | PRD sections | Verification | Notes |
|---|---|---|---|
| REQ-wishlist-save-product | User and system flow; Functional requirements | test | New behaviour |
```

Every Requirement maps to approved PRD text. Every acceptance-critical
behaviour in the PRD maps to a Requirement, or the PRD says why it stays
context. The Design gate covers the full PRD and the mapping; any edit needs
the gate again.
