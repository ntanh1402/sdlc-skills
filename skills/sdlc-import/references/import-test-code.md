# Importing test code

One run reads one suite of runnable tests and writes one TestSuite with one
TestCase per test. Read `test-suite.md` and `test-case.md` in
`.wiki-llm/schema/` first.

Read only. Never run the tests.

Before anything else, check the prerequisite: a Feature the suite verifies is
on the default branch. `# Verifies` needs at least one. If none is, stop and
name the Feature import to run first.

## 1. Which tests

- `suiteType` is `integration`, `e2e`, `load` or `security`.
- **A unit test suite is refused:** "unit tests are not imported". When the
  folder holds unit tests beside other tests, import only the other tests and
  say which folders were left out.
- **One suite per run.** When the folder holds several suites (several types,
  or several features), list them and ask which one this run imports.

## 2. What to write

`tests/TS-<name>/` with:

| File | Content |
|---|---|
| `overview.md` | `status: Implemented`, `suiteType`, `framework`, `resource` set to where the tests live, and `# Verifies` linking the Feature |
| `TC-<name>.md` | One per test |
| `log.md` | One `**Import**` entry |

Rules for a TestCase:

- **The key** comes from the test's own name: `test_double_submit_is_one_order`
  gives `TC-double-submit-is-one-order`.
- **`# Steps`, `# Preconditions`, `# Test data`, `# Postconditions and
  cleanup`** are read from the test's code: its setup, each action with what
  it asserts, its fixtures, its teardown. Every step needs an observable
  expected result and what is inspected; they are the test's assertions.
- **A test with no assertion** has no expected result, so its case is not
  written. List it under "Could not determine".
- **`risk`** is proposed and confirmed by the person.
- **`# Covers`** links the Requirements the person confirms the test proves,
  by full path and anchor. When the person names none, link the Design
  concepts the test exercises (the Endpoint it calls, the Table it checks).
  Never guess a Requirement from a name.
- **`sources`** names the test file and the commit.
- Test data is described, not copied, when it holds a secret or a real
  person's data.

## 3. Comparing with a suite that exists

When the suite is already in the wiki, follow `compare.md`. One case is
special: a suite that is `Draft` or `Approved` was designed before its tests
were written. A TestCase there with no test in the code is **not written
yet**: report it, never offer it for deletion. When every designed case has a
test, tell the person the suite may be set to `Implemented`; that edit is
theirs to approve at the Design gate.

## 4. What to ask

- Which Feature the suite verifies, and for each test or group of tests which
  Requirements it proves.
- The risk of each case, proposed from what the test protects.
