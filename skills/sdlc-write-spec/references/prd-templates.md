# PRD templates and quality checks

Use this after part 2 of the Intent gate, to write the PRD and its Requirement
mapping for the Design gate.

## Feature PRD (`references/REF-<name>-prd/prd.md`)

Use these headings, in this order, under the `# <Feature> PRD` title. They
follow the common industry PRD shape, so the PRD can be turned into a
document outside the wiki by dropping its links, without restructuring.

```markdown
## Summary
## Problem and evidence
## Goals and success metrics
## Users and personas
## User flows
## Business rules
## Requirements
## Release and rollout
## Risks, assumptions and open questions
## Out of scope
```

- `## Summary`: two or three sentences: what changes for whom, and why now.
- `## Goals and success metrics`: a primary metric and a guardrail metric,
  each with its baseline and target when known.
- `## User flows`: one subsection per flow, with its happy, alternate and
  failure paths.
- `## Requirements` holds only this line, because the Requirements live once,
  in the Feature's `overview.md`:
  `The Requirements are listed in the Feature's overview.md, under # Requirements.`
- `## Release and rollout`: only when the brief names phases, a feature
  flag, a migration of users or data, or a deadline; otherwise leave the
  heading out.
- No metadata block: status, version, owner team, priority, target release
  and Epic key are the Feature's fields.

## Change PRD (`references/REF-<name>-change-prd/change-prd.md`)

Under the `# <Change> PRD` title:

```markdown
## Target Feature
## Reason
## Before and after
## Changed flow
## Changed and regression requirements
## Impact hypothesis
## Constraints and compatibility
## Risks, assumptions and open questions
## Out of scope
```

`## Changed and regression requirements` holds only this line:
`The Requirements are listed in the ChangeRequest's overview.md, under # Requirements.`
It names in prose the guarantees that must not regress.

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
| REQ-wishlist-save-product | User flows; Business rules | test | New behaviour |
```

Every Requirement maps to approved PRD text. Every acceptance-critical
behaviour in the PRD maps to a Requirement, or the PRD says why it stays
context. The Design gate covers the full PRD and the mapping; any edit needs
the gate again.
