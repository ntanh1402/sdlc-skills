---
name: sdlc-import
description: Bring an existing, already built system into the project wiki, one source per run - a service's or frontend's code, an architecture document, a requirement document (PRD), a built capability that has no document, an end-to-end, integration, load or security test suite, a test plan, or a page, document or code example to keep as a Reference - as as-built Design files, Released Features, decisions, TestSuites and References that a person confirms group by group. When the source is already in the wiki, compare it with the wiki instead and let the person decide each difference. Use for brownfield onboarding, importing or documenting existing code, documents or tests, and checking whether the wiki still matches the code. Not for anything that is not built yet, for reviewing a code change, or for running tests.
---

# Import an existing project

This skill records what already exists. One run takes one **Import source** (a
code folder, a document or a test suite) and writes the concept files that say
what is built and running today. A person confirms them group by group.

| Kind of Import source | Guide in this skill's folder |
|---|---|
| Code: one service's or one frontend's folder | `references/import-code.md` |
| Architecture document | `references/import-architecture-document.md` |
| Requirement document (a PRD, a functional spec) | `references/import-requirement-document.md` |
| A built capability that has no document | `references/import-undocumented-capability.md` |
| Test code: one end-to-end, integration, load or security suite | `references/import-test-code.md` |
| Test document (a test plan, a sheet of manual cases) | `references/import-test-document.md` |
| A reference: a page, a document or a code location to consult | `references/import-reference.md` |

When the Import source is already in the wiki, the run compares instead of
creating (`references/compare.md`).

Its draft prefix is `import-`: the draft for the code of `SVC-orders` is
`wiki/import-SVC-orders`.

## Before you start

Read, in this skill's folder, `references/read-protocol.md`,
`references/flow.md` and `references/write-protocol.md`. `flow.md` gives the
steps of the run and the three gates; this file says what is this skill's own
at each step. Then read `schema.md` and `reference.md` in the wiki's
`.wiki-llm/schema/`. The guide of the kind names the other schema pages; open
only that guide.

Four rules of the shared files read differently in this skill:

- **"Never edit another step's output."** This skill edits a file another
  skill wrote when the edit is a **correction**: the file was wrong about what
  is built (`schema.md`, "Corrections"). Section 3 says which files may be
  corrected.
- **The draft key** is not built from a Feature or ChangeRequest key. Section 2
  gives it.
- **The Design gate** is taken group by group, and the files of a group are
  written after its answer (section 5). Here the design is the files
  themselves.
- **A difference** found by a compare run is a question with no
  recommendation, except the two proposals `references/compare.md` allows.

Other requests go elsewhere; say so and stop:

| Request | Skill |
|---|---|
| Something that is not built yet: a new capability, a change, a bug to fix | `sdlc-write-spec` |
| User stories | `sdlc-write-stories`; an import writes none |
| A question about the wiki | `sdlc-ask-wiki` |
| A review of a code change against the wiki | `sdlc-review-code` |
| A PDF, Word, slide, sheet or other non-text document | `sdlc-convert-doc` first, then this skill on its Markdown |
| An Application that does not exist yet | `sdlc-setup-wiki` ("add application `<key>`") |
| Writing the code of a Task | `sdlc-build-task` |
| A typo or a wording fix that needs no source to check against | `sdlc-edit-wiki` |
| Tracker issues, running tests | Not this skill. Tasks are never imported |

Being asked to run this skill does not approve anything it writes.

## 1. The questions

The lookup of this skill reads two things: the Import source, and the wiki
for what it already says about it (sections 2 and 3). Then ask in rounds, as
`references/flow.md` section 4 says. The first round holds every question of
this table the Import source leaves open, each with the answer it shows as
the recommendation, so the person mostly confirms. It also names the kind,
says whether the run creates or compares, and asks the wiki question: what
else in the wiki this Import source touches. A file of another kind is
another run, listed under "For other skills".

