# sdlc-import

Bring an existing, already built system into the wiki, or compare the wiki with
it. [Back to the user guide](user-guide.md).

## At a glance

| | |
|---|---|
| **Who** | Tech lead and architect (code, architecture documents, requirement documents); QA (test suites) |
| **Use when** | The project already exists and the wiki does not describe it yet (onboarding); or the wiki and the code may no longer agree; or a test suite has been written and its TestSuite must be marked `Implemented` |
| **Needs first** | The wiki is set up and the Application exists. A non-text document is converted first with [sdlc-convert-doc](sdlc-convert-doc.md). Its prerequisites are merged (see the order below) |
| **Say** | "Import the code of ../shop-orders", "Import docs/architecture.md", "Check the wiki against ../shop-orders" |
| **You get** | As-built Design files, `Released` Features, decisions and TestSuites, which you confirm group by group. In a compare run, you decide each difference |
| **Next** | Merge the import pull request. Then the next source in the order below |

It records **what is built and running today**. Anything not built yet goes to
[sdlc-write-spec](sdlc-write-spec.md).

## What it imports

One source per run:

| Source | It writes | Status written |
|---|---|---|
| **Code** of one service or frontend | The Service or frontend, its endpoints and subscriptions, and the tables, channels, stores and externals it uses that the wiki lacks | `Active` |
| **Architecture document** | The Application's architecture, decisions, conventions, glossary, a Service page for each service the wiki lacks, and the document as a Reference | Decisions `Accepted`; Services `Active` |
| **Requirement document** (PRD, functional spec) | One as-built Feature per capability, with the document as a Reference | `Released` |
| **A built capability with no document** | One as-built Feature | `Released` |
| **Test code** (end-to-end, integration, load, security) | One TestSuite and one TestCase per test | `Implemented` |
| **Test document** (test plan, sheet of manual cases) | One TestSuite and its TestCases, with the document as a Reference | `Approved` (`Implemented` if you say the runnable tests exist) |

**The order for a new project:** design first, then Features, then tests. Import
the code or architecture document first, then the requirement document or
capability, then the tests. Import the code of a folder before its tests.

## What the skill does

1. Reads the source and the wiki, and decides whether it is **creating** or
   **comparing** (the main concept is already in the wiki).
2. Asks the first round. It lists what the source leaves open, each with a
   recommended answer: where the source is, what kind, which Application,
   which team owns it, whether it is built and running, how current it is.
3. **Intent gate:** restates all this and the draft key (for example
   `wiki/import-SVC-orders`).
4. Prepares every file and shows the Run plan.
5. **Design gate, group by group:** shows each group of files in full and ends
   with one question (see below). Files are written as soon as their group is
   answered.
6. Shows three lists before the change set: *Could not determine*, *Not
   modelled*, *Disagreements*.
7. Self review, then **Change-set gate**, then commit.

## What you do

- Give the folder or file path. The skill never guesses it. "This folder" is an
  answer.
- Answer for each group of files: **Approve**, **Change** (it corrects and shows
  the group again), or **"Save it, I did not check it"** (written without a
  confirmation stamp).
- Read the three lists. Decide each disagreement yourself.
- Merge the pull request.

## Scenarios

| What happens | What the skill does | What you do |
|---|---|---|
| **Onboarding a code folder** | Records the service or frontend, endpoints, subscriptions and the data it uses. Names every source as the repository URL, the path and the commit it read | Confirm each group. Provide the owner team, which code does not say |
| **The repository holds several services** | Imports one service per run and asks for the URL of that service's folder | Give it, then repeat for the other services |
| **The code folder has uncommitted changes** | Says the recorded commit will not match the files it read, and asks whether to go on | Commit first, or accept |
| **The code has no git remote** | Asks for the repository URL | Give it |
| **The folder holds code and tests** | Treats them as two runs, the code first | Run the second after the first is merged |
| **An architecture document names a service the wiki lacks** | Asks for that service's repository URL, owner team and type. Without all three the service is listed as *not imported* | Give them, or import that service's code later |
| **You say "import all of it"** | Lists the sources it sees and the order, and does the first only | Run the next ones yourself |
| **A prerequisite is not in the wiki.** A requirement document describes a service that is not imported, for example | Stops before the Intent gate and names the run to do first. If the prerequisite is in an unmerged draft, it names that draft | Do that run, or merge the draft |
| **The source describes something not built** | Stops: "use sdlc-write-spec" | Write the spec instead |
| **The source is partly built** | Imports the built part and lists the rest for a ChangeRequest | Run [sdlc-write-spec](sdlc-write-spec.md) for the rest |
| **A document is partly out of date** | Leaves that part out and lists it | Tell it which part, and decide what to do with it |
| **A document is a PDF or Word file** | Asks for the Markdown | Run [sdlc-convert-doc](sdlc-convert-doc.md) first |
| **A required field is missing** (an owner team, an idempotency note, a fallback) | Asks before showing the group. With no answer, a prose section gets the line "Not determined by the import." and you can fill it in; a section that must hold a table or a diagram cannot, so that file is not written | Answer, or accept the gap |
| **A group contains a Reference** (a document copy) | Does not allow "save unchecked": the schema needs a person's confirmation on a Reference | Read it and approve |
| **The source is already in the wiki** | Switches to a **compare** run | See the next rows |
| **Compare: a file matches** | Reports it. You may confirm it | Confirm if you checked |
| **Compare: a difference the wiki marks as not built yet** | Reports it as expected | Nothing |
| **Compare: any other difference** | Asks one numbered round with no recommendation: keep the wiki, take what the source says, or "the code is wrong" | Decide each one. The skill never chooses |
| **Compare: "take what the source says"** | Corrects only a file that records what exists (an `Active` Design file, a `Released` Feature, an `Accepted` decision, a TestSuite, the Application's own files). If the correction removes a Requirement that user stories or TestCases list, it fixes those in the same draft | Check the corrected files |
| **Compare: a file points at something the code dropped** | Marks it `Deprecated` and keeps the file | Approve |
| **Compare: you answer "keep the wiki"** | Writes nothing for that file. The run does not confirm it | Nothing |
| **Compare: you answer "the code is wrong"** | Writes nothing and says: open a bugfix ChangeRequest with [sdlc-write-spec](sdlc-write-spec.md) | Run it |
| **Documents and code disagree** | Code wins for contracts (endpoints, tables, channels). Documents add requirements, reasons and diagrams. Every disagreement is listed, none resolved | Decide |
| **The source contains a secret or personal data** | Never copies it. It names the setting, not the value | Nothing |
| **A test document describes tests that exist as code** | Imports the document as a suite, `Implemented` when you say the runnable tests exist | Say so |
| **You reject the whole import** | Discards a draft this run started | Nothing |
| **The run stops half-way** | Next time it continues from the first group with no answer | Run it again |

## Not this skill

| Request | Use |
|---|---|
| A new capability, a change, a bug fix | [sdlc-write-spec](sdlc-write-spec.md) |
| User stories (an import writes none) | [sdlc-write-stories](sdlc-write-stories.md) |
| Tasks or tracker issues (never imported) | [sdlc-plan-tasks](sdlc-plan-tasks.md) |
| Review a code change against the wiki | [sdlc-review-code](sdlc-review-code.md) |
| Run tests or import unit tests | Not a skill |
| A typo that needs no source to check against | [sdlc-edit-wiki](sdlc-edit-wiki.md) |
