# Importing a test document

One run reads one document of test cases (a test plan, a sheet of manual
cases) and writes one TestSuite with its TestCases. Read `test-suite.md`,
`test-case.md` and `source-document.md` in `.wiki-llm/schema/` first.

Before anything else, check the prerequisite: a Feature the suite verifies is
on the default branch. If none is, stop and name the Feature import to run
first.

## 1. What to write

`tests/TS-<name>/` with:

| File | Content |
|---|---|
| `overview.md` | `suiteType`, `# Verifies` linking the Feature, and the status below |
| `<document name>.md` | The document's Markdown copy as a Reference, with the images it links |
| `TC-<name>.md` | One per case in the document |
| `log.md` | One `**Import**` entry |

Rules:

- **Status.** The suite is `Approved` and has no `resource`. When the person
  says its runnable tests exist, it is `Implemented` and `resource` says where
  they live.
- **`suiteType`** is the kind of test the cases describe: `integration`,
  `e2e`, `load` or `security`. Manual cases a tester performs through the
  user interface are `e2e`. Unit tests are never imported.
- **The Reference** needs the person's approval of the whole body, so the
  group that holds it cannot be saved as not checked.
- **A case with no observable expected result is not written.** List it under
  "Could not determine". Never complete it by guessing.
- **`# Steps`** keeps the document's steps, one row each, with the expected
  result and what is inspected. `# Test data` gives the document's concrete
  values.
- **`risk`** is the document's priority when it has one, mapped to `low`,
  `med`, `high` or `critical` and confirmed by the person; otherwise proposed
  and confirmed.
- **`# Covers`** links the Requirements the document or the person names for
  the case, by full path and anchor; otherwise the Design concepts the case
  exercises.
- The suite and every case name the Reference in `sources`
  (`resource: <document name>.md`).
- **One document, several suites.** A document that holds cases of several
  types, or for several Features, is imported one suite per run; the
  Reference lives in the first suite's folder.

## 2. What to ask

- Which Feature the suite verifies.
- Whether runnable tests exist for these cases, and where.
- The document's date, and any case known to be out of date. Leave such a
  case out and list it.

## 3. Before the Design gate

Check by reading:

- every case in the document is a TestCase or is in a list, with the reason;
- every step has an expected result and a validation;
- the Reference is the whole document.
