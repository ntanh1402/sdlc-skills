# Importing an architecture document

One run reads one document that describes the system as it is built: its
parts, how they connect, the decisions behind them, the team's conventions,
its terms. Read these schema pages in `.wiki-llm/schema/` first:
`application.md`, `architecture-decision.md`, `convention.md`, `glossary.md`,
`service.md` and `reference.md`.

A document adds what code cannot show: reasons, decisions, diagrams, terms.
It never decides a contract. Code wins for endpoints, tables, channels,
stores, vendors and their operations.

## 1. What to write

| From the document | File |
|---|---|
| The document itself | The Reference `references/REF-<document name>/`, as `SKILL.md` section 6 says |
| The system picture | The Application's `# Architecture`: prose and one Mermaid `flowchart` |
| Each decision in force | `decisions/ADR-<name>.md`, `status: Accepted` |
| Coding and working rules | `conventions.md` |
| Terms and roles | `glossary.md` |
| Each service the wiki lacks | `services/SVC-<name>/overview.md` and `log.md`, `status: Active`, when the person gives its repository URL, owner team and type |

Rules:

- **The Reference** holds the document's Markdown copy, complete, as a
  content file, and an overview that summarises it. It needs the person's
  approval of the whole folder, so its group cannot be saved as not checked.
- **Service pages only.** Of the Design types this run writes only Service
  pages, one for each service the wiki lacks and the person gave a repository
  URL, an owner team and a type for. Such a page holds the title, the
  description and what the document says the service is for; it has no
  Endpoint, Subscription or link to a store. A later code import compares the
  page and adds the contracts.
- **Everything else the document names** (endpoints, tables, channels,
  vendors, frontends) appears in the Application's `# Architecture` only, by
  name. List each one as not imported: "import its code".
- **A decision is imported only when it links a concept.** `# Affected
  concepts` needs at least one link to a concept that is in the wiki or in
  this draft. A decision that links none is listed as not imported, with the
  import that would make it possible.
- **A replaced decision.** When the document shows a decision as replaced,
  write both: the old one with `status: Superseded`, and the new one linking
  it under `# Supersedes`. Otherwise import only decisions in force. Never
  write `# Superseded by`; the tool does.
- **`decisionDate`** is the date the document gives. With none, leave the
  field out; never use today's date.
- **Existing content is compared, not replaced.** When the Application already
  has an `# Architecture`, conventions or a glossary, show the differences and
  let the person decide each one (`compare.md`). New terms and new rules are
  additions.
- Every file written from the document links its Reference under
  `# References`, with a note naming the part it was written from. The
  Application's own files and the decisions link it too.

## 2. What to ask

- The document's date, and any part the person knows is out of date. Leave
  that part out of every file except the Reference, and list it.
- For each service the document names and the wiki lacks: its repository URL,
  owner team and type. Without all three the service is listed as not
  imported.
- For a decision without stated alternatives: whether the person knows them.
  With no answer write `Not determined by the import.` under `# Alternatives`.

## 3. Before the Design gate

Check by reading:

- the `flowchart` shows every service and frontend the prose names;
- every decision links at least one concept that exists;
- the Reference's content file is the whole document, and its images are
  beside it;
- nothing the document describes as planned was written as built. List it for
  `sdlc-write-spec` instead.