| Question | Notes |
|---|---|
| Where is it? | A folder or a file path. The user gives it; never guess it. "This folder" is an answer |
| What kind is it? | It selects the guide. A folder with code and tests is two kinds, so two runs: the code first |
| Which Application does it belong to? | Read `wiki/index.md`. One Application: propose it. An Application the wiki lacks stops the run: "run sdlc-setup-wiki to add application `<key>`" |
| Which team owns it? | `ownerTeam` is required on a Service, a frontend, a Feature and a decision; code does not say it |
| Is what it describes built and running today? | "Not built": stop, "use sdlc-write-spec". "Partly": import the built part and list the rest for a ChangeRequest |
| How current is it? | For a document: its date, and any part the person knows is out of date. Leave that part out and list it |
| What is the repository URL? | Only for code with no git remote |
| What is the URL of this service's folder? | Only when the repository holds several services (section 4) |
| For each service an architecture document names and the wiki lacks: its repository URL, owner team and type? | A Service page needs all three. Without them the service is listed as not imported |

When the user asks for several Import sources at once ("import all of it"),
list the ones you see and the order to do them (section 2), and do the first.

## 2. The kinds

| Kind | Writes | Status written | Draft key | Must be on the default branch first |
|---|---|---|---|---|
| Code | The Service or frontend, its Endpoints and Subscriptions, and the Tables, Channels, stores and externals it uses that the wiki lacks | `Active` | `import-SVC-<name>`, `import-WEB-<name>` or `import-MB-<name>` | Nothing |
| Architecture document | The Application's `# Architecture`, decisions, `conventions.md`, `glossary.md`, a Service page for each service the wiki lacks, and the document as a Reference | Decisions `Accepted`; Services `Active` | `import-<document name>` | Nothing |
| Requirement document | One as-built Feature per capability, and the document as a Reference | `Released` | `import-FEAT-<name>`; `import-<document name>` for several Features | A Service page for each service it uses |
| Capability with no document | One as-built Feature | `Released` | `import-FEAT-<name>` | The Endpoints and Subscriptions of the services it uses |
| Test code | One TestSuite and one TestCase per test | `Implemented` | `import-TS-<name>` | A Feature it verifies |
| Test document | One TestSuite, its TestCases, and the document as a Reference | `Approved` | `import-TS-<name>` | A Feature it verifies |
| Reference | One Reference, and the `# References` links to it | `Active` | `import-REF-<name>` | Nothing |

`<document name>` is the file name without its extension, in lower-case words
joined by `-`: `Architecture Overview.pdf` gives `import-architecture-overview`.

Three cases write another status:

- a decision the document shows as replaced is `Superseded`;
- a file kept after the code dropped what it describes is `Deprecated`
  (`references/compare.md`);
- a TestSuite from a test document is `Implemented`, with `resource`, when the
  person says its runnable tests exist.

The order is Design, then Features, then tests. When a prerequisite is not on
the default branch, stop before the Intent gate and name the run to do first:

```text
checkout-prd.md describes the orders and payments services. SVC-payments is
not in the wiki. Import its code or its architecture document first.
```

If the prerequisite sits in a draft that is not merged, name that draft
instead (write protocol, section 3, case 1).

## 3. Create or compare

The run compares when the **main concept** of the Import source is already on
the default branch:

| Kind | The main concept |
|---|---|
| Code | The Service or frontend whose `resource` is this repository, or whose key is the one you would propose |
| A document, a reference | The Reference whose `resource` is the source's URL, or whose key is the one you would propose |
| Capability with no document, test code | The Feature or TestSuite the person names |

Compare repository URLs in one form: `https://<host>/<org>/<repo>`, with no
`.git` and no trailing slash, so `git@github.com:acme/orders-service.git`
matches `https://github.com/acme/orders-service`.

A compare run follows `references/compare.md`; read it now. It still asks the
rounds, keeps the three gates and uses one draft. In short:

- A file that matches is reported, and the person may confirm it.
- A difference the wiki marks as not built yet is reported as expected.
- For every other difference the person chooses: keep the wiki, take what the
  Import source says, or "the code is wrong". The differences are one
  numbered round. Never choose for them.
- "Take what the Import source says" is a correction. It may edit only a file
  that records what exists: an `Active` Design file, a `Released` Feature, an
  `Accepted` decision, a TestSuite and its TestCases, and the Application's own
  files. Never a file that holds a target not built yet. A correction that
  removes a Requirement a user story lists fixes those stories in the same
  draft, as the last rule of `user-story.md` and of `test-case.md` say.

## 4. Intent gate, then the draft and the Run plan

For code, read the repository facts first (`SRC` is the path the user gave):

