# Importing test code

One run reads one suite of runnable tests and writes its tests as TestCases,
one per test, into the TestSuite of the Feature they verify: `TS-<name>`,
the Feature's key without `FEAT-`. The run creates the suite when it does
not exist. Read `test-suite.md`, `test-group.md` and `test-case.md` in
`.wiki-llm/schema/` first.

Read only. Never run the tests.

Before anything else, check the prerequisite: a Feature the suite verifies is
on the default branch. `# Verifies` links exactly one. If none is, stop and
name the Feature import to run first.

## 1. Which tests

- Each case's `testType` is `integration` or `e2e`; a security test is an
  `integration` or `e2e` case with `testCategory: security-validation`.
- **Unit and load tests are refused:** "unit and load tests are not
  imported". When the folder holds them beside other tests, import only the
  other tests and say which folders were left out.
- **One Feature per run.** When the folder holds tests of several Features,
  list them and ask which Feature this run imports.

## 2. What to write

`tests/TS-<name>/` with:

| File | Content |
|---|---|
| `overview.md` | When new: `framework`, `resource` set to where the tests live, and `# Verifies` linking the Feature |
| `STORY-<name>/` or `GENERAL/` | Each group the cases go in, `status: Implemented`, with one `**Import**` entry in its `log.md` |
| `STORY-<name>/TC-<id>-<name>.md` or `GENERAL/TC-<id>-<name>.md` | One per test |

Rules for a TestCase:

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
  and the name comes from the test's own name: `test_double_submit_is_one_order`
  gives `TC-4-double-submit-is-one-order`.
- **`# Steps`, `# Preconditions`, `# Postconditions and cleanup`** are read
  from the test's code: its setup and fixtures (the data that must exist),
  each action with what it asserts, its teardown. Every step needs an
  observable expected result and what is inspected; they are the test's
  assertions. Each Action says by itself what to do, with the real names of
  the tables, topics and endpoints the test uses, never a wiki key. A step
  that calls an API or publishes a message gets its `### Step <n>` block
  with the request the test sends and the fields it asserts, as
  `test-case.md` says.
- **Expected result and Validation** follow `test-case.md`: one checkpoint
  per table, topic, cache entry, page or group of API fields, `- <field>:
  <value>` lines joined with `<br>`; the Validation names each checked field
  in bold, or `validate` reports it.
- **A test with no assertion** has no expected result, so its case is not
  written. List it under "Could not determine".
- **`risk`** is proposed and confirmed by the person.
- **`# Covers`** links the Requirements the person confirms the test proves,
  by full path and anchor, after the story with its criteria
  (`— AC 1, 3`) for a case in a `STORY-*` group. When the person names none, link the Design
  concepts the test exercises (the Endpoint it calls, the Table it checks).
  Never guess a Requirement from a name.
- **`sources`** names the test file and the commit.
- Fixture data is described, not copied, when it holds a secret or a real
  person's data.

## 3. Comparing with a suite that exists

When the suite is already in the wiki, follow `compare.md`. One case is
special: a group that is `Draft` or `Approved` was designed before its tests
were written. A TestCase there with no test in the code is **not written
yet**: report it, never offer it for deletion. When every designed case of a
group has a test, tell the person the group may be set to `Implemented`;
that edit is theirs to approve at the Design gate.

## 4. What to ask

- Which Feature the suite verifies, and for each test or group of tests which
  Requirements it proves.
- The risk of each case, proposed from what the test protects.
