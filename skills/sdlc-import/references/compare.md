# Comparing an Import source with the wiki

Use this file when the main concept of the Import source is already on the
default branch (`SKILL.md`, section 3). The run then compares what the Import
source says with what the wiki says, and the person decides each difference.

**Drift** is a difference between a concept file and the code that nothing in
the wiki marks as not built yet. Three things mark a difference as not built
yet, and such a difference is expected, not Drift:

- a `# Pending changes` entry on the file;
- an `Approved` ChangeRequest on a `Released` Feature (the Feature already
  holds that request's target);
- a TestSuite that is not `Implemented`.

## 1. Find the match

- **Code.** The Service or frontend whose `resource` is this repository, in
  the URL form of `SKILL.md` section 3. In a repository with several services,
  every `resource` that starts with the repository URL is a candidate: list
  them and ask which one this folder is. A match by key alone (the page has
  another `resource`, for example after the repository moved) is still the
  match, and `resource` is then one of the differences.
- **A document.** A Reference with the document's name.
- **Otherwise** the Feature or TestSuite the person names.

Name the match at the Intent gate ("SVC-orders is already in the wiki; I will
compare") and get it confirmed.

Two matches stop or change the run:

- A Feature is compared only when it is `Released`. Before that it describes
  something not built: stop, "FEAT-coupons is not built yet; there is nothing
  to compare".
- A TestSuite that is `Draft` or `Approved` may describe tests nobody has
  written yet. Compare it, but a TestCase with no test in the code is expected
  there.

## 2. Compare every file the Import source covers

Read the Import source as the guide of its kind says, and build what you would
have written. Then go file by file:

| Finding | Do |
|---|---|
| The file matches | Say so. If nobody confirmed the file, or the person wants to confirm it again, offer to confirm it (section 4) |
| The wiki is ahead, and a `# Pending changes` entry on the file describes that difference | Report it as expected, naming the Feature or ChangeRequest. Write nothing |
| A `Released` Feature is ahead, and an `Approved` ChangeRequest on it describes that difference | Report it as expected, naming the ChangeRequest. Write nothing |
| A TestSuite that is not `Implemented` has a TestCase with no test in the code | Report it as not written yet. Write nothing, and never offer the case for deletion |
| The file has a pending entry, and the difference is not what the entry describes | Report both. Write nothing: the file holds the target, so the correction waits until the pending work is closed. Name the Feature or ChangeRequest |
| Drift, or a difference from a document | Ask the person (section 3) |
| The Import source has something the wiki lacks | A new file, shown at the Design gate like any other |
| The wiki has something the code no longer has | Ask the person (section 3). For "take what the code says", see section 5 |

Show the findings as one list before asking anything:

```text
SVC-orders is already in the wiki, so I compared it with the code at 3f2a9c1.
  EP-create-order.md   the code accepts a field `giftNote` the wiki does not list
  EP-cancel-order.md   expected: CR-cancel-window is not built yet
  TBL-orders.md        matches the code; nobody has confirmed this file yet
```

## 3. The three answers

Ask about the differences in one numbered round, one question per
difference: "Keep the wiki, take what the code says, or is the code wrong?"
Never pick an answer, and give no recommendation except the two proposals
below.

| Answer | Effect |
|---|---|
| Keep the wiki | Nothing is written. The file is not confirmed by this run |
| Take what the Import source says | The file is corrected in the draft |
| The code is wrong | Nothing is written. Say: "open a bugfix ChangeRequest with sdlc-write-spec" |

Rules for "take what the Import source says":

- It is a **correction**, so it is allowed only on a file that records what
  exists: an `Active` Design file, a `Released` Feature, an `Accepted`
  decision, a TestSuite and its TestCases, and the Application's own files
  (its `# Architecture`, conventions, glossary).
- Add a `**Correction**` entry to the folder's log, naming the commit or the
  document. For a file with no log (the Application's own files and
  decisions), put the line
  `Correction: <path>, checked against <the commit or the document>` in the
  commit message.
- Add the Import source to the file's `sources`.
- A file a person had confirmed before stays confirmed: the person saw the
  difference. A file nobody had confirmed is shown in full, and the person
  approves it or it is saved as not checked (`--unverified`). Seeing one
  difference does not confirm the rest of the file.

Two proposals you may make, with the reason, while the person still decides:

- When a document disagrees with a file that was written from code, propose
  "keep the wiki": code wins for contracts.
- When the difference is really a planned change (the document describes
  something not built), it is not a correction. Name `sdlc-write-spec`.

## 4. Confirming a file that did not change

When the person confirms a file whose content matches, record it in the draft
worktree:

```bash
$T verify wiki/shop/datastores/DB-shop/TBL-orders.md
```

It adds the person to the file's `verified` and a `**Verification**` entry to
the folder's log. `draft finish` leaves such a file's `generated` alone.

## 5. Something the code no longer has

When the person answers "take what the code says" for a file whose subject is
gone from the code, look for what links to it:
`grep -rl "<KEY>" wiki/ --include='*.md'`.

| Who links to the file | Do |
|---|---|
| Nothing | Delete the file |
| Live files: a Feature's `# Architecture`, a Service's `# Calls`, a TestCase's `# Covers` | List them and ask: correct them too, or keep the file as `Deprecated` |
| A record: an `Implemented` ChangeRequest's `## Target delta`, a `Done` Task's `# Planned scope` | Never rewrite the record. Keep the file and set `status: Deprecated` |

A deletion and a `Deprecated` status are both shown at the Design gate.

## 6. The draft

- Start the draft only when there is something to write or to confirm. A
  compare run with nothing to write and nothing confirmed ends without a
  draft: report the findings and stop.
- The Design gate shows every new file, every corrected file and every
  deletion, in the groups of `SKILL.md` section 5. The Run plan lists them
  under those groups.
- The input paths of the input check are every wiki file you compared.
