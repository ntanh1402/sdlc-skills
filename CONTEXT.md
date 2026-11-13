# SDLC Skills

AI skills run a software project's lifecycle by reading and writing a knowledge bundle of Markdown files. This repository is the home of the schema, the tool and the skills that act on a bundle; they work with any AI agent that reads skill folders.

## Language

**Bundle**:
The folder of Markdown concept files that holds one project's knowledge, rooted at an `index.md` that carries `schema_version`.
_Avoid_: wiki (when the folder is meant), knowledge base

**Wiki repository**:
A project's own git repository whose purpose is to hold its Bundle.
_Avoid_: wiki repo, bundle repo

**Workspace**:
The folder an AI agent is started in, linked to one Wiki repository by a note in its agent instruction file; it may be the Wiki repository itself.
_Avoid_: project folder, working directory

**Release**:
One numbered version of the skills, the schema and the tool, published from this repository; a user installs its skills into any AI agent, and `sdlc-setup-wiki` installs its tool into a Wiki repository.
_Avoid_: plugin, package, distribution

**Tool copy**:
The copy of the schema and the tool kept inside a Wiki repository, taken from one Release; skills and CI run this copy.
_Avoid_: vendored tool, local tool

**Schema version**:
The version of the bundle rules a Bundle was written against, recorded in its root `index.md`.
_Avoid_: version (unqualified)

**Key**:
The name that identifies a concept within its Application, made of a type prefix and a descriptive name (`CR-coupon-codes`), never a sequence number.
_Avoid_: ID number, sequence

**Lifecycle step**:
One stage of the lifecycle that one writing skill performs, usually by one role (a business analyst writes the spec, a solution architect the architecture); a step reads only what earlier steps merged into the default branch.
_Avoid_: phase (the schema's Phase is a concept grouping), stage

**Draft**:
One lifecycle step's unapproved changes to a Bundle, held on their own branch until a pull request merges them; the next step starts only from what is merged.
_Avoid_: proposal, overlay, staging

**Import source**:
An existing code folder, document or test suite of a project that an import reads to write concept files; each file written from it names it in `sources`.
_Avoid_: resource (the schema field `resource` is the real asset a concept describes), input, artifact

**Spec version**:
The number of a Feature's or ChangeRequest's revision of its Requirements and PRD, from 1, kept in its `version` field; the design, user stories, Tasks and TestSuites written from it record it in `designBasedOn` or `basedOn`.
_Avoid_: revision (unqualified), Schema version, Release version

**Outdated**:
Written from an older Spec version than the target now has; reported by the tool and cleared by writing the file again, by a person confirming it is still current, or, for a `Done` Task, by planning a new Task for the difference and updating its `basedOn`. An approved target has no outdated Task.
_Avoid_: stale (the schema's `stale_after` is about age), out of sync, Drift (which compares the wiki with code)

**Drift**:
A difference between what a concept file says and what the code does that nothing in the wiki marks as not built yet: a `# Pending changes` entry, an `Approved` ChangeRequest on a Feature, or a TestSuite that is not `Implemented`.
_Avoid_: mismatch, out of sync, stale (the schema's `stale_after` is about age, not difference)

**Approval gate**:
One of the three points where a writing skill stops for the user's explicit approval: Intent (problem, outcome, scope), Design (the full PRD, architecture, task plan or test design), and Change-set (the Draft's diff and commit message).
_Avoid_: checkpoint, confirmation, review step

**Tracker**:
The system outside the Bundle (Jira, with Confluence for pages) where people follow the progress of Features, ChangeRequests, User stories and Tasks; only `sdlc-sync-atlassian` reads or writes it, and the Bundle owns the content while the Tracker owns status, assignee and sprint.
_Avoid_: board, backlog, issue system

**User story**:
One actor's goal in a Feature or ChangeRequest, written as "As a …, I want …, so that …" with numbered pass/fail acceptance criteria that each cite a Requirement it lists; a file `STORY-<name>.md`, optional, with no status.
_Avoid_: story (unqualified, in skill text), epic, use case

**Foundation Task**:
A Task that serves no User story, because several stories need what it builds and none owns it; the Tasks that use it wait for it. A Task serves at most one User story.
_Avoid_: shared task, common task, epic task

**Reference**:
Material a person approved for others to read while they work: a PRD, a change brief, a test plan, an architecture document, a page explaining a domain term, a vendor's documentation or a code example; a folder `references/REF-<name>/` of one Application whose `overview.md` summarises it, linked from any concept under `# References`. It is context, never a contract.
_Avoid_: source document, attachment, doc

**Run plan**:
The list of things one run of one skill has to do to produce its output, with what is done so far; it belongs to the run and is never part of the Bundle.
_Avoid_: spec (the output of `sdlc-write-spec`), task plan (the output of `sdlc-plan-tasks`), todo list

**Actor**:
Who wrote or confirmed a file, as recorded in its provenance: `human:<id>`, `process:<id>`, or `<skill>/<Release version>` for a skill, never a model name.
_Avoid_: author, model, agent (as a provenance value)

**Release version**:
The number of a Release; it changes with tool or skill fixes that leave the Schema version unchanged.
_Avoid_: version (unqualified)

**Test suite**:
The container of the test design of one Feature or ChangeRequest: its Test groups. It has no status of its own; each Test group is approved on its own.
_Avoid_: test plan, integration suite, e2e suite (a suite has no type)

**Test case**:
One test, of type integration or e2e, written so a tester who did not design the system can run it from its steps alone.
_Avoid_: scenario, test script

**Test case id**:
The number of a Test case, unique within its Test suite, counting from 1 and never reused after the case is deleted.
_Avoid_: test number, step number

**Test group**:
A folder of a Test suite with its own overview, log and open questions: one per user story the suite proves, plus the General group.
_Avoid_: sub-suite, story suite

**General group**:
The Test group that holds the Test cases tied to no single user story, of any type.
_Avoid_: E2E folder, cross-story folder

**Orphaned group**:
A Test group named after a user story that was split, merged or deleted. The tool warns; `sdlc-design-feature-tests` moves its Test cases to the General group.
_Avoid_: stale group, story drift

**Test category**:
What a Test case checks: functional, field validation, negative, error handling, data validation, security validation or integration with a downstream system. Separate from its type, which says how it runs.
_Avoid_: test type (for this meaning), security test
