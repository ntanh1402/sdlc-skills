---
name: sdlc-ask-wiki
description: Answer questions from the project wiki without changing it - list an application's Features with status, owner, priority, design readiness and open ChangeRequests; show one Feature's approved architecture with its diagrams, services, frontends, contracts, decisions, traceability and what is not built yet; show one Endpoint or consumer with its input, output, validations and diagrams; show a user story or print its paste-ready copy for the tracker; list the References (documents, pages, code examples) that apply to a subject; or answer any free-form question about requirements, user stories, architecture, tasks, tests, dependencies and history. Use for read-only questions about the sdlc-skills wiki. Not for writing or changing it.
---

# Ask the wiki

Read-only. Never create, edit, delete or commit a wiki file, and never start a
draft. Route a request to change the wiki to the skill that does it:
`sdlc-write-spec` (requirements), `sdlc-write-stories` (user stories),
`sdlc-design-arch` (architecture),
`sdlc-plan-tasks` (tasks), `sdlc-design-tests` (test design),
`sdlc-import` (existing code, documents or tests to bring into the wiki, or
to compare with it), `sdlc-close-task` (a Task whose code is merged),
`sdlc-edit-wiki` (a typo, the glossary or conventions, a Feature marked
released, a ticket link on a Task or a user story), `sdlc-setup-wiki` (the wiki itself, or a new
Application). A request to write a Task's code goes to `sdlc-build-task`, and
one to review a code change to `sdlc-review-code`.

Read `references/read-protocol.md` in this skill's folder and follow it: it
finds the wiki, says how to read the default branch, and where the schema
pages are. Read the schema page of a type before relying on its headings or
statuses.

## How to answer

1. Ask only for what is genuinely missing: an Application when there are
   several and the question does not say which, or a Feature when several
   match.
2. Search cheaply first (indexes, `grep -rl`), then read only the files the
   answer needs.
3. Answer the question first, then cite the paths you read. Separate what the
   wiki says from what you infer. When nothing is found, say what you searched.
4. Do not paste whole files when a short interpreted answer does.

## Recipe: list features

For one Application (ask which if there are several), read
`wiki/<app>/features/index.md` and each Feature's `overview.md`. Report one row
per Feature:

| Column | From |
|---|---|
| Key and title | frontmatter |
| Status | `status` (the values are on the Feature schema page) |
| Owner, priority | `ownerTeam`, `priority` |
| Designed | `# Architecture` is not `None` |
| Not live | number of Design concepts whose `# Pending changes` links this Feature |
| Open changes | ChangeRequests listed in its `# Change history` whose status is in `pending.open_requests` of `.wiki-llm/schema/schema.json` |

Explain an empty list. Offer "show the architecture of FEAT-x" for detail.

## Recipe: show a feature's architecture

For exactly one Feature:

1. Summary: title, status, owner, and whether it is designed (`Approved` or
   later) or still at requirements (`Draft`, `ReqApproved`).
2. Requirements: key, priority and one line each.
3. The stored diagrams from `## High-level architecture` and
   `## Runtime sequences`, as they are.
4. Frontends (only when `## Frontends` exists): each one's status, its routes
   or screens, and the Endpoints and Operations under its `# Calls`.
5. Services: each one's status, its Endpoints and Subscriptions, the channels
   it publishes, the tables and stores it uses, and the externals it calls.
6. Decisions under `## Decisions`, with their consequences.
7. `## Traceability`, Requirement by Requirement.
8. References the Feature links under `# References`, with their notes.
9. Not live: every concept with a `# Pending changes` entry for this Feature or
   one of its ChangeRequests, with the entry's text; and the open
   ChangeRequests.
10. Gaps found while reading: links that do not resolve, Requirements missing
   from Traceability, differences between the wiki and code you also read
   (`sdlc-import` on that code compares them file by file).

A Feature with `# Architecture` `None` is not an error: say it is not designed
yet and that `sdlc-design-arch` designs it once it is `ReqApproved`.

## Recipe: show an endpoint or a consumer

For exactly one Endpoint or Subscription:

1. Summary: title, status, its Service, and `method` and `path`, or the
   channel it consumes.
2. Input: `# Request`, or the channel's payload linked from `# Consumes`.
3. Output: `# Response` with `## Status codes`, or the side effects named in
   `# Handler`.
4. `# Validations`, as stored.
5. `# Behavior` or `# Handler`.
6. The stored `# Flowchart` and `# Sequence diagram`, as they are.
7. `# Pending changes`, when present, with each entry's text.

## Recipe: show a user story

Stories are `STORY-*.md` files in a Feature's or ChangeRequest's folder
(`user-story.md`). For one story, give its sentence, its criteria, the
Requirements it lists, the Tasks whose `# Stories` link it, and its
`# Changed by` entries: a Feature story describes the Feature as first
delivered, and the ChangeRequest stories listed there describe later changes.

For "the paste-ready copy", "give me the story for the tracker" or similar,
print each story asked for as `references/paste-format.md` shows, and
nothing else.

## Free-form questions

- "What uses X?": open X and read its tool-written reverse section
  (`# Used by`, `# Publishers`, `# Subscribers`, a Reference's
  `# Referenced by`), else `grep -rl "<KEY>" wiki/`.
- "What should I read about X?", "is there an example of Y?": the References
  in `wiki/<app>/references/index.md` whose title or description matches,
  and those the concepts about X link under `# References`. Give each one's
  description, status and `resource`, and say when it is `Deprecated` or
  past its `stale_after`.
- "What is not live?": `grep -rl "^# Pending changes" wiki/`, then read the
  entries.
- "What is not tested, not planned or has no story?": `coverage tests`,
  `coverage tasks` and `coverage stories` (read-protocol section 3).
  `coverage stories` reporting every Functional Requirement means the
  Feature has no stories, which is allowed.
- "Why is it like this?": the decisions in `wiki/<app>/decisions/`, the
  concept's `log.md`, then `git log -p` on its folder.
- "Who confirmed it?": the `verified` stamps; a file without one is
  unconfirmed.
- "How far is this Task?": a Task is `Todo` until its code is merged, then
  `Done`. Say that progress in between is in the Tracker, and give the Task's
  `trackerKey` and `resource` when it has them.
