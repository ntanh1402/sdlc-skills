# The wiki does not record test results, and no skill runs tests

The owner first asked for skills that cover build, review and test execution, and schema v2 gave every TestCase a required `lastResult` and an optional `lastRunAt` for a test-running skill to fill. On 2026-10-02 the owner decided that the wiki tracks which TestSuites and TestCases exist, what they cover and where their runnable code lives, and nothing about whether they pass. No skill runs tests or writes test code on its own; the two fields are removed from the TestCase type.

## Considered Options

- **A skill runs the tests and writes results through a Draft when a result changes.** Each change of result needs a branch and a pull request, and the wiki would then repeat what the test runner and CI already record.
- **Keep the fields for people to fill by hand.** A field nobody updates ends up stating a result that is no longer true.

## Consequences

- The recorded owner answer "build, review, test execution" becomes "build and review".
- Removing `lastResult` is a schema change that touches the sample and `sdlc-design-tests`, which writes `lastResult: not-run`; it ships after sub-project 3 is merged.
- TestSuite `status: Implemented` and `resource` stay: they say that runnable tests exist and where, not what they returned.
- Amended 2026-10-03: `sdlc-build-task` writes the unit tests that `conventions.md` requires and records nothing about them in the wiki. It never touches a TestCase or a TestSuite. Runnable code for TestCases, and setting a TestSuite to `Implemented`, belong to QA skills that are not designed yet. (This replaces "runnable test code is written together with the feature code by the build skill of sub-project 4".)
