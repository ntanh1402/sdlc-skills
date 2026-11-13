# TestGroup

[Common rules](schema.md)

One folder of a [TestSuite](test-suite.md): `STORY-<name>/` holds the cases
that prove one user story of the suite's target, `GENERAL/` the cases that
prove no single story, of any type. Each group is written, reviewed and
approved on its own.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `TestGroup` |
| Phase | Verify |
| Path | `<app>/tests/TS-*/STORY-<name>/ or <app>/tests/TS-*/GENERAL/` |
| Shape | Folder with `index.md`, `overview.md`, `log.md` |
| Status | `Draft`, `Approved`, `Implemented`, `Deprecated` |
| Owns | TestCase |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `TestGroup` |
| `title` | yes | text |
| `description` | yes | text |
| `status` | yes | `Draft`, `Approved`, `Implemented`, `Deprecated` |
| `basedOn` | yes | `{ version, at }`: a spec version and its `YYYY-MM-DD` |
| `generated` | yes | `{ by, at }` |
| `verified` | no | `{ by, at }`, or a list of them |
| `sources` | no | list of `{ id, resource, title }` |
| `resource` | no | URL or bundle path |
| `stale_after` | no | ISO 8601 timestamp with offset |
| `tags` | no | `[a, b]` |

### Headings

| Heading | Presence | Written by | Links to | Qualifier | Content |
|---|---|---|---|---|---|
| `# <title>` | required; first heading | author |  |  |  |
| `# Story` | optional | author | UserStory (exactly 1) |  |  |
| `# Scope` | optional | author |  |  |  |
| `# Open questions` | optional | author |  |  |  |
| `# References` | optional | author | Reference (any number) |  |  |
<!-- generated:schema end -->

## Rules

- The folder is named after a user story of the suite's target, or is
  `GENERAL`. A `STORY-*` group links that story under `# Story`; `GENERAL`
  has no `# Story` and must say under `# Scope` which flows it covers.
- `basedOn` is the version of the suite's target the cases were designed
  from. See [Spec versions](schema.md#spec-versions).
- `status` is the group's design lifecycle: `Draft` while cases are being
  written, `Approved` once reviewed, `Implemented` when runnable tests exist.
  The wiki does not record pass and fail results.
- Each case of a `STORY-*` group links the story under `# Covers` with the
  acceptance criteria it proves (`— AC 1, 3`), and covers at least one
  Requirement the story lists. Every criterion of the story is proved by at
  least one case of the group.
- A broken link to the group's own story is a warning (the story was removed);
  any other broken link is an error.
- `# Open questions` is a numbered list of questions about the
  Requirements, acceptance criteria or design that the cases cannot settle;
  each item links what it is about. A group with open questions is `Draft`.
  The run that applies an answer removes the question and logs the answer in
  `log.md`.
- Story warnings, not errors: an orphaned group (a story removed or renamed outside
  `wiki_llm.py rename`), a criterion number that no longer exists, a
  criterion no case proves, a case that covers none of its story's
  Requirements. `sdlc-write-stories` may leave these; `sdlc-design-story-tests`
  fixes them before it approves the group.
