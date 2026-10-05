# Story rules

## One story per actor goal

A story is one actor wanting one thing done, for a reason they would say
themselves. Split by who acts (shopper, support agent, administrator) and by
what they want done. Never split by screen, layer, service or Task: "build
the gift card table" is a Task, not a story.

Find the actors and goals in the PRD's users and flows. Requirements that
serve the same actor's same goal go in one story. A Requirement that serves
two goals goes in both stories.

## Which Requirements need a story

| Requirement | Story |
|---|---|
| Functional, `**Must**`, `**Should**` or `**Could**` | At least one story lists it |
| Functional, `**Wont**` | None; it is out of scope |
| Nonfunctional or Constraint | Optional: list it in the story whose criteria it shapes ("the confirmation appears within 2 seconds"), otherwise leave it to the Tasks |

A story lists at least one Functional Requirement. A story of Nonfunctional
Requirements only ("as an operator I want p95 under 300 ms") is not written.

## Acceptance criteria

- Numbered **Given** / **When** / **Then** scenarios, one behaviour each.
- Real values: "a card with a balance of 50", not "a valid card".
- Cover the main path, then each failure or limit the Requirements name.
- Each criterion ends with the links of the Requirements it shows. Each
  Requirement the story lists is shown by at least one criterion.
- A criterion shows a Requirement; it never adds behaviour. A behaviour the
  person wants that no Requirement states is a gap for `sdlc-write-spec`.

## INVEST check

Use it in the self review, one line per story:

| Letter | The story… | When it fails |
|---|---|---|
| Independent | can be built and demonstrated without another story | Merge the two, or cut along a different goal |
| Negotiable | states the need, not the design | Move design detail to `# Notes` or drop it |
| Valuable | gives the actor something they would notice | It is a Task; drop the story |
| Estimable | is clear enough for a team to size | Ask the person in the next round |
| Small | fits in one iteration | Split by sub-goal or by rule ("pay in full", "pay part"), never by layer |
| Testable | has criteria with real values | Rewrite the criteria |

## ChangeRequests

A ChangeRequest's stories list only its own Requirements, linked in its own
`overview.md`, and describe the change. When it changes a Requirement that a
Feature story lists (same key), name that Feature story under `# Affects` of
the story that lists the new text. Never edit the Feature's stories: they
describe the Feature as first delivered, and the tool writes `# Changed by`
on them.

## Revisions

Keep each existing story's key, even when its title changes. A Task may link
it, and a ticket may carry it. A story whose Requirements were all removed is
deleted; the log says why. In the same draft, drop the links to it from
every Task's `# Stories` and every ChangeRequest story's `# Affects`, and log
that in each folder you change. That link is the only edit this skill makes
outside its own stories.
