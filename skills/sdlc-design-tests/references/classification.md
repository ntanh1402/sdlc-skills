# Test levels and test classification

## Test levels (suite types)

The suite type is the test level of a suite, its `suiteType`. This skill
designs two levels, both run by QA against a deployed environment:

- `integration`: one service through its entry points (endpoint, consumer,
  scheduled job, webhook, file intake), with its datastore, messages and
  externals, real or stubbed at the seam the suite names;
- `e2e`: actor outcomes across the deployed flow, through the owning frontend
  when there is one.

Unit tests are not designed here: developers write them with the code
(`sdlc-build-task`), and no case of this skill counts on them. Every rule a
unit test would prove in isolation (a field validation, a calculation, an
error mapping, a permission rule) is proved at `integration`, through the
entry point where its input enters. When the person asks for `unit` cases,
say so and design them at `integration`.

Load and security are not test levels: they are the `performance` and
`security` categories ("Testing types and categories" below). A `security`
case sits in the suite of the level it tests at: `integration` (an entry
point, a datastore or external boundary) or `e2e` (an actor's flow). A `performance` case, including a load profile, sits in the
`integration` suite (one service or boundary under load) or the `e2e` suite
(a deployed flow under load).

## Testing types and categories

Every case gets exactly one testing type, one category of that type, one
polarity and one priority, written in its information table (`case-format.md`):

| Testing type | Category | It checks |
|---|---|---|
| `functional` | `business-rule` | the business functions, rules, calculations, decisions and status transitions the acceptance criteria and Requirements state; what a screen shows, including its empty and loading states; the rejection of an operation that breaks a rule |
| `functional` | `field-validation` | each field of an input where it enters the system (API body, path, query and header; screen form; message or event payload; file record or batch row) against its constraints: mandatory or optional, data type, format, length, range, allowed values and cross-field rules |
| `functional` | `error-handling` | a failure of a datastore, queue, cache or external system (timeout, error response, unavailable, slow, malformed response, partial failure) and its retry, fallback or dead letter: the right error to the caller, the screen's error state, and a consistent state |
| `functional` | `data-integrity` | data created, updated, deleted, stored, mapped and synchronized across components and systems; response, message and file contracts; rollback and migration |
| `functional` | `idempotency` | a retried, replayed, redelivered or concurrent request has one effect only |
| `non-functional` | `security` | authentication, authorization, abuse, secrets, sensitive data and audit, as "Security cases" in `security-load-checklists.md` lists |
| `non-functional` | `performance` | latency, throughput, saturation and load profiles against a numeric target, as "Performance cases" in `security-load-checklists.md` lists |
| `non-functional` | `reliability` | recovery after a restart or failure without data loss |
| `non-functional` | `usability` | ease of use and accessibility of a screen |
| `non-functional` | `compatibility` | browsers, devices, client versions and schema versions |

The category is what the case's main assertion proves. When two fit, take
the first in this order: `security`, `performance`, `reliability`,
`field-validation`, `error-handling`, `idempotency`, `data-integrity`,
`business-rule`, `compatibility`, `usability`. For example: a missing
mandatory field is rejected, `field-validation`; an operation over a
business limit is rejected, `business-rule`; a dependency times out,
`error-handling`; the amounts two systems store match, `data-integrity`.

## Polarity

| Polarity | Expected result |
|---|---|
| `positive` | the stated success outcome, with every side effect checked |
| `negative` | the stated rejection or fallback, with the exact error, **and** proof that no business effect happened: the subject's amount, quantity and status did not move, and no business record, message, file or external call the success path makes was made. What the design says a rejection writes (a rejected or declined record, an audit or trace record, a failure event, an error log) is checked as written, with its values |

A `negative` case whose design states a fallback that still completes the
operation (a default value, a stand-in decision, a deferred or queued retry, a
cached answer) checks the effect of that fallback instead of "no business
effect": exactly the amount, status, record, message or retry the fallback
makes, with its values, and nothing the normal success path makes beyond it.

## Risk

`risk` is in the case's front matter, with the values `low`, `med`, `high`
and `critical` (not `medium`). It is what is lost if the behaviour the case
proves is broken in production:

| Risk | When a failure of the behaviour |
|---|---|
| `critical` | moves money, a balance or a quantity wrongly, loses or corrupts data, exposes sensitive data or lets an unpermitted actor in, on the main flow |
| `high` | breaks the main flow of an acceptance criterion or Requirement, or does any of the `critical` harms on an alternate or rare flow |
| `med` | breaks an alternate flow, a validation or a fallback, with no `critical` harm |
| `low` | breaks a message, a display or a rare edge case with no business effect |

## Priority

The values are `high`, `medium` and `low`. Start from the risk: `critical`
and `high` give `high`, `med` gives `medium`, `low` gives `low`. Then:

- the main `positive` path of each acceptance criterion or Requirement is
  `high`, whatever its risk;
- a `usability` or `compatibility` case is `low` unless its risk gives more.

## Techniques

Apply each technique that fits to every inventory item and every Requirement
it cites, and name it in the case's `# Purpose` with the name used here.

The standard techniques are applied as they are known, with these rules of
this skill:

- **Equivalence partitioning**: one case per class that behaves differently;
  the classes of an input field are in "Field validation" below.
- **Boundary value analysis**: min−1, min, min+1, max−1, max, max+1 of each
  limit (length, count, range, date); the values with the same expected
  result share one case, one test data row each.
- **State transition**: each allowed transition (`positive`), and each
  forbidden transition from each state (`negative`).
- **Decision table**, **Use case and scenario** and **Pairwise**: as they
  are known.

The techniques below are this skill's own; apply them as their row says:

| Technique | Apply when | Cases it produces |
|---|---|---|
| Asynchronous outcome | the result appears later than its cause (a message, a job, a callback, a cache or replica update) | the outcome found within the stated delay; the outcome still absent before the delay is over, when it matters |
| Time-based rules | an outcome depends on the clock: an expiry, a time to live, a cut-off, an end of day or month, a time zone, a schedule | just before, at and just after each time limit; a change of day, month or time zone; each value set with the clock or the stored time the environment allows |
| Numeric precision and rounding | the flow computes, converts or splits an amount, a rate or a quantity | the rounding rule at each half-unit; the smallest and largest allowed value; a conversion between units or currencies; the parts of a split that add up to the whole |
| Configuration and feature switches | a behaviour changes with a setting, a feature switch or a per-tenant option the design names | one case per value of the setting that changes the outcome |

These names are used for cases that the "Coverage rules" table or
`security-load-checklists.md` derive, with no rules of their own here:
**CRUD and data lifecycle** (the Table or datastore row), **Error guessing
and fault injection** (the External row; each case is `negative`),
**Idempotency and concurrency** and **Ordering and partial batches** (the
Endpoint, Subscription and job rows), **Security abuse cases** (the security
checklist).

## Coverage rules

An entry point is anything that starts the flow under test: an endpoint, a
screen, a consumer, a scheduled or batch job, a file intake or a webhook. A
scheduled job is triggered the way the environment allows (its schedule, a
manual run, an admin endpoint), and the case says which.

Each concept in scope gets the cases its row asks for, each one that exists
in its contract or design:

| Concept | Cases it needs |
|---|---|
| Endpoint | each response status of its contract; each exit of its `# Flowchart` and each rule of its `# Validations` (the packet's coverage check lists them); each input field ("Field validation" below); each side effect in the store, a message or an external call; authentication and authorization; an `idempotency` case when it can be retried or called twice at once; a contract change that older clients still meet (`compatibility`) |
| Subscription, consumer, Channel | each payload field as for an Endpoint; schema; each exit of its `# Flowchart`; messages in order, out of order and with a gap; a duplicate and a replayed message (`idempotency`); retry and its exhaustion; dead letter; a poison message; acknowledgement |
| Scheduled or batch job, file intake | its trigger; an empty run; one and many records; a record that fails in the middle (what the others do, what is retried); a run that overlaps the previous one; a restart after a crash (`reliability`) |
| Table or datastore | constraints; transactions and rollback when a later step fails; concurrent writes; migration; retention |
| External system, datastore, queue or cache the flow calls | at least one `error-handling` case: timeout, error response, unavailable, slow, malformed response, rate limit, partial failure; its retry, fallback and recovery |
| Frontend route or screen | its access rule; what it shows; its empty, loading, error and offline states |
| Alert, metric or audit record the design promises on a branch | a validation of its own in that branch's case |
| Decision or quality target | a case that proves the promised quality, or the suite that owns it |
| ChangeRequest Delta | for each existing behaviour it touches but does not change, one `positive` regression case or a link to an existing case that proves it; for a removed behaviour, a case proving it is gone |

And for every case:

- For each inventory item, think through both sides: the `positive` side
  (each real way it succeeds) and the `negative` side (each real way it can
  fail). Write a case for every branch you find on either side. Having both
  polarities is not required: when an item has no real failure branch, or
  no real success branch, do not add a case only to fill that polarity,
  because it duplicates a case that already proves the same behaviour.
- Every case is useful and testable: it proves a behaviour no other case
  proves, and a tester can set up its data, run its steps and see its
  expected result in the environment of its suite. A branch that cannot be
  triggered there is listed as uncovered, with its reason, not written as
  a case.
- Each input field of each entry point in scope has its `field-validation`
  cases, in the `integration` suite, at the entry point where the input
  enters, as "Field validation" below says. No field is left out because
  another layer (a frontend, a gateway, the code) is said to check it.
- Add `security` cases for every entry point that needs identity or a role,
  or handles sensitive data, even when no Requirement states it. Add other
  `non-functional` cases only from a stated Requirement, decision or risk.
  For each `security` and `performance` case, each line of
  `security-load-checklists.md` that applies to an entry point in scope has
  a case, or an uncovered row with its reason.
- One case checks one behaviour. Never merge a `positive` and a `negative`
  outcome in one case.
- Values of one partition that give the same expected result, such as the
  boundary values inside a limit, are rows of one case's test data, not one
  case each; the steps run once per row (`case-format.md`). A value whose
  expected result differs, such as another error code, is its own case.
- One behaviour has one case per level in the application. Before writing a
  case, look for an existing case, on the default branch or in an open test
  draft (the skill's step 1 says how to search them), in a suite of the same
  level, whose `# Covers` names the same Requirement and Design concept and
  whose purpose is the same branch. When one exists, do not write a new
  case: list the existing case in the coverage matrix of the input, with its
  test case ID. This holds across stories: two stories that cite the same
  Requirement share its cases.
- A behaviour proved at one level gets a case at another level only when
  that level proves something the first cannot. `e2e` proves the main
  `positive` path of each acceptance criterion or Requirement and each
  outcome the actor sees across the deployed flow; it does not repeat the
  `field-validation` and `error-handling` partitions an `integration` case
  already proves. An `e2e` case does check a validation or a failure the
  actor sees on a screen (the message, the form state), since the frontend
  adds a behaviour of its own.

## Field validation

The fields of an entry point come from its contract: the Endpoint's
`# Request` and `# Validations` (body, path, query and header), the
channel's `# Payload`, the file layout, or the Table columns a job reads.
List every field, nested ones by their full path (`items[].quantity`), with
each constraint the contract states. A constraint the contract does not
state (no maximum length, no format) is never invented: ask for it in the
first round, and list it as uncovered with its reason when there is no
answer.

For each field, check the rows that apply:

| Constraint | Values to send |
|---|---|
| Mandatory | the field absent; `null`; empty (`""`, `[]`, `{}`); only spaces, for text |
| Optional | the field absent, and the default the contract states applied |
| Data type | a value of another type (text for a number, a number for text, an object or a list for a single value, a decimal for an integer) |
| Format | each pattern the contract states (date, date and time with zone, email, phone, identifier, currency code, number of decimals): one valid value, and one value per way it can be malformed |
| Length | min−1, min, max, max+1 characters or items |
| Range | min−1, min, max, max+1; zero and a negative value for an amount or a quantity |
| Allowed values | each allowed value or group that behaves the same; an unknown value; the wrong letter case, when it matters |
| Cross-field rule | each combination the rule allows and each it forbids (a date range out of order, a field required only when another is set) |
| Unique or existing reference | a value that is already taken; an identifier that does not exist; one that belongs to another actor (also a `security` case) |
| Unknown field | a field the contract does not define, rejected or ignored as the contract says |
| Header | each required header (content type, idempotency key, correlation id, version) absent or malformed |
| Path and query | a parameter absent, malformed or out of range; an identifier that does not exist |

Group the rows into cases with the rule on values of one partition above:
one case per constraint and entry point when the expected result is the same
for every value, one data row per field or value, with the row's note naming
what the result points at (`(expect field: email)`). For example, one case
"Each mandatory field missing is rejected" with one row per mandatory field,
and one case "Each mandatory field null is rejected" when `null` gives
another error. A field whose error differs from the others is its own case.
Every valid boundary goes in one `positive` case with its rows. The design's
field matrix (the skill's step 4) shows every field, constraint and value
with the case that proves it.
