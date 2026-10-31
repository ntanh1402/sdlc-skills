# Writing an import draft to the project wiki

This file says how `sdlc-import` drafts, checks, approves and commits its
changes to the wiki. `SKILL.md` says what to write; this file says how.
Read it when `SKILL.md` section 1 finds an unfinished draft, or at section 4.

## 1. The rules

- Every change goes into a **draft**: a branch `wiki/import-<target>` with its
  own worktree in `WIKI/.worktrees/import-<target>/`. The default branch changes
  only when the user merges the draft's pull request.
- One Import source is one draft and one pull request. It reads only what is
  already merged into the default branch.
- Stop at the three **approval gates** of `SKILL.md`: Intent, Design (taken
  group by group) and Change-set. No draft is started before the Intent gate is
  approved (and for a compare run, no draft is started unless there is
  something to write or to confirm).
- Never merge, never open a pull request, never call a hosting service; the
  user does that.
- Edit only what a person writes. Never edit an `index.md`, a TestSuite's
  `checklist.csv` or a reverse section the schema page marks as written by the
  tool (`# Used by`, `# Publishers`, `# Subscribers`, `# Change history`,
  `# Superseded by`); `draft finish` writes those.
- A compare run edits existing files when the person chooses "take what the
  Import source says": that edit is a **correction** (`schema.md`,
  "Corrections"). It may edit only a file that records what exists (`Active`
  Design file, `Released` Feature, `Accepted` decision, TestSuite/TestCase, or
  Application file) — never a file that holds a target not built yet. When a
  correction removes a Requirement, fix the user stories (`user-story.md`) and
  TestCases (`test-case.md`) that list it in the same draft. Adding or removing
  a `# References` entry is allowed on any file the run writes.
- Keys are names taken from the Import source's own names or titles, never
  numbers: `SVC-orders`, `EP-create-order`, `TBL-orders`. A key on the default
  branch never changes. Before the pull request is merged,
  `$T rename <old> <new>` changes one.

## 2. The draft key

The key is `import-<target>` as `SKILL.md` section 2 defines for each kind of
Import source:

```text
import-SVC-orders    import-WEB-shop    import-architecture-overview    import-FEAT-checkout    import-TS-orders-e2e    import-REF-domain-guide
```

**First, look for a worktree.** When `WIKI/.worktrees/import-<target>/` exists,
an earlier run started this draft and did not commit it. Never discard it and
never start it again: a draft with no commit yet passes the "merged" test of
case 3 below, and its files and its `plan.md` exist nowhere else.

- It holds a `plan.md`: `cd` into it and resume as section 4 ("Resuming")
  says.
- It holds no `plan.md`: show the user `git status` in it and ask whether to
  go on from those files or to discard them.

Otherwise decide what to do after `git fetch --quiet origin 2>/dev/null`:

1. **A prerequisite of this kind (`SKILL.md`, section 2) is not on the default
   branch.** Stop before the Intent gate. If
   `git branch -a --list 'wiki/*-<Key>' 'remotes/origin/wiki/*-<Key>'` shows the
   draft that holds it, say: "<Key> is in draft `wiki/<that branch>`, not on
   `<default>`. Merge its pull request first." Otherwise name the import run to
   do first.
2. **`wiki/import-<target>` exists and is not merged** into the default branch
   (`git merge-base --is-ancestor wiki/import-<target> "$DEFAULT"` fails). This
   is a revision, for example after review: `$T draft resume import-<target>`.
   Tell the user that new commits join any pull request open for that branch.
3. **`wiki/import-<target>` exists and is merged.** Run
   `$T draft discard import-<target> --remote`, then
   `$T draft start import-<target>`. Everything on that branch is already on
   the default branch, so deleting it loses nothing. If your environment
   refuses the deletion, ask the user to run the same `draft discard` command,
   then continue.
4. **Otherwise** `$T draft start import-<target>`.

## 3. The commands of each section

Each part is for the section of `SKILL.md` it names.

### At section 4: Intent gate, then the draft and the Run plan

Choose `import-<target>` and start or resume the draft
(section 2). Then:

```bash
cd "$WIKI/.worktrees/import-<target>"
READ=$(git rev-parse "$DEFAULT")
```

Read the wiki files again here, from the default branch at `READ`. Write the Run
plan (section 4) to `plan.md` in this folder, the root of the worktree, with
files grouped by their review group. Git ignores it there.

### At sections 5 and 6: Design gate, group by group; Write

