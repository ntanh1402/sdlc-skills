# The checks of a code change

A code change is checked against the wiki by reading: the Task's
`# Acceptance` and `# Planned scope`, the Design files linked there, and the
Application's `conventions.md`. A Design file with a `# Pending changes`
section holds the **target**, what the system will be once the pending work
is built; the code is checked against the target. No check runs the code or
its tests.

## The groups

| Group | A finding is | Severity |
|---|---|---|
| Acceptance | An item of the Task's `# Acceptance` the change does not meet | `must fix` |
| Contract | A place where the code and a Design file in scope disagree: a field, its type, whether it is required, a status code, a validation, a behaviour step, a payload, a column, an index, a timeout | `must fix` |
| Outside the scope | A contract the change alters whose Design file is not in the Task's `# Planned scope`; or a contract the wiki has no file for: a new endpoint, table, channel or vendor call | `must fix` |
| Convention | A rule of `conventions.md` the change breaks | `should fix` |
| Not checked | What you could not check, and why; and differences that belong to other pending work, with its key | — |

## Rules

- Check only what the change does. Code the change did not touch is not
  checked; a difference there is Drift, and `sdlc-import` finds it.
- A finding needs evidence on both sides: the code location and the wiki
  path. With evidence on one side only, it goes to "Not checked".
- An acceptance item that reading cannot decide (a performance number, a
  behaviour only a running system shows) goes to "Not checked": say what
  would decide it.
- Style, naming or design taste is not a finding unless `conventions.md`
  states the rule.
- A Reference is context, never evidence: code that differs from a code
  example, or from a document a Reference holds, is not a finding unless the
  Task, a Design file or `conventions.md` states the same rule.
- Never copy a secret or personal data from the code into a report, a Run
  plan or a commit message.

Running the checks never changes the wiki. When the wiki is the wrong side,
the remedy is a ChangeRequest with `sdlc-write-spec` when the design should
change, or `sdlc-import` on the code folder when the wiki records what is
built wrongly.
