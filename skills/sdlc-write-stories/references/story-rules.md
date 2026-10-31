# Story rules

## One story per actor goal

A story is one actor wanting one thing done on one surface (a page, an app,
an API a partner calls), for a reason they would say themselves. Never split
by layer, service or Task: "build the gift card table" is a Task, not a
story. Find the actors, surfaces and goals in the PRD's users and flows.

## Splitting the Requirements into stories

Work these steps out from the current Requirements in every run. The labels
are only for your reasoning: never write them into a file.

1. Mark each Functional Requirement:
   - **SPINE**: an action the actor takes to reach a goal ("a customer pays
     with a gift card").
   - **RULE**: a validation, limit or invariant that holds while a SPINE
     happens ("a card pays at most its balance"). Not to be confused with
     the business rules of the PRD.
   - **EXTENSION**: a later variation of a SPINE ("pay part with a card and
     the rest by another method").
   A Nonfunctional Requirement or Constraint keeps its own type.
2. Group the SPINEs by actor and surface: each group is a story.
3. Fold each RULE, and each Nonfunctional Requirement the actor would
   observe ("the confirmation appears within 2 seconds"), into the SPINE
   story it governs. A RULE that governs two stories goes in both.
4. An EXTENSION is its own story when it can ship later; otherwise fold it
   into its SPINE story.
5. Split a story too big for one iteration vertically: by kind of RULE, by
   workflow step, by input variation, by lifecycle (create, change, cancel)
   or by actor. Each half still runs end to end for the actor.

A story made only of RULEs ("retry checkout safely") cannot be built or
tested alone: fold it into the story whose SPINE they govern, as
"Revisions" says.

## Which Requirements need a story

| Requirement | Story |
|---|---|
| Functional, `**Must**`, `**Should**` or `**Could**` | At least one story lists it |
| Functional, `**Wont**` | None; it is out of scope |
| Nonfunctional or Constraint | Optional: list it in the story whose criteria it shapes ("the confirmation appears within 2 seconds"), otherwise leave it to the Tasks |

A story lists at least one Functional Requirement. A story of Nonfunctional
Requirements only ("as an operator I want p95 under 300 ms") is not written.

## Acceptance criteria

- A numbered list of pass/fail statements: each says what must hold, with a
  concrete boundary or outcome, so a reviewer can answer yes or no. Steps
  and test data belong to the test cases.
- Order them in four groups, and leave out a group with nothing in it:
  1. input and preconditions: what is accepted or required to start;
  2. state and output: what changes and what the actor sees;
  3. boundaries and idempotency: limits, edges, repeats;
  4. rejections and invariants: what is refused, and what never happens.
- Real values: "a card with a balance of 50 pays at most 50", not "a valid
  card pays".
- Each criterion ends with the links of the Requirements it shows. Each
  Requirement the story lists is shown by at least one criterion.
- A criterion shows a Requirement; it never adds behaviour. A behaviour the
  person wants that no Requirement states is a gap for `sdlc-write-spec`.

## INVEST check

Use it in the self review, one line per story. The last row is not an INVEST
letter; check it with the others.

| Letter | The story… | When it fails |
|---|---|---|
| Independent | can be built and demonstrated without another story | Merge the two, or cut along a different goal |
| Negotiable | states the need, not the design | Move design detail to `# Notes` or drop it |
| Valuable | gives the actor something they would notice | It is a Task; drop the story |
| Estimable | is clear enough for a team to size | Ask the person in the next round |
| Small | fits in one iteration | Split vertically, step 5 of "Splitting the Requirements into stories", never by layer |
| Testable | has criteria with real values | Rewrite the criteria |
| One actor, one surface | is one actor on one surface | Split by actor or surface |

## ChangeRequests

A ChangeRequest's stories list only its own Requirements, linked in its own
`overview.md`, and describe the change. When it changes a Requirement that a
Feature story lists (same key), name that Feature story under `# Affects` of
the story that lists the new text. Never edit the Feature's stories: they
describe the Feature as first delivered, and the tool writes `# Changed by`
on them.

## Revisions

Keep each existing story's key, even when its title changes: a Task may link
it, and a ticket may carry it.

A story this run touches for any reason is rewritten whole in the current
form: its criteria become pass/fail statements even where only one
Requirement changed. Which stories to touch is decided by the change; how a
touched story is written is decided here.

A story is deleted in two cases, and the log says why:

- its Requirements were all removed: drop the links to it from every Task's
  `# Stories` and every ChangeRequest story's `# Affects`;
- it was folded into another story (it held only RULEs of that story's
  SPINE): replace each link to it under a Task's `# Stories` or a
  ChangeRequest story's `# Affects` with a link to the story it was folded
  into, unless that link is already there, then drop it.

In earlier log entries, a link to the deleted story becomes its key as plain
text (`schema.md`, "`log.md`"). Log the link changes in each folder you
change. Those links are the only edit this skill makes outside its own
stories.