Write each group's files under `wiki/` in the worktree when `SKILL.md` section 5
says. Add an entry to the `log.md` of every concept folder you write or change,
under today's date, newest first:

```markdown
## 2026-10-02

* **Import**: Imported from orders-service at 3f2a9c1. Written by an AI model with sdlc-import.
```

When the person rejects the import as a whole, remove a draft this run started:

```bash
cd "$WIKI" && $T draft discard import-<target>
```

### At section 7: Finish and commit

**Input check.** Check whether any wiki file the run compared, linked or
relied on as a prerequisite changed on the default branch since you read it:

```bash
git fetch --quiet origin 2>/dev/null
git diff --quiet "$READ" "$DEFAULT" -- <the input paths> || git diff --stat "$READ" "$DEFAULT" -- <the input paths>
```

If it changed, show the user what changed and re-check the affected groups.
Do not merge the default branch in here: `$T refresh` is for a pull request
that has conflicts (section 5).

**Finish.** Stamp, check and validate, naming any files or folders (every
changed file under the folder) from groups saved unchecked after
`--unverified`:

```bash
$T draft finish --by "sdlc-import/<the line in RELEASE>" --verified-by \
  --unverified <paths of groups saved unchecked>
```

With every group approved, leave `--unverified` out. `--verified-by` without
a value records the person in `git config user.email` as having confirmed
the approved files; `--unverified` without `--verified-by`, or a path the
draft did not change, is refused. If `ok` is false, fix what `missing_logs`
and `validate.errors` report and run it again; a fix to a file of an
approved group changes what the person confirmed, so show that group again
and take its answer again. Never record a model name.

**Change-set gate.** Run `$T draft diff`. Show the files it lists (those
marked `authored: false` were written by the tool) and a commit message. Ask
for approval. A change to an approved group reopens that group.

**Commit, then the summary.**

```bash
$T draft commit -m "<message>"; cd "$WIKI"
```

Run both in one command: `draft commit` removes the worktree you are in,
and the `plan.md` with it. Judge the result by the JSON it prints (`ok`,
`branch`, `pushed`), not by an error about the current directory. In the
summary, "Done" names the branch `wiki/import-<target>` and says the user
opens the pull request. If there is no remote, say the branch must be pushed
first.

## 4. The Run plan

The Run plan is the list of things this run has to do, with what is done so
far. It is the file `plan.md` at the root of the draft worktree. Its
`## Files` lists the files under their group headings, as `SKILL.md` section
4 shows:

```markdown
# Run plan: sdlc-import, SVC-orders
Intent approved 2026-10-03 · Design approved 2026-10-03

## Answers
1. Code import of SVC-orders in shop, owned by team orders.

## Assumed
- Database DB-shop holds TBL-orders.

## Files
(the groups of `SKILL.md` section 4)

## For other skills
- Unbuilt refund endpoint in branch feature/refund: sdlc-write-spec
```

- `## Answers` holds what the person decided in the rounds. `## Assumed` holds
  what you decided without asking.
- Do not copy the files into `plan.md`. Show each group's files in full in the
  chat at the Design gate.
- Add "Design approved" with the date when the last group is answered.
- Leave out a heading that has nothing under it.
- Git ignores the file. It is never committed and goes when the worktree goes.

**Resuming.** Do not ask the rounds again. Show the plan and ask one question:
"does this plan still stand?". On yes, continue at the first group that has no
answer yet (or the first unticked file in an answered group), then go on to
the input check and the Change-set gate. Any change the person makes to an
already-approved group reopens that group: show the group in full again and
take its answer again.

## 5. When a step goes wrong

| Situation | Do |
|---|---|
| `draft start` says the branch exists | Use section 2 again; never delete a draft that is not merged |
| The pull request has conflicts, because another draft was merged first | `$T draft resume import-<target>` if the worktree is gone, then `$T refresh` in it. It resolves conflicts in tool-written files itself; for a file a person writes it stops and names it: resolve it with git and run `$T refresh` again |
| `refresh` reports `ids.duplicate-key` | Another draft chose the same key: `$T rename <old> <new>`, then `$T refresh` |
| `draft finish` says `git config user.email` is not set | Ask the user for the id to record, and pass it: `--verified-by human:<id>` |
| `draft commit` refuses because files changed after `finish` | Run `draft finish` again |
| The user abandons the change | `cd "$WIKI" && $T draft discard import-<target> --remote` |