```bash
git -C "$SRC" rev-parse --show-toplevel    # the repository; no output: not a git repository
git -C "$SRC" remote get-url origin        # the URL; none: ask the person
git -C "$SRC" rev-parse --short HEAD       # the commit to record
git -C "$SRC" status --porcelain           # not empty: uncommitted changes
```

- Write the URL in the form of section 3.
- When the folder has uncommitted changes, say so: the import reads the files
  as they are, so the recorded commit will not match them. Ask whether to go
  on or to commit first.
- When the repository holds several services (the path is a folder inside it
  and its siblings are services too), one run imports one of them. Ask for the
  URL of this service's folder; it starts with the repository URL, for example
  `https://github.com/acme/shop/tree/main/services/orders`. That URL is the
  Service's `resource`.

**Intent gate.** Restate, and ask for approval:

- the answers of section 1;
- the kind, and whether the run creates or compares; for a compare, the match
  ("SVC-orders is already in the wiki; I will compare");
- the draft key;
- the types of file the run will write;
- that the prerequisites of section 2 are on the default branch.

Then start or resume the draft (write protocol, section 3, with the key of
section 2). A compare run starts its draft, and so its Run plan, only when it
has something to write or to confirm (`references/compare.md`).

Follow the guide of the kind to prepare every file, then write the Run plan.
Its `## Files` lists the files under their groups (section 5), and each group
heading records the person's answer once it is given:

```markdown
## Files
### The Service page: approved
- [x] services/SVC-orders/overview.md (add)
- [x] services/SVC-orders/log.md (add)
### Endpoints: saved unchecked
- [x] services/SVC-orders/EP-create-order.md (add)
### Tables of DB-shop
- [ ] datastores/DB-shop/TBL-orders.md (add)
```

A group with no answer yet has not been shown. A resumed run continues at the
first such group.

The **input paths** of the input check are every wiki file the run compared or
linked, and the files that are its prerequisite.

## 5. Design gate, group by group

Show the Run plan once, before the first group. Then show the files in
groups, each file in full, never as a summary.

| Kind | Groups, in this order |
|---|---|
| Code | The Service or frontend page; its Endpoints; its Subscriptions; the Tables of each Database; Channels; stores; externals with their Operations |
| Architecture document | The Reference; each Service page; each decision; the Application's `# Architecture`; conventions; glossary |
| Requirement document, capability with no document | Each Feature, with its Reference when it has one |
| Test code, test document | The suite page, with the Reference of a test document; then its TestCases, a few at a time |
| Reference | The Reference, with the links to it |

End each group with one question. Three answers are accepted:

| Answer | Effect |
|---|---|
| Approve | The files are written and confirmed: `verified` by the person |
| Change | Correct the group and show it again |
| "Save it, I did not check it" | The files are written without `verified` |

Before a group is shown, ask for each required field of its files that the
Import source does not give (list 1 below): one question, with a proposal
when the source supports one. Write the files of a group (section 6) as soon
as it has its answer, tick them, and record the answer on the group's heading
in the Run plan.

A group that holds a Reference cannot be saved unchecked: the schema requires
a person's confirmation on a Reference. Say so and ask again.

After the groups, show three lists. Say "none" for an empty one. They are
shown here, before the Change-set gate, and are not repeated after the
commit.

1. **Could not determine.** What you looked for and did not find. Never invent
   a value. The schema still requires some of what is missing:
   - a required field was asked before its group was shown. With no answer
     the file was not written;
   - a required section of prose (a Subscription's `# Idempotency`, an
     external's `# Fallback`, a decision's `# Alternatives`) gets the one line
     `Not determined by the import.`; the person may fill it in now;
   - a required section that must hold a table or a diagram cannot take that
     line, so the file is not written.

   List every such file and section.
2. **Not modelled.** Things the schema has no type for, such as a scheduled
   job or a store that is not relational. Describe them in the Service's prose.
3. **Disagreements.** Where the Import source and the wiki, or a document and
   the code, say different things. Code wins for contracts (endpoints, tables,
   channels); documents add requirements, reasons, decisions and diagrams.
   List each one; never resolve one yourself.

Rejecting the import as a whole discards a draft this run started (write
protocol, section 4, step 3).

## 6. Write

In the draft worktree, under `wiki/<app>/`, write the approved files as their
schema pages require. For every file:

