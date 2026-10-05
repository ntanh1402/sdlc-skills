---
name: sdlc-write-stories
description: Break the approved Requirements of a Feature or ChangeRequest in the project wiki into user stories - one actor goal each, "As a … I want … so that …", with Given/When/Then acceptance criteria that cite the Requirements, and a paste-ready copy for the tracker. Use when a business analyst wants user stories, a story breakdown or story acceptance criteria for requirements that are approved for design, or wants existing stories regrouped. Not for writing or changing Requirements, architecture, tasks, test design, tracker sync or code.
---

# Write the user stories

This skill is a lifecycle step after the Requirements are approved. It runs
at the same time as `sdlc-design-arch` on the same target; neither waits for
the other. It takes a Feature or ChangeRequest and writes `STORY-<name>.md`
files into its folder, so that every Functional Requirement that is not
**Wont** is listed by at least one story.

Stories are optional: a Feature or ChangeRequest without them is planned,
tested and built as before. A story groups Requirements; it never adds
behaviour. The Requirements stay the testable unit.

Its draft prefix is `stories-`: the draft for `FEAT-coupons` is
`wiki/stories-FEAT-coupons`.

## Before you start

Read, in this skill's folder, `references/read-protocol.md`,
`references/flow.md` and `references/write-protocol.md`. `flow.md` gives the
steps of the run and the three gates; this file says what is this skill's own
at each step. Then read `references/story-rules.md`,
`references/story-format.md` and `references/paste-format.md`, and the schema
pages `schema.md`, `user-story.md`, `feature.md`, `change-request.md` and
`task.md` in the wiki's `.wiki-llm/schema/`.

| Request | Skill |
|---|---|
| New or changed Requirements, or a criterion no Requirement supports | `sdlc-write-spec` |
| Architecture | `sdlc-design-arch` |
| Build tasks, or linking Tasks to stories | `sdlc-plan-tasks` |
| Test cases or suites | `sdlc-design-tests` |
| Create or update tickets in the tracker | No skill does: a person pastes the story and may add `trackerKey` and `resource` to it (`sdlc-edit-wiki`) |
| Show a story, or its paste-ready copy again | `sdlc-ask-wiki` |
| A typo in a story | `sdlc-edit-wiki` |

## 1. Look up: readiness and the inventory

Accept one `FEAT-*` or `CR-*` key, or find it as `sdlc-write-spec` does
(a key the user gave, an exact title, the Feature whose outcome owns the
behaviour). Read it on the default branch:

| State | When | Do |
|---|---|---|
| `READY` | A Feature `ReqApproved`, `Approved` or `InDev`, or a ChangeRequest `ReqApproved` or `Approved`; and `coverage stories` reports Requirements, or the person asks to revise the stories | Go on |
| `NEEDS_SPEC` | `Draft` or `Proposed` | Stop: route to `sdlc-write-spec` |
| `NOT_MERGED` | Not on the default branch, but a `wiki/*-<Key>` draft exists | Stop and name the draft |
| `CLOSED` | A Feature `Released` or `Deprecated`, or a ChangeRequest `Implemented` or `Rejected` | Stop: a change to a Released Feature goes through a ChangeRequest (`sdlc-write-spec`) |
| `ALREADY_CURRENT` | `coverage stories` reports nothing and the person asks for nothing to change | Report the stories and stop |

```bash
$T coverage stories --feature FEAT-coupons      # or --change CR-sms-alerts
```

Every state but `READY` is a refusal, not a question.

Then read the Requirements, the PRD (`prd.md` or `change-prd.md`), the
stories already in the folder, and the Tasks that link them. For a
ChangeRequest, also read the changed Feature's stories that list a
Requirement the ChangeRequest changes (same key).

Build the inventory: each Requirement with its key, priority and type,
marked **needs a story** (Functional, not **Wont**) or **optional**; and the
actors and goals the PRD names.

## 2. Questions and the Intent gate

Ask in rounds, as `references/flow.md` section 4 says. The first round names
the target and its state, shows the inventory, and proposes the stories: key,
actor, goal and the Requirements each lists, split as
`references/story-rules.md` says. It asks the choices that are the person's:

