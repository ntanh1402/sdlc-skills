---
name: sdlc-review-code
description: Review a code change against the project wiki, read-only - check a branch or working tree against its Task's acceptance, the contracts in the wiki's Design files (endpoints, events, tables, vendor operations), the Task's planned scope and the Application's conventions, and report each finding as must fix or should fix with the code location and the wiki path. Use when a developer asks to review code, a branch or a pull request against the project wiki, a Task, the spec or the design. Not for a general code review without a wiki, for fixing code, for running tests, or for changing the wiki.
---

# Review code against the wiki

Read-only. This skill reads a code change and the wiki, and reports in the
chat where they disagree. It never edits code, writes to the wiki, changes a
Task's status, runs tests or posts to a hosting service. It gives no verdict:
each finding is `must fix` or `should fix`, and a person decides whether the
code is merged.

Read `references/read-protocol.md` in this skill's folder and follow it: it
finds the wiki, says how to read the default branch, and where the schema
pages are. Read the schema page of a type before relying on its headings or
statuses. When no wiki is linked, stop as the read protocol says.

Other requests go elsewhere; say so and stop:

| Request | Answer |
|---|---|
| Fix the code, or write it | Not this skill: it reports findings only. `sdlc-build-task` writes the code of a Task |
| Record that the change is merged | `sdlc-close-task` |
| The wiki is wrong about what is built | `sdlc-import` on the same folder compares and corrects it |
| The design or the user stories should change | A ChangeRequest with `sdlc-write-spec` |
| A question about the wiki | `sdlc-ask-wiki` |
| Review a wiki draft or its pull request | Not a skill: the approval gates and the pull request are that review |
| A general code review, with no wiki to check against | Not this skill |

## 1. The input

| Input | Rule |
|---|---|
| The code folder | The user names it. "This folder" is an answer. Never guess it |
| The branch to compare against | The repository's default branch, unless the user names another |
| A Task key | When there is one. If the user gave none, ask once: "Which Task does this change build? None is an answer." |

Find the change (`SRC` is the code folder):

```bash
BASE=$(git -C "$SRC" symbolic-ref --quiet --short refs/remotes/origin/HEAD \
  || { git -C "$SRC" show-ref --verify --quiet refs/heads/main && echo main; } \
  || echo master)
FROM=$(git -C "$SRC" merge-base "$BASE" HEAD)
git -C "$SRC" diff --stat "$FROM"       # commits on the branch and uncommitted edits
git -C "$SRC" status --porcelain        # new files not added yet are part of the change
```

The change is everything between `FROM` and the working tree. When it is
empty, say so and stop. Read the changed files in full where the diff alone
does not show what the code does.

## 2. What to read in the wiki

Read the wiki's default branch.

**With a Task.** Find the Task file:
`git ls-tree -r --name-only "$DEFAULT" -- wiki | grep '/TASK-<name>.md$'`.
A Task is unique inside its Application; when several Applications have one
with that key, ask which. Read:

- its `# Acceptance`, and the Requirements the acceptance links;
- its `# Planned scope`, and every Design file linked there;
- the Feature or ChangeRequest that owns the Task, for context.

A Design file with a `# Pending changes` section holds the **target**: what
the system will be once the pending work is built. Review the code against
the target.

**Without a Task.** Find the Service or frontend whose `resource` is this
repository. Compare URLs in one form, `https://<host>/<org>/<repo>` with no
`.git` and no trailing slash; get the code's URL with
`git -C "$SRC" remote get-url origin`. In a repository with several services,
every `resource` that starts with the repository URL is a candidate; the
changed paths say which one. Then read the Design files of what the change
touches: the Endpoints whose handlers changed, the Tables whose migrations or
queries changed, the Channels it publishes or consumes, the vendor Operations
it calls.

When no Service or frontend matches, say so under "Not checked": "this
repository is not in the wiki; import it with sdlc-import".

**Always.** The Application's `conventions.md`, when it exists, and the
References the Task and the Design files link under `# References`, as
context only (`references/code-checks.md`).

## 3. Whose work a target is

A Design file with `# Pending changes` describes what will be built, and
several Tasks may build one file. A difference between the code and such a
file is this change's finding only when this Task covers the file and no
other work shares it.

- **With a Task.** For each file in its `# Planned scope` that has pending
  entries, check two things: whether another Task that is not `Done` also
  links the file in its `# Planned scope`
  (`grep -rl "<KEY>" wiki/ --include='TASK-*.md'`), and whether the file has a
  pending entry of another Feature or ChangeRequest. If either is true, a
  difference goes to "Not checked", with that Task's or request's key, unless
  this Task's `# Acceptance` states it.
- **Without a Task.** Every difference in a file with `# Pending changes`
  goes to "Not checked", with the Feature or ChangeRequest the entry names.
  Ask for the Task.

## 4. The checks

Read `references/code-checks.md` in this skill's folder: it holds the five
groups (acceptance, contract, outside the scope, convention, not checked),
the severity of each and the rules for a finding. `sdlc-build-task` holds the
same file and fixes what the checks find; this skill only reports.

## 5. The report

Report in the chat, in the order of the groups, one line per finding. Each
finding cites the code location and the wiki path. The last line counts the
findings. Say which wiki branch and commit you read.

```text
Reviewed feature/refund against main for TASK-refund-endpoint. Wiki: main at 4c1e9a2.

Acceptance
  must fix    "returns 409 when the order is already refunded": not implemented.
              src/api/refund.py:40 · wiki/shop/features/FEAT-refunds/TASK-refund-endpoint.md
Contract
  must fix    EP-refund.md says `reason` is required; the code accepts it missing.
              src/api/refund.py:31 · wiki/shop/services/SVC-orders/EP-refund.md
Outside the scope
  must fix    The migration adds column `refunded_at` to `orders`; TBL-orders is not in the Task's planned scope.
              migrations/0009_refunds.sql:3 · wiki/shop/datastores/DB-shop/TBL-orders.md
Convention
  should fix  conventions.md asks for a test per endpoint; none was added.
              wiki/shop/conventions.md
Not checked
  The p95 latency in the acceptance: only a load test shows it.

3 must fix, 1 should fix.
```

With no finding in a group, write "none" under it. Never add a verdict such
as "approved" or "ready to merge".

When the review was made against a Task, end with one line: after the merge,
the Task is closed in the wiki with `sdlc-close-task`.

## 6. When the person says the wiki is the wrong side

Name the remedy and change nothing:

- the design should be different: a ChangeRequest with `sdlc-write-spec`;
- the wiki records what is built wrongly: `sdlc-import` on the same folder.

The finding stays in the report until the wiki changes.

## Done when

- The change, the base and the wiki commit are named.
- Every acceptance item is met, a finding, or under "Not checked".
- Every finding cites a code location and a wiki path.
- Nothing was written: no code, no wiki file, no comment on a hosting
  service.
