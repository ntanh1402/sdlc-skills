# sdlc-ask-wiki

Ask the wiki a question. It answers from the wiki's files and changes nothing.
[Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | Everyone: a PO checking status, a developer reading a design, QA checking coverage, a release manager checking what is not built |
| **Use when** | You want a list of Features, one Feature's architecture, what is not built yet, which tests cover a Requirement, a user story's paste-ready copy for a ticket, or the history of a decision |
| **Needs first** | A linked wiki. Nothing else |
| **Say** | "List the features", "Show the checkout architecture", "What is left to build for CR-sms-notifications?" |
| **You get** | The answer first, then the wiki files it read. It separates what the wiki says from what it infers |
| **Next** | Whatever the answer suggests. If the answer shows a gap, it names the skill that fixes it |

It is read-only. It starts no draft, writes no file and has no gates. It asks
only for what is genuinely missing: which Application, or which Feature when
several match.

## What the skill does

1. Finds the wiki and reads its default branch.
2. Searches cheaply (indexes, then a text search), then reads only the files
   the answer needs.
3. Answers the question, then cites the paths.
4. When nothing is found, says what it searched.

## What you do

Ask. Name the Application or Feature if there are several.

## Scenarios

| What happens | What the skill does | What you do |
|---|---|---|
| **"List the features."** | One row per Feature: key and title, status, owner and priority, whether it is designed, how many design items are not live, and open ChangeRequests. Explains an empty list | Ask "show the architecture of FEAT-x" for detail |
| **"Show the architecture of a Feature."** | Gives a summary, the requirements, the stored diagrams, the frontends, the services with their endpoints and subscriptions, the decisions, the traceability from each Requirement, what is not live yet, and gaps it noticed (broken links, requirements missing from traceability) | Read it. If it reports a difference with code, run [sdlc-import](sdlc-import.md) on that code to compare |
| **"Show an endpoint or a consumer."** | Gives its input, output with status codes, validations, behavior, and the stored flowchart and sequence diagram | Use it. Ask for it by key, for example `EP-orders-create` |
| **The Feature has no architecture yet** | Says it is not designed yet, and that [sdlc-design-arch](sdlc-design-arch.md) designs it once it is `ReqApproved` | Merge the spec, then design |
| **"Show me a user story."** | Gives the sentence, criteria, Requirements, the Tasks that link it, and its change history | Use it |
| **"Give me the story for the tracker."** | Prints the paste-ready copy of each story asked for, and nothing else | Paste it into a ticket. To record the ticket link in the wiki, ask [sdlc-edit-wiki](sdlc-edit-wiki.md) |
| **"What uses X?"** | Reads the reverse sections the tool writes (`# Used by`, `# Publishers`, `# Subscribers`), or searches for the key | Plan a change with the answer |
| **"What is not live yet?"** | Finds every design item with pending changes and reads the entries | Use before a release |
| **"What is not tested, planned, or has no story?"** | Runs the wiki's coverage checks. A Feature with no stories is allowed, because stories are optional | Run the skill that fills the gap |
| **"Why is it like this?"** | Reads the decisions, the concept's log, then the git history of its folder | |
| **"Who confirmed this file?"** | Reads the `verified` stamps. A file with none is unconfirmed | Ask the author to confirm it (`sdlc-edit-wiki` records it) |
| **"How far is this Task?"** | Says a Task is `Todo` until its code is merged, then `Done`. Progress in between is in your tracker, so it gives the Task's ticket link if it has one | Check the tracker |
| **Several Applications, and your question does not say which** | Asks which | Name it |
| **You ask it to change something** | Refuses and names the skill that does it | Run that skill |

## Not this skill

| Request | Use |
|---|---|
| Requirements | [sdlc-write-spec](sdlc-write-spec.md) |
| User stories | [sdlc-write-stories](sdlc-write-stories.md) |
| Architecture | [sdlc-design-arch](sdlc-design-arch.md) |
| Tasks, tests | [sdlc-plan-tasks](sdlc-plan-tasks.md), [sdlc-design-tests](sdlc-design-tests.md) |
| Bringing existing code, documents or tests in | [sdlc-import](sdlc-import.md) |
| Typos, glossary, released, ticket links | [sdlc-edit-wiki](sdlc-edit-wiki.md) |
| The wiki itself, a new Application | [sdlc-setup-wiki](sdlc-setup-wiki.md) |
| Writing a Task's code, or reviewing code | [sdlc-build-task](sdlc-build-task.md), [sdlc-review-code](sdlc-review-code.md) |
