# Plan: Industry-shaped PRD, user stories and Tasks

**Date:** 2026-10-31
**Status:** Implemented; forward tests not run
**Related research:** [industry-standards-prd-user-story-task.md](research/industry-standards-prd-user-story-task.md)

## 1. Why

1. **The PRD, stories and Tasks should read like the industry standard**, so an
   agent can turn any of them into a public version (Jira, Confluence, a
   document) by dropping the wiki's links and terms, without restructuring.
2. **Given/When/Then in stories repeats the TestCases.** A story's criteria
   should state the rules that must hold; the TestCases hold data and steps.
3. **Stories are split badly.** A flat list of Requirements leads to stories
   that cannot ship or be tested alone (`STORY-checkout-retry-safely`).
4. **A Task linked to two stories cannot be a tracker sub-task**, which has one
   parent in Jira, Linear, Azure DevOps and GitHub alike.
5. **QA cannot tell which test cases to run for a story** when its ticket
   reaches "test", and test cases do not cover every story rule.
6. **The `unit` suite type is confused with a developer's unit tests.**

How things are published to Jira or Confluence is out of scope: no skill
reads or writes the tracker, as today.

## 2. Decisions

### PRD (`sdlc-write-spec`)

1. Feature PRD headings, in this order: `Summary`, `Problem and evidence`,
   `Goals and success metrics`, `Users and personas`, `User flows`,
   `Business rules`, `Requirements`, `Release and rollout` (optional, only
   when the brief mentions phases, a flag, a migration or a deadline),
   `Risks, assumptions and open questions`, `Out of scope`.
2. Dropped: `Scope` (the flows and Requirements say it), `Acceptance` (the
   Requirements and stories hold it), `Data and events` (business rules or
   Nonfunctional Requirements), and the prose `Functional requirements` and
   `Nonfunctional requirements`.
3. One copy of the Requirements: the `REQ-*` entries stay in `overview.md`.
   The PRD's `## Requirements` holds one line saying so; a converting agent
   inserts the entries there.
4. No metadata block in `prd.md`: status, version, owner team, priority,
   target release and Epic key are Feature fields; a converting agent takes
   them from there.
5. The change PRD keeps its own shape, with the same merge (`Risks,
   assumptions and open questions`), the same single copy of the
   Requirements for `Changed and regression requirements`, and no
   `Acceptance`.
6. The interview's readiness list follows the PRD sections, one line each. It
   asks for a primary and a guardrail metric; a missing number is an open
   question that does not block `ReqApproved`. No anti-personas: `Out of
   scope` holds exclusions. Rollout is asked only when relevant.
7. Existing PRDs stay valid (nothing checks PRD headings). A PRD is rewritten
   whole in the new shape only when `sdlc-write-spec` revises its Feature or
   ChangeRequest for a real reason; content no new section takes is shown at
   the Design gate as a gap. There is no conversion-only run, so no version
   bump or status change for a cosmetic edit. PRDs of `Approved` or later
   Features stay in the old shape.

### User stories (`sdlc-write-stories`)

8. Acceptance criteria are numbered pass/fail rules with concrete boundaries
   and outcomes, each ending with the Requirements it shows, grouped as
   input/precondition, state/output, boundary/idempotency, and
   rejection/invariant rules. The validator drops only the Given/When/Then
   check, so existing stories stay valid.
9. Splitting: classify each Requirement as SPINE (a primary user action),
   RULE (a validation or invariant during a SPINE) or EXTENSION (a later
   variation); a Nonfunctional or Constraint Requirement keeps its own type.
   The labels are worked out from the current Requirements in every run and
   never stored. Group SPINEs by actor and surface; fold RULEs and observable
   Nonfunctional Requirements into the SPINE story they govern; split
   oversized stories vertically (by rule type, workflow step, input
   variation, lifecycle or actor), never by layer.
10. A rule that governs two stories goes in both.
11. The INVEST check gains "one actor on one surface". There is no separate
    gate and no rule-count limit.
12. A story the skill touches for any reason is rewritten whole in the new
    form. Old stories are converted on request through the existing "revise
    the stories" case.
13. Story writing ignores the QA test categories.

### Tasks (`sdlc-plan-tasks`)

14. A Task serves 0 or 1 story (`"max": 1` on `# Stories`), worded
    tracker-neutral: a Task with one story is that story's sub-task; a Task
    with none is a foundation, migration, spike or Nonfunctional Task under
    the Feature or ChangeRequest.
15. Several story Tasks may change one concept (two stories both modify
    `WEB-storefront`), each listing it in `# Planned scope` with a note naming
    its slice. A concept several stories need and none owns gets one 0-story
    foundation Task; one a single story owns is built by that story's Task.
    The self review checks that every concept is covered, and that a
    concept several stories need is built by its owning story's Task or by
    one foundation Task that blocks the Tasks that use it, not that every
    concept has exactly one owner. The pending entry already closes only
    when every covering Task is Done.
16. No fixed waves: each Task's `# Blocked by` sets the order, a 0-story
    foundation comes before the story Tasks it unblocks, and the computed
    waves report at the Design gate stays.
17. `sdlc-plan-tasks` goes on when the person asks to replan, as
    `sdlc-write-stories` does.
18. "One code repository per Task" is already a rule; nothing changes.

