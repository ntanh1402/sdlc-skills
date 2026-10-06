# Importing a requirement document

One run reads one document that states what a capability must do (a PRD, a
functional spec) for something that is built and running. It writes one
as-built Feature per capability. Read these schema pages in
`.wiki-llm/schema/` first: `feature.md` and `reference.md`.

Before anything else, check the prerequisite: every service the document's
capability uses has a Service page on the default branch. If one is missing,
stop and name the import to run first.

## 1. What to write

For each capability, `features/FEAT-<name>/` with:

| File | Content |
|---|---|
| `overview.md` | `status: Released`, the Requirements, `# Architecture`, and `# References` linking the document's Reference |
| `log.md` | One `**Import**` entry |

and the document itself once, as the Reference `references/REF-<document name>/`
(`SKILL.md` section 6).

Rules:

- **Requirements are those the document states and that are built.** Give
  each a key `REQ-<feature words>-<behaviour words>` and the form
  `feature.md` requires.
- **How to know a Requirement is built.** The wiki's Design files show it
  where they can: an Endpoint, a Table or a Channel that does what the
  Requirement says. Where they cannot (the service has only a Service page,
  or no file speaks about that behaviour), ask the person about each such
  Requirement and write only those the person says are built.
- **A Requirement the system does not satisfy is left out** and listed for a
  ChangeRequest: "REQ-…: stated in the document, not built; open a
  ChangeRequest with sdlc-write-spec once the Feature is merged".
- **`# Architecture`** is written from the Design files on the default
  branch, with the nested sections `feature.md` requires: the context, one
  Mermaid `flowchart` of the services and frontends, `## Services`,
  `## Frontends` only when the capability has a user interface, one
  `sequenceDiagram` covering each Requirement's main flow, the decisions, and
  the traceability table from each Requirement to the Design concepts that
  satisfy it.
- **A service with no contracts in the wiki.** When a service has only a
  Service page, the flows and the traceability name that Service page, and
  the missing contracts are listed under "Could not determine" with "import
  its code".
- **Never design.** Write only links to Design files that exist. Never write
  or change a Design file in this run.
- **One document, several Features.** Every Feature links the one Reference
  under `# References`, each with a note naming its part of the document.
  The draft key is then `import-<document name>`.
- `releasedAt` is written only when the person gives the date.

## 2. What to ask

- The owner team and, when the document names several capabilities, which of
  them are built.
- For each Requirement the Design files cannot show as built: "Is this built
  and running today?"
- The document's date, and any part known to be out of date.

## 3. Before the Design gate

Check by reading:

- every Requirement appears in `## Traceability`;
- every concept in `## Services` and `## Frontends` appears in the flowchart;
- the Reference's content file is the whole document;
- every Requirement left out is in the list for a ChangeRequest.
