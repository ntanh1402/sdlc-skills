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

**Drift**:
A difference between what a concept file says and what the code does that nothing in the wiki marks as not built yet: a `# Pending changes` entry, an `Approved` ChangeRequest on a Feature, or a TestSuite that is not `Implemented`.
_Avoid_: mismatch, out of sync, stale (the schema's `stale_after` is about age, not difference)

**Approval gate**:
One of the three points where a writing skill stops for the user's explicit approval: Intent (problem, outcome, scope), Design (the full PRD, architecture, task plan or test design), and Change-set (the Draft's diff and commit message).
_Avoid_: checkpoint, confirmation, review step

**Tracker**:
The system outside the Bundle where people create a Task's ticket and follow its progress; no skill reads or writes it.
_Avoid_: board, backlog, issue system

**User story**:
One actor's goal in a Feature or ChangeRequest, written as "As a …, I want …, so that …" with Given/When/Then acceptance criteria that each cite a Requirement it lists; a file `STORY-<name>.md`, optional, with no status.
_Avoid_: story (unqualified, in skill text), epic, use case

**Run plan**:
The list of things one run of one skill has to do to produce its output, with what is done so far; it belongs to the run and is never part of the Bundle.
_Avoid_: spec (the output of `sdlc-write-spec`), task plan (the output of `sdlc-plan-tasks`), todo list

**Actor**:
Who wrote or confirmed a file, as recorded in its provenance: `human:<id>`, `process:<id>`, or `<skill>/<Release version>` for a skill, never a model name.
_Avoid_: author, model, agent (as a provenance value)

**Release version**:
The number of a Release; it changes with tool or skill fixes that leave the Schema version unchanged.
_Avoid_: version (unqualified)