### Tests (`sdlc-design-tests`)

19. Requirements and contracts stay the test unit; a TestCase's `# Covers`
    keeps linking them, never stories.
20. The skill reads the stories, takes each story rule as a partition of the
    Requirement it cites, and its self review checks that every rule has a
    case.
21. The e2e suite has a case for each PRD user flow that spans two or more
    stories.
22. The skill no longer proposes `unit` suites. The enum keeps `unit`,
    documented as "older suites only; no skill writes it".
23. A guideline, not a check: consider Functional, Field Validation,
    Negative, Error Handling, Data Validation and Security Validation cases
    for each endpoint and story rule.
24. `sync` writes a `# Test cases` section on each story: the cases whose
    `# Covers` links a Requirement the story lists, plus the cases covering a
    concept in the `# Planned scope` of the story's Tasks. QA opens it from
    the wiki path on the ticket. A case may appear on several stories.

### Upgrade (`sdlc-setup-wiki`)

25. The schema version stays `1`; no migration.
26. After `copy install`, the upgrade runs `validate`. For each Task with two
    or more stories it asks, in one round, which story the Task keeps
    (recommending the story that lists the Requirements its `# Acceptance` links), drops the other links,
    and logs them, for example
    `* **Upgrade**: Kept STORY-checkout-pay-and-confirm; also served STORY-checkout-retry-safely (one story per Task since <release>).`
    Section 6.1's "do not fix wiki content" names this as its one exception.
    The summary's "Next" names `sdlc-plan-tasks` for the unlinked stories of
    open Features. A story with no Task is not a validator error.

### Unchanged

27. Feature and ChangeRequest schema, `sdlc-review-code`, `sdlc-build-task`
    (it already reads the Task's stories).

## 3. Files

### Schema and tool (`wiki-llm/`, then `python3 release.py`)

- `schema/schema.json`: Task `# Stories` `"max": 1`; UserStory `# Test cases`,
  tool-written.
- `schema/user-story.md`: the criteria rule (pass/fail rules); `# Test cases`.
- `schema/task.md`: `# Stories` links at most one story; shared concepts with a
  slice note. Regenerate the tables with `docs.write()`.
- `schema/test-suite.md`: `unit` is for older suites only.
- `tools/wikilib/rules/stories.py`: drop `STEPS` and the Given/When/Then check.
- `tools/wikilib/sync.py`: derive `# Test cases` (two steps: story →
  Requirement ← TestCase, and story ← Task → concept ← TestCase). Today's
  generated sections only mirror a direct link, so this is new code.
- `tools/tests/`: `test_rules_stories.py` (drop the Given/When/Then test; a
  Task with two stories fails `relationships.cardinality`), `test_sync.py`
  (`# Test cases`), `fixture.py` (checklist criteria).

### Skills

- `sdlc-write-spec`: `references/prd-templates.md` (decisions 1–5),
  `references/interview-guide.md` (6), `SKILL.md` (7: rewrite the PRD whole in
  a revision).
- `sdlc-write-stories`: `references/story-rules.md` (8–11),
  `references/story-format.md` and `references/paste-format.md` (checklist
  examples), `SKILL.md` (12, description).
- `sdlc-ask-wiki`: `references/paste-format.md` (checklist examples).
- `sdlc-plan-tasks`: `references/decomposition-rules.md` (14–16),
  `references/task-format.md`, `SKILL.md` (14, 15, 17; the self review).
- `sdlc-design-tests`: `SKILL.md` (suite types without `unit`; 20, 21 in the
  self review), `references/test-design-rules.md` (20, 21, 23).
- `sdlc-setup-wiki`: `SKILL.md` section 3 (26) and section 6.1 (the exception).

### Forward tests, glossary, guide

- `forward-tests/sample/shop/features/FEAT-checkout/`: fold
  `STORY-checkout-retry-safely` into `STORY-checkout-pay-and-confirm`, delete
  it, run `sync`.
- `forward-tests/fixtures/gift-cards-stories/`,
  `forward-tests/sdlc-write-stories/*.md`: checklist criteria.
- `forward-tests/sdlc-write-spec/brief.md`, `resume-plan.prd.md`,
  `forward-tests/fixtures/gift-cards-spec/.../prd.md`: the new PRD headings.
- New `forward-tests/sdlc-setup-wiki/upgrade-task-with-two-stories.md`, with a
  fixture adding a second Given/When/Then story linked from
  `TASK-order-creation-endpoint`: the upgrade names the Task, asks which story
  it keeps, drops the other with a log entry, finishes `ok`, and the old
  stories stay valid.
- `CONTEXT.md` ("User story"), `user-guide/user-guide.md`,
  `user-guide/sdlc-write-stories.md`, `user-guide/sdlc-design-tests.md`,
  `user-guide/sdlc-write-spec.md`.

## 4. Verify

```bash
python3 -c 'import sys; sys.path.insert(0, "wiki-llm/tools"); from wikilib import docs, schema; docs.write(schema.load())'
python3 release.py
python3 -m unittest discover -s wiki-llm/tools/tests -t wiki-llm/tools
```

Then run by hand the forward tests of `sdlc-write-spec`,
`sdlc-write-stories`, `sdlc-plan-tasks`, `sdlc-design-tests` and the new
`sdlc-setup-wiki` scenario.
