# Importing a test document

One run reads one document of test cases (a test plan, a sheet of manual
cases) and writes its cases as TestCases into the TestSuite of the Feature
they verify: `TS-<name>`, the Feature's key without `FEAT-`, created when it
does not exist. Read `test-suite.md`, `test-group.md`,
`test-case.md` and `reference.md` in `.wiki-llm/schema/` first.

Before anything else, check the prerequisite: a Feature the suite verifies is
on the default branch. If none is, stop and name the Feature import to run
first.

## 1. What to write

`tests/TS-<name>/` with:

| File | Content |
|---|---|
| `overview.md` | When new: `# Verifies` linking the Feature |
| `STORY-<name>/` or `GENERAL/` | Each group the cases go in, with the status below, `# References` linking the document's Reference, and one `**Import**` entry in its `log.md` |
| `STORY-<name>/TC-<id>-<name>.md` or `GENERAL/TC-<id>-<name>.md` | One per case in the document |

and the document itself as the Reference `references/REF-<document name>/`
(`SKILL.md` section 6).

Rules:

- **Status.** Each group the run writes is `Approved`, and the suite has no
  `resource`. When the person says its runnable tests exist, the groups are
  `Implemented` and the suite's `resource` says where they live.
- **`testType`** is the kind of test a case describes: `integration` or
  `e2e`; a security case carries `testCategory: security-validation`. Manual cases a tester performs through the user interface
  are `e2e`. Unit and load tests are never imported; list them under "Left
  out".
- **The group.** A case that proves one user story of the Feature goes in
  its group `STORY-<name>/`, when the person confirms the story, the
  acceptance criteria it proves and one Requirement of the story it covers;
  every other case goes in `GENERAL/`. A group this run creates gets an
  `overview.md` (`type: TestGroup`, the status below, `basedOn` of the
  Feature's version, `# Story` linking the story, or `# Scope` for
  `GENERAL`) and a `log.md`.
- **`testCategory`** is what the case checks (`test-case.md` lists the
  values), proposed and confirmed by the person.
- **The key** is `TC-<id>-<name>`: the id is the highest id in the suite + 1,
  and the name comes from the case's title.
- **The Reference** needs the person's approval of the whole folder, so the
  group that holds it cannot be saved as not checked.
- **A case with no observable expected result is not written.** List it under
  "Could not determine". Never complete it by guessing.
- **`# Steps`** keeps the document's steps, one row each, with the expected
  result and what is inspected. Each Action says by itself what to do,
  copies the values it needs, and uses real names, never a wiki key. The
  document's concrete data that must exist before the test goes in
  `# Preconditions`. A step that calls
  an API or publishes a message gets its `### Step <n>` block with the
  request and the expected response, as `test-case.md` says, when the
  document gives them.
- **Expected result and Validation** follow `test-case.md`: one checkpoint
  per table, topic, cache entry, page or group of API fields, `- <field>:
  <value>` lines joined with `<br>`; the Validation names each checked field
  in bold, or `validate` reports it.
- **`risk`** is the document's priority when it has one, mapped to `low`,
  `med`, `high` or `critical` and confirmed by the person; otherwise proposed
  and confirmed.
- **`# Covers`** links the Requirements the document or the person names for
  the case, by full path and anchor, after the story with its criteria
  (`— AC 1, 3`) for a case in a `STORY-*` group; otherwise the Design
  concepts the case exercises.
- The group links the Reference under `# References`; a case links it too
  when its steps come from a part a tester should read.
- **One document, several Features.** A document that holds cases for
  several Features is imported one Feature per run. The first
  run writes the Reference; the later runs link it.

## 2. What to ask

- Which Feature the suite verifies.
- Whether runnable tests exist for these cases, and where.
- The document's date, and any case known to be out of date. Leave such a
  case out and list it.

## 3. Before the Design gate

Check by reading:

- every case in the document is a TestCase or is in a list, with the reason;
- every step has an expected result and a validation;
- the Reference's content file is the whole document.
