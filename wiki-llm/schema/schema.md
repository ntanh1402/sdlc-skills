# SDLC Skills Wiki Schema

Version 1. Rules for an SDLC Skills knowledge bundle, built on
[OKF v0.2](okf-spec.md). The [sample](../sample/index.md) is a conformant worked
example.

Every rule a program can check lives in [`schema.json`](schema.json). The tool
`wiki-llm/tools/wiki_llm.py` enforces it, and the tables in these pages are
written from it by `wiki_llm.py docs`. The prose in these pages holds the rules
that need judgment; the tool does not check those.

## Shape

```text
<bundle>/
├── index.md                       okf_version and schema_version
└── <app>/                         Application
    ├── index.md  overview.md
    ├── conventions.md             optional
    ├── glossary.md                optional
    └── <collection>/              navigation only
        ├── index.md
        ├── <KEY>.md               a concept that is one file (decisions/)
        └── <KEY>/                 a concept that is a folder
            ├── index.md  overview.md  log.md
            └── <OWNED-KEY>.md     a concept the folder owns
```

- A folder or filename without `.md` is the key. There is no `key` field.
- Ownership comes from nesting: a Table belongs to the Database folder it sits
  in, a Task or a user story to its Feature or ChangeRequest, a TestCase to
  its TestSuite.
- An application contains only the collections it uses.
- A key is a type prefix and a name: lower-case words joined by `-`, taken
  from the title (`CR-coupon-codes`, `TASK-refund-endpoint`). Keys are never
  sequence numbers, so writers working in parallel do not pick the same one.
- Keys are unique per type inside an application. TestCase keys are unique
  inside their suite.
- A key never changes after it reaches the default branch. Before that,
  `wiki_llm.py rename` changes it and every reference to it.

## Frontmatter

- Values are single values, except `tags` and the OKF families `generated`,
  `verified`, and `sources`. Structured data and prose belong in the body.
- `generated` says who or what wrote the current content and when. Update it
  whenever the content changes in meaning.
- `verified` says who confirmed the content against its sources. A file with no
  `verified` is unconfirmed. Removing a stale `verified` is correct when the
  content changed and nobody re-confirmed it.
- Actors are `human:<id>`, `process:<id>`, or `<producer>/<version>` for a skill
  or agent.
- `sources` lists what the content was derived from outside the bundle: an
  OpenAPI file, a ticket, an external document. It never names a
  [Reference](reference.md); link a Reference under `# References`. `resource`
  names the real asset the file describes: a repository, a source file, a
  tracker ticket.
- Relationships to other concepts never go in frontmatter.
- A field whose values read "lower-case words joined by `-`; common: …"
  describes the system and is free text in that form. A skill suggests the
  values already used in the Application and the common ones; the person
  picks one or writes their own.

The tool reads exactly these forms. Each is valid YAML; any other YAML form is
rejected, for example a `generated:` mapping spread over several lines, a
comment, or an unquoted value that contains `: `.

```yaml
title: "Orders: one value on the line"
status: Active
tags: [sales, orders]
generated: { by: human:ntanh, at: 2026-10-01T09:00:00Z }
verified:
  - { by: human:ntanh, at: 2026-10-02T10:00:00Z }
sources:
  - id: openapi
    resource: https://example.com/openapi.yaml
    title: Orders OpenAPI
```

`verified` may also be one `{ by, at }` mapping on the line, like `generated`.

## Reserved files

### `overview.md`

The concept document of an Application and of every folder concept. Its first
heading is `# <title>`, matching the `title` field. Headings then follow the
order on the concept's schema page. Introductory prose may follow the title.

### `index.md`

Every directory has one, and the tool writes all of them. Never edit an index;
run `wiki_llm.py sync`.

### `log.md`

Every folder concept has one; the Application and the bundle root do not. A log
records why the folder's overview or an owned file changed, newest date first,
one `## YYYY-MM-DD` heading per date:

```markdown
# Title — change log

## 2026-10-01

* **Change kind**: what changed and why, with links where useful.
```

Files outside a concept folder (the Application's own files and decisions) have
no log; git history is their record.

## Links and relationships

- Use relative links, or links from the bundle root that begin with `/`. Every
  internal link and anchor resolves, and none leaves the bundle.
- Link a folder concept through its `overview.md`, and a file concept directly.
- A relationship is a list item under the heading that names it:
  `* [label](path) — qualifier — note`. The first link is the relationship; any
  other link in the note is context.
- Each relationship is written once, on the side its schema page names. The
  other side, where it exists, is written by the tool.
- A note never states another concept's status or pending state.
- A section with no relationships contains `None`.

## References

Every type may end its own sections with `# References`: the
[References](reference.md) a reader should consult while working on the
concept. It comes after the author's sections and before any section the tool
writes and `# Pending changes`.

```markdown
# References

* [REF-cancel-flow-example](../../references/REF-cancel-flow-example/overview.md) — take the idempotency-key handling; ignore its legacy retry loop.
```

- Each entry links the `overview.md` of a Reference of the same Application.
  The note says what to take from it. A `Deprecated` Reference is a warning.
- The tool writes the other side, `# Referenced by`, on the Reference.
- Adding or removing an entry is not a change of the concept: its status stays,
  it needs no ChangeRequest and no pending entry, and `verified` stays. Record
  it in the folder's `log.md` as a **References** entry, or in the commit
  message for a file that has no log.
- In a type whose other headings are free (Convention), `# References` still
  means this list. A document's own list of sources is called
  `# Bibliography`.

## Pending changes

A Design concept file always holds the approved target. While that target is
not yet built:

- its status is `Planned` (new), `Modifying` (changed), or `Removing`
  (to be removed);
- it has a `# Pending changes` section as its last section, with one entry per
  Feature or ChangeRequest responsible:
  `* [CR-7](path) — modified — what is not live yet`.

Whoever writes the target contract adds the entry. Whoever closes the Tasks
that build it removes the entry and, when no entry is left, sets the status to
`Active` and removes the section. The tool cross-checks entries against open
ChangeRequests, Features, and Tasks.

Closing the last Task has three more consequences, which the tool checks:

- a concept that was `Removing` and has no entry left becomes `Deprecated`
  and loses the section (`pending.removing-file`). Its file stays: the Task
  and the request that removed it still link it, and a link to a missing file
  is an error;
- a ChangeRequest whose Tasks are all `Done` is `Implemented`
  (`pending.request-implemented`);
- a Feature in `InDev` whose Tasks are all `Done` is reported as a warning
  (`pending.feature-built`): a person sets it `Released` when it ships.

## Corrections

A correction changes the record, not the system: the file was wrong about what
is built.

- It is written directly, with no ChangeRequest and no pending entry.
- It names what it was checked against: in a `**Correction**` entry in the
  folder's log, or, for a file that has no log (the Application's own files and
  decisions), in the commit message.
