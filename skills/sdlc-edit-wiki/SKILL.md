---
name: sdlc-edit-wiki
description: Make a small edit to the project wiki that no lifecycle skill owns - fix a typo or wording, change the glossary or the conventions, mark a Feature released or deprecated, add a Task's or a user story's ticket link, add a Task's pull request link, or record that a person confirmed a file. Use for small corrections of wording and for these status and link changes. Not for requirements, architecture, tasks, test design, corrections against code or documents, or closing a Task - those belong to the lifecycle skills, and this skill names the right one.
---

# Edit the wiki

This skill makes the small edits that no lifecycle skill owns, in one draft
`wiki/edit-<key>`. It refuses every other edit and names the skill that owns
it. The list below is short on purpose: a wiki change that carries a
decision goes through the skill that asks for that decision.

## Before you start

Read, in this skill's folder, `references/read-protocol.md`,
`references/flow.md` and `references/write-protocol.md`. This skill uses the
**short form** of `flow.md` section 8: no rounds and no Run plan, one stop
that is the Intent and the Design gate together, then the Change-set gate.
Then read `schema.md` ("Corrections", "Pending changes") and the schema page
of each type you will edit, in the wiki's `.wiki-llm/schema/`.

## 1. What this skill edits

| Allowed | Rule |
|---|---|
| A typo or a wording fix in any file a person writes | The meaning of a contract, a Requirement or an acceptance item does not change |
| The Application's `glossary.md` and `conventions.md` | Terms, roles and rules, added, changed or removed |
| A Feature's status to `Released` or `Deprecated` | Only when none of its Tasks is `Todo` and no Design file has a pending entry for it; `Released` only from `InDev`, with `releasedAt` set to the time the person gives |
| A Task's `trackerKey`, `resource` and `prUrl` | The ticket and the pull request a person followed by hand. Never its status |
| A user story's `trackerKey` and `resource` | The ticket a person made from the story's paste-ready copy |
| A `verified` stamp | The person says they read the file and it is right: `$T verify <path>` in the draft worktree |

| Refused | Say |
|---|---|
| A new or changed Requirement | `sdlc-write-spec` |
| A new target design, a new Design concept, a changed contract | A ChangeRequest with `sdlc-write-spec`, then `sdlc-design-arch` |
| A user story added, regrouped or deleted, or its criteria changed | `sdlc-write-stories` |
| A Task added, or a Task's scope, acceptance or stories changed | `sdlc-plan-tasks` |
| A TestCase or a TestSuite | `sdlc-design-tests`; `sdlc-import` for a correction |
| A Task's status | `sdlc-close-task`, after its code is merged |
| The wiki is wrong about what is built | `sdlc-import` on the code or the document: it compares and corrects |
| A Feature's or ChangeRequest's status other than `Released` or `Deprecated` | The lifecycle skill of that step |
| A question about the wiki | `sdlc-ask-wiki` |

A refusal is not a question. Three rules decide the cases the tables do not
name:

- **Does the edit change what someone would build or test?** If a developer
  or a tester would do anything differently after the edit, it is not a
  wording fix. Refuse it and name the skill.
- **A file that holds a target not built yet** (a `Planned`, `Modifying` or
  `Removing` Design file, a Feature before `Released`) is never edited in a
  way that changes that target. A typo there is still a typo.
- **A request that mixes both** is split: do the allowed part, and list the
  rest under "For other skills" with the skill for each.

## 2. Look up, and ask only when needed

Find the file or files on the default branch, and read them. Ask only what
the request leaves undecided: which of two matching files, the exact new
wording when the person gave only the fault, the release time. One question,
with your proposal.

For `Released` or `Deprecated`, read the Feature's Tasks, and find the
Design files that still have a pending entry for it:
`grep -rl "features/<Feature key>/overview.md" "wiki/<app>"`, then keep those
whose `# Pending changes` section links it. `validate` refuses a Feature that
is neither `Approved` nor `InDev` while such an entry exists
(`pending.parent-open`), and this skill never removes an entry. So refuse when:

- for `Released`, a Task is `Todo`: name the Tasks, and say each is closed
  with `sdlc-close-task` after its code is merged;
- for `Deprecated`, a Task is `Todo` or an entry is left: name them. No skill
  withdraws an approved design; a person removes the entries, the `Planned`
  files and the `Todo` Tasks by hand, then asks again;
- for `Released`, an entry is left with no `Todo` Task: name the files; a
  close that is not merged yet usually explains it.

## 3. One stop: the Intent and the Design gate

Show the exact changes, file by file, as the old text and the new text, and
what is refused and where it goes. Ask for approval.

```text
Edit FEAT-catalog:
  features/FEAT-catalog/overview.md   status InDev → Released; releasedAt 2026-10-04T00:00:00+07:00
  features/FEAT-catalog/log.md        a Released entry
Not done here: "add a requirement for search filters" is sdlc-write-spec.
Approve?
```

An edit here is shown again. A rejection writes nothing.

## 4. Write, finish and commit

The draft key is `edit-<key>`: the key of the concept that holds the main
file (`edit-FEAT-catalog`, `edit-TASK-sms-channel`, `edit-SVC-orders`), or a
short name for an Application file (`edit-glossary`, `edit-conventions`).
Start it as `references/write-protocol.md` section 3 says. The input paths
are the files you edit.

Write exactly the approved changes. Add an entry to the `log.md` of each
concept folder you changed, saying what changed and who asked:

```markdown
* **Edit**: Reworded the summary; no contract changed. Written by an AI model with sdlc-edit-wiki.
* **Released**: The Feature is live since 2026-10-04. Written by an AI model with sdlc-edit-wiki.
```

The Application's own files have no log; the commit message says what
changed. Never write `generated`, a section the tool writes, or an
`index.md`.

Then follow `references/write-protocol.md` section 4 from step 5: the input
check, `draft finish`, the Change-set gate, `draft commit`. Commit message:
`edit(<key>): <what changed>`, for example
`edit(FEAT-catalog): released on 2026-10-04`.

End with the summary of the short form: "Done" and "Next", and "For other
skills" when part of the request was refused.

## 5. What this skill never does

- It never changes a Requirement, a contract, an acceptance item, a planned
  scope, a TestCase or a diagram's meaning.
- It never changes a Task's status, and never a status other than a
  Feature's `Released` or `Deprecated`.
- It never adds a `# Pending changes` entry or removes one.
- It never reads code to decide what the wiki should say.

## Done when

- Every change made is in the "Allowed" table, and every refused part was
  named with its skill.
- The exact changes were approved before the draft was started.
- `draft finish` was `ok`, the change set was approved, and `draft commit`
  reported the branch.
