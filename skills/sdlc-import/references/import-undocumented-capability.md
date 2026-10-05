# Importing a capability that has no document

Some built capabilities were never written down. This run writes one as-built
Feature for one of them, from the wiki's Design files, the code and the
person's answers. Read `feature.md` in `.wiki-llm/schema/` first.

Before anything else, check the prerequisite: the code of every service the
capability uses is imported, so its Endpoints and Subscriptions are on the
default branch. A Service page alone is not enough here: the Requirements are
proposed from the contracts. If they are missing, stop and name the code
import to run first.

## 1. Find the capability's contracts

Ask the person to name the capability and what a user or another system does
with it. Then find the Endpoints, Subscriptions, Tables and Channels that
serve it: search the Application's indexes and `grep -rl` for its words.
Show the list and let the person add or remove.

## 2. Propose the Requirements

Propose one Requirement per behaviour the contracts show: what each Endpoint
does, what each Subscription reacts to, what is stored, what is refused. Put
them to the person as one numbered round, each proposal a question:

- the person corrects the wording, the priority and the kind;
- the person adds behaviour the contracts do not show (a business rule, a
  limit, a reason);
- stop when the person says the list is complete.

Never write a Requirement the person did not confirm.

## 3. What to write

`features/FEAT-<name>/` with `overview.md` (`status: Released`) and `log.md`.
There is no Reference, because there is no document.

- `# Architecture` is written as `import-requirement-document.md` section 1
  says: from the Design files on the default branch, never designing.
- `sources` repeats the code entries of the Design files the Requirements
  were read from.
- The log entry says the Requirements were stated by the person:
  `* **Import**: Requirements stated by the owner team and read from SVC-orders. Written by an AI model with sdlc-import.`

## 4. Before the Design gate

Check by reading:

- every Requirement appears in `## Traceability` with a concept that exists;
- no Requirement describes something planned. List it for a ChangeRequest.