- A file that holds a target not built yet is not corrected: a `Planned`,
  `Modifying` or `Removing` Design file, a Feature before `Released`, and a
  `Released` Feature where the difference belongs to an `Approved`
  ChangeRequest.
- A change to the system goes through a Feature or a ChangeRequest.

## Generated content

`wiki_llm.py sync` writes every `index.md` and every section marked *tool* on a
schema page. `wiki_llm.py validate` fails when they are out of date. Do not edit
them; edit the authored side and run `sync`.

## Deviations from OKF v0.2

- `status` uses the per-type values on each schema page, not OKF's
  `draft | stable | deprecated`.
- The bundle-root `index.md` carries `schema_version` beside `okf_version`.
- OKF's Attested Computation type is not used.

## Concept catalog

<!-- generated:schema start -->
| Phase | Type | Schema page | Path |
|---|---|---|---|
| Plan | Application | [application](application.md) | `<app>/` |
| Plan | Feature | [feature](feature.md) | `<app>/features/FEAT-<slug>/` |
| Plan | ChangeRequest | [change-request](change-request.md) | `<app>/change-requests/CR-<name>/` |
| Plan | UserStory | [user-story](user-story.md) | `<app>/features/FEAT-*/STORY-<name>.md or <app>/change-requests/CR-*/STORY-<name>.md` |
| Design | ArchitectureDecision | [architecture-decision](architecture-decision.md) | `<app>/decisions/ADR-<name>.md` |
| Source | Reference | [reference](reference.md) | `<app>/references/REF-<name>/` |
| Plan | Convention | [convention](convention.md) | `<app>/conventions.md` |
| Plan | Glossary | [glossary](glossary.md) | `<app>/glossary.md` |
| Design | Service | [service](service.md) | `<app>/services/SVC-<slug>/` |
| Design | WebFrontend | [frontend-web](frontend-web.md) | `<app>/frontends/WEB-<slug>/` |
| Design | MobileFrontend | [frontend-mobile](frontend-mobile.md) | `<app>/frontends/MB-<slug>/` |
| Design | Endpoint | [endpoint](endpoint.md) | `<app>/services/SVC-*/EP-<slug>.md` |
| Design | Subscription | [subscription](subscription.md) | `<app>/services/SVC-*/SUB-<slug>.md` |
| Design | MessageChannel | [message-channel](message-channel.md) | `<app>/channels/CHAN-<slug>/` |
| Design | Database | [datastore-database](datastore-database.md) | `<app>/datastores/DB-<slug>/` |
| Design | Table | [datastore-table](datastore-table.md) | `<app>/datastores/DB-*/TBL-<slug>.md` |
| Design | Cache | [datastore-cache](datastore-cache.md) | `<app>/datastores/CACHE-<slug>/` |
| Design | BlobStore | [datastore-blob](datastore-blob.md) | `<app>/datastores/BLOB-<slug>/` |
| Design | SearchIndex | [datastore-search-index](datastore-search-index.md) | `<app>/datastores/IDX-<slug>/` |
| Design | ExternalService | [external-service](external-service.md) | `<app>/externals/EXT-<slug>/` |
| Design | Operation | [external-operation](external-operation.md) | `<app>/externals/EXT-*/OP-<slug>.md` |
| Build | Task | [task](task.md) | `<app>/features/FEAT-*/TASK-<name>.md or <app>/change-requests/CR-*/TASK-<name>.md` |
| Verify | TestSuite | [test-suite](test-suite.md) | `<app>/tests/TS-<slug>/` |
| Verify | TestCase | [test-case](test-case.md) | `<app>/tests/TS-*/TC-<slug>.md` |

**Design types:** Service, WebFrontend, MobileFrontend, Endpoint, Subscription, MessageChannel, Database, Table, Cache, BlobStore, SearchIndex, ExternalService, Operation.

| Qualifier set | Values |
|---|---|
| change | `new`, `modified`, `removed` |
| access | `read`, `write`, `rw` |
| criticality | `critical` |
<!-- generated:schema end -->

## Conformance

A conformant bundle passes `wiki_llm.py validate` and follows the judgment rules
on each page it uses.