- **The Import source is named** on every file. Code and test code are
  named in `sources`:

  ```yaml
  sources:
    - id: code
      resource: https://github.com/acme/orders-service
      title: src/api/orders.py at 3f2a9c1
  ```

  `resource` is the repository URL and `title` is the path that was read,
  then `at`, then the commit. Build no link to a hosting service's file view.
  A capability with no document repeats the code entries of the Design files
  it was read from. A document is never named in `sources`: every file
  written from it links its Reference under `# References`, with a note
  naming the part it was written from.
- **A document's Reference** is the folder
  `references/REF-<document name>/`, as `reference.md` says: the document's
  Markdown copy as a content file named after the document
  (`architecture-overview.md`), the images it links and the original file
  beside it, an `overview.md` that summarises the document and lists the copy
  under `# Contents`, and `log.md`. `resource` is the document's URL when it
  has one.
- **`resource`** of a Service or frontend is the repository URL of section 4.
  A TestSuite written from test code has `resource` set to where its tests
  live.
- **Keys** are names taken from the Import source's own names: `SVC-orders`,
  `EP-create-order`, `TBL-orders`.
- **A document's Markdown copy** is named after the document
  (`architecture-overview.md`). A name the folder keeps for itself (`index`,
  `overview`, `log`, and in the Application folder `conventions` and
  `glossary`) gets `-document` added. Images it links are copied beside it.
- **Logs.** Add an entry to the `log.md` of every concept folder you write or
  change:

  ```markdown
  * **Import**: Imported from orders-service at 3f2a9c1. Written by an AI model with sdlc-import.
  * **Correction**: The request also takes `giftNote`; checked against orders-service at 3f2a9c1. Written by an AI model with sdlc-import.
  ```

  The Application's own files and decisions have no log. When one of them is
  corrected, the commit message carries a line
  `Correction: <path>, checked against <the commit or the document>`.
- Never write `generated` or `verified`, a reverse section (`# Used by`,
  `# Publishers`, `# Subscribers`, `# Change history`, `# Superseded by`) or an
  `index.md`; the tool writes them.
- Never copy a secret, a credential or personal data from the Import source
  into the wiki. Name the setting, not its value.

## 7. Self review, finish and commit

Follow `references/write-protocol.md` section 4 from step 5. In the self
review, also check that:

- every file written names the Import source: in `sources`, or by linking
  the document's Reference under `# References`;
- no file has a status that means "not built yet" or a `# Pending changes`
  entry, and no secret was copied;
- every group in the Run plan has its answer, and the files of a group saved
  unchecked are the ones you will name after `--unverified`.

A fix to a file of an approved group changes what the person confirmed: show
that group again and take its answer again.

Finish with the groups the person did not check named after `--unverified`,
each as a file or as a folder (every changed file under it):

```bash
$T draft finish --by "sdlc-import/<the line in RELEASE>" --verified-by \
  --unverified wiki/shop/datastores/DB-shop/TBL-orders.md wiki/shop/channels/CHAN-order-created
```

With every group approved, leave `--unverified` out. `--unverified` without
`--verified-by` is refused, and so is a path the draft did not change.

Commit message: `import(<main concept or document name>): <what was imported>`,
for example `import(SVC-orders): the orders service from its code at 3f2a9c1`.

In the summary, "Not done" names the files that were not written (the first
list of section 5), "For other skills" names what the differences need
(a ChangeRequest with `sdlc-write-spec`), and "Next" is the next run in the
order of section 2.

## What this skill never does

- It never writes a Task, a ChangeRequest, or a Feature that is not built.
- It never writes a status that means "not built yet" (`Draft`, `ReqApproved`
  or `Approved` on a Feature; `Planned`, `Modifying` or `Removing` on a Design
  file), and never a `# Pending changes` entry.
- It never corrects a file that holds a target not built yet.
- It never runs the code or its tests, and never imports unit tests.
- It never picks the answer to a difference.

## Done when

- One Import source was read, and every file written from it names it, in
  `sources` or under `# References`.
- Every group was approved, corrected, or saved as not checked; no file is
  marked confirmed that the person did not see in full.
- The three lists were shown before the Change-set gate.
- The self review found nothing it could not fix, or the person accepted what
  was left at the Change-set gate.
- `draft finish` was `ok`, the change set was approved, and `draft commit`
  reported the branch.