- where one goal is cut into two stories;
- which actor a story is for when the PRD names several;
- the priority of each story;
- for a ChangeRequest, which Feature stories it affects.

When the brief or the person already names stories, take them as given, with
their wording: propose only the tracing, and report what they leave
uncovered. Do not split, merge or reword them yourself.

A criterion the person wants that no Requirement supports is not written. It
is a gap in the Requirements: name it under "For other skills" for
`sdlc-write-spec`. When the stories cannot be written without it, stop before
the Intent gate and name `sdlc-write-spec` as the skill to run first.

The wiki question's usual answer is "nothing: only story files and the
folder's log".

**Intent gate.** Restate the target, the inventory and the proposed stories
(key, actor, goal, Requirements). Ask for approval.

## 3. Run plan and the Design gate

Start or resume the draft `stories-<Key>` as `references/write-protocol.md`
section 3 says. The input paths are the target's `overview.md` and, for a
ChangeRequest, the changed Feature's `overview.md` and the Feature stories it
affects.

Prepare every story in full, with `references/story-format.md`: the
sentence, the numbered criteria with real values, the Requirements, and for
a ChangeRequest `# Affects`. Prepare the coverage matrix: each Requirement of
the inventory to the stories that list it, and each optional Requirement no
story lists.

Write the Run plan. Its `## Files` are one line per story file, added,
changed or deleted, with its goal in a few words, each Task or other story
whose link to a deleted story is dropped, and each `log.md` changed.

**Design gate.** Show every story as it will be written, never only a
summary, then the coverage matrix, then the Run plan. Ask for approval.

## 4. Write

In the draft worktree, in the Feature's or ChangeRequest's folder, write each
story as `STORY-<feature-name>-<name>.md`. In a revision, keep each existing
story's key. Delete a story whose Requirements were all removed, say why in
the log, and drop the links to it from every Task's `# Stories` and every
ChangeRequest story's `# Affects`, with a log entry in each folder changed. Add an entry to the folder's `log.md`, for example
`* **Stories**: Wrote 3 user stories. Written by an AI model with sdlc-write-stories.`

Do not touch `overview.md`, the PRD or the changed Feature's stories, and
change a Task only to drop a link to a deleted story. Linking Tasks to the
stories is `sdlc-plan-tasks`. Do
not write `index.md` or `# Changed by`: `draft finish` does.

**Input check.** `sdlc-design-arch` may merge while this draft is open, and
it writes the same `overview.md` (its `# Architecture` or `# Delta`, and the
status). When the input check of `references/write-protocol.md` shows that
file changed, compare only its `# Requirements` between `READ` and the
default branch. The same Requirements: the input did not change for this
step; go on. Different: show what changed and go back to step 3.

## 5. Self review, finish and commit

Follow `references/write-protocol.md` section 4 from step 5. In the self
review, also check that:

- `$T coverage stories`, run in the worktree, reports nothing;
- `$T validate` reports no `story.*` or `ids.story-format` finding;
- each story is one actor's goal and passes the INVEST check of
  `references/story-rules.md`;
- each criterion has real values and cites only Requirements its story
  lists;
- no file outside the story files and the folder's `log.md` changed, except
  a dropped link to a deleted story and its log entry.

Commit message: `stories(<Key>): <n> user stories`, for example
`stories(FEAT-gift-cards): 3 user stories`.

Before the summary, print the paste-ready copy of each story added or
changed, as `references/paste-format.md` shows. It is not written to the
wiki. Then the summary. "Next" is "`sdlc-plan-tasks` once the design is
merged"; when the folder already has Tasks, "run `sdlc-plan-tasks` again to
link the stories".

## Done when

- The target and the proposed stories were confirmed in the rounds, and the
  intent was approved at the Intent gate.
- Every story was shown in full and approved at the Design gate.
- Every Functional Requirement that is not **Wont** is listed by a story;
  every criterion cites a listed Requirement, and every listed Requirement is
  cited.
- The self review found nothing it could not fix, or the person accepted what
  was left at the Change-set gate.
- `coverage stories` reports nothing, `draft finish` was `ok`, the change set
  was approved, `draft commit` reported the branch, and the paste-ready copy
  was printed.
