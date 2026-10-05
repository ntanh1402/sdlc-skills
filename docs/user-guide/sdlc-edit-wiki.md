# sdlc-edit-wiki

Make a small edit to the wiki that no other skill owns.
[Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | Anyone: a release manager marking a release, a tech lead adding ticket links, an author fixing a typo |
| **Use when** | You need a typo or wording fix; a glossary or conventions change; a Feature marked `Released` or `Deprecated`; a Task's or user story's ticket or pull request link; or a record that a person confirmed a file |
| **Needs first** | The file exists on the wiki's default branch. For `Released`: the Feature is `InDev`, no Task is `Todo`, and no design item still has a pending entry for it |
| **Say** | "Mark FEAT-gift-cards released, shipped today", "Add ticket SHOP-142 to TASK-gift-card-redeem" |
| **You get** | A small draft, `wiki/edit-<key>`. Anything that changes what someone would build or test is refused, and the skill names the skill to use instead |
| **Next** | Merge the pull request |

This skill uses the short form: it asks only when something is unclear, then
stops once to show the exact old and new text, then once for the change set.

## What it can edit

| Allowed | Rule |
|---|---|
| A typo or wording fix in any file a person writes | The meaning of a contract, Requirement or acceptance item does not change |
| `glossary.md` and `conventions.md` of the Application | Terms, roles and rules, added, changed or removed |
| A Feature's status to `Released` or `Deprecated` | `Released` only from `InDev`, with the release time you give. Only when none of its Tasks is `Todo` and no design item has a pending entry for it |
| A Task's `trackerKey`, `resource` and `prUrl` | The ticket and pull request you followed by hand. Never its status |
| A user story's `trackerKey` and `resource` | The ticket you made from the story's paste-ready copy |
| A `verified` stamp | You say you read the file and it is right |

## What you do

- Say exactly what to change. If you give only the fault, the skill proposes the
  wording; if you give no release time, it asks.
- Approve the old-to-new text, then the change set.
- Merge the pull request.

## Scenarios

| What happens | What the skill does | What you do |
|---|---|---|
| **A typo or a wording fix** | Shows the old and new text and writes it. A typo in a file that holds a target not built yet (a `Planned` design file, or a Feature before `Released`) is still a typo, but the target itself is never changed | Approve |
| **A glossary or conventions change** | Edits the Application's file. These files have no log, so the commit message says what changed | Approve |
| **You release a Feature after deploying** | Sets `Released` and `releasedAt`, adds a log entry | Deploy first, then ask, with the time |
| **`Released`, but a Task is still `Todo`** | Refuses, names the Tasks and says each is closed with [sdlc-close-task](sdlc-close-task.md) after its code is merged | Close them |
| **`Released`, no `Todo` Task, but a pending entry is left** | Refuses and names the files. A close that is not merged yet usually explains it | Merge the close pull request, then ask again |
| **You deprecate a Feature that has `Todo` Tasks or pending entries** | Refuses and names them. No skill withdraws an approved design | Remove the entries, the `Planned` files and the `Todo` Tasks by hand, then ask again |
| **You add a ticket link to a Task** | Writes `trackerKey`, `resource` or `prUrl`. It never changes the status | Give the ticket key and URL |
| **You add a ticket link to a story** | Writes `trackerKey` and `resource` | Give them |
| **You say "I read this file and it is right"** | Records the confirmation stamp | Be sure you read it |
| **You want to change a Requirement** | Refuses. [sdlc-write-spec](sdlc-write-spec.md) | Run it |
| **You want a new or changed design, contract or concept** | Refuses. A ChangeRequest with [sdlc-write-spec](sdlc-write-spec.md), then [sdlc-design-arch](sdlc-design-arch.md) | Run them |
| **You want a story added, regrouped or its criteria changed** | Refuses. [sdlc-write-stories](sdlc-write-stories.md) | Run it |
| **You want a Task added, or its scope, acceptance or stories changed** | Refuses. [sdlc-plan-tasks](sdlc-plan-tasks.md) | Run it |
| **You want a TestCase or TestSuite changed** | Refuses. [sdlc-design-tests](sdlc-design-tests.md); [sdlc-import](sdlc-import.md) for a correction | Run it |
| **You want a Task's status changed** | Refuses. [sdlc-close-task](sdlc-close-task.md), after the code is merged | Close it |
| **The wiki is wrong about what is built** | Refuses. [sdlc-import](sdlc-import.md) compares and corrects | Run it |
| **Your request mixes allowed and refused edits** | Does the allowed part and lists the rest under "For other skills", each with its skill | Run the other skills |
| **Unsure if the edit is a wording fix** | Applies one test: would a developer or tester do anything differently afterwards? If yes, it is refused | Use the skill it names |
| **You reject the plan** | Writes nothing | Nothing |

## Not this skill

| Request | Use |
|---|---|
| Requirements, architecture, tasks, test design | The lifecycle skills of [the flow](user-guide.md#the-flow) |
| Corrections checked against code or documents | [sdlc-import](sdlc-import.md) |
| Closing a Task | [sdlc-close-task](sdlc-close-task.md) |
| A question about the wiki | [sdlc-ask-wiki](sdlc-ask-wiki.md) |
