# sdlc-write-spec

Write the requirements of a new Feature, or of a ChangeRequest to an existing
Feature. [Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | Business analyst, product owner |
| **Use when** | You define a new capability, turn a brief into requirements, write a PRD, or change an existing Feature (a bug, a security, performance or refactor change), or revise requirements that are not designed yet |
| **Needs first** | The Application exists. If the input is a PDF or Word file, convert it first with [sdlc-convert-doc](sdlc-convert-doc.md) |
| **Say** | "Write the spec for gift cards: customers pay part or all of an order with a gift card balance", "Add SMS as a second notification channel" |
| **You get** | A **Feature** (`FEAT-…`) with a PRD and Requirements, or a **ChangeRequest** (`CR-…`) when the Feature is already designed. Draft branch `wiki/spec-<Key>` |
| **Next** | Merge the spec pull request. Then [sdlc-design-arch](sdlc-design-arch.md), and [sdlc-write-stories](sdlc-write-stories.md) at the same time if you want user stories |

## What the skill does

1. Searches the wiki for features that already own the capability, and decides
   the **mode**: new Feature, revise a Feature, new ChangeRequest, or revise a
   ChangeRequest. You confirm it.
2. Asks the rounds. The first round shows what it found (Application, mode,
   target, change type and risk for a ChangeRequest) and the questions about the
   requirements: outcome, users, why now, flow, constraints, risks, scope.
3. **Intent gate:** restates the outcome, users, each Requirement (key, priority,
   type, how it is verified), success measures, risks, assumptions, open
   questions and what is out of scope.
4. Writes the PRD straight to its file and prepares a table that maps each
   Requirement to the PRD text it came from.
5. **Design gate:** shows the **full PRD** and the mapping, then asks two
   questions: is the PRD approved as written, and are the requirements
   **approved for design** (`ReqApproved`) or still a draft?
6. Writes `overview.md`, the PRD and `log.md`, checks them, then the
   **Change-set gate** and the commit.

## What you do

- Describe the capability or the change. A brief is enough; the skill does not
  ask what the brief already says.
- Confirm the mode and the target Feature.
- Answer the rounds, read the PRD in full at the Design gate, and choose
  `ReqApproved` only when you want design to start.
- Merge the pull request.

## Scenarios

| What happens | What the skill does | What you do |
|---|---|---|
| **A new capability** no Feature owns | Writes a new Feature, status `Draft` | Approve; choose `ReqApproved` at the Design gate when ready |
| **The Feature exists and is `Draft`** | Revises that Feature | Say what changes |
| **The Feature exists and is `ReqApproved`** | Revises it and puts it back to `Draft` until approved again. It says so in the first round | Re-approve at the Design gate |
| **The Feature is `Approved` or later** | Writes a new **ChangeRequest** (`Proposed`) instead. It never edits the target Feature | Choose the change type and risk it proposes |
| **You revise an open ChangeRequest** (`Proposed` or `ReqApproved`) | Revises it. A `ReqApproved` one goes back to `Proposed` | Re-approve |
| **You revise an `Approved` ChangeRequest** | Writes a new ChangeRequest | Approve |
| **You say "new feature" but one already owns that behaviour** | The exact match wins. It asks you to confirm the existing Feature | Confirm, or name a different Feature |
| **You describe a change but no Feature owns the behaviour** | It cannot silently make a new Feature. It asks | Say whether it is new |
| **Several features could match** | Asks one question naming the candidates and writes nothing until you answer | Pick one |
| **Your brief already lists Requirements** | Takes them as given, with your wording and count. It does not split, add or reword them. A flow or rule without a Requirement stays in the PRD as context | Nothing, unless a Requirement is wrong |
| **Your brief contradicts itself or the wiki** | Asks at most two scope questions, only about the contradiction | Resolve it |
| **The brief describes something already running** | Asks once whether it is built. If yes it stops: "this is already built; use sdlc-import" | Run [sdlc-import](sdlc-import.md) |
| **The Application does not exist** | Stops and routes to [sdlc-setup-wiki](sdlc-setup-wiki.md) ("add application `<key>`") | Add it, then ask again |
| **The same key is already used** (a folder or an open draft) | Picks another key from the title | Confirm |
| **Your revision removes a Requirement** that user stories or TestCases list | Fixes those stories and cases in the same draft (drops the link and the criteria that only cite it; deletes a story left with no requirement), shows the edits at the Design gate and logs them | Check the edits |
| **You correct the PRD at the Design gate** | Edits the file and asks the gate again | Re-approve |
| **You want to keep working on it** | Answer "draft" at the second question: the status stays `Draft` (Feature) or `Proposed` (ChangeRequest) | Come back later, run the skill again |
| **A run stops part-way** | Next time it finds the draft and asks whether its plan still stands | Say yes or change it |
| **You reject the intent** | Writes nothing | Nothing |
| **You ask for a typo fix, architecture, tasks or tests** | Names the skill: [sdlc-edit-wiki](sdlc-edit-wiki.md), [sdlc-design-arch](sdlc-design-arch.md), [sdlc-plan-tasks](sdlc-plan-tasks.md), [sdlc-design-tests](sdlc-design-tests.md) | Run that skill |

## Not this skill

| Request | Use |
|---|---|
| A question about the wiki | [sdlc-ask-wiki](sdlc-ask-wiki.md) |
| A PDF or Word file as input | [sdlc-convert-doc](sdlc-convert-doc.md) first |
| Something already built and running | [sdlc-import](sdlc-import.md) |
| Architecture, stories, tasks, tests | [sdlc-design-arch](sdlc-design-arch.md), [sdlc-write-stories](sdlc-write-stories.md), [sdlc-plan-tasks](sdlc-plan-tasks.md), [sdlc-design-tests](sdlc-design-tests.md) |
| A typo, the glossary, a Feature marked released | [sdlc-edit-wiki](sdlc-edit-wiki.md) |
| A bug diagnosis | Not a wiki skill. Once you know the fix, write it up here as a ChangeRequest |
