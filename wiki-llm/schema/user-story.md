# UserStory

[Common rules](schema.md)

One actor's goal in a Feature or ChangeRequest: the Requirements it groups,
stated as pass/fail acceptance criteria. It lives in the folder of the
Feature or ChangeRequest whose Requirements it lists.

<!-- generated:schema start -->
|  |  |
|---|---|
| Type | `UserStory` |
| Phase | Plan |
| Path | `<app>/features/FEAT-*/STORY-<name>.md or <app>/change-requests/CR-*/STORY-<name>.md` |
| Shape | One file |
| Status | None; this type has no `status` field |

### Fields

| Field | Required | Values |
|---|---|---|
| `type` | yes | `UserStory` |
| `title` | yes | text |
| `description` | yes | text |
| `basedOn` | yes | `{ version, at }`: a spec version and its `YYYY-MM-DD` |
| `trackerKey` | no | text |
| `priority` | no | `P0`, `P1`, `P2`, `P3` |
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
| `# Acceptance criteria` | required | author |  |  |  |
| `# Requirements` | required | author | Requirement (1 or more) |  |  |
| `# Affects` | optional | author | UserStory (any number) |  |  |
| `# Notes` | optional | author |  |  |  |
| `# References` | optional | author | Reference (any number) |  |  |
| `# Changed by` | when not empty | tool | mirrors UserStory `# Affects` |  |  |
| `# Test cases` | when not empty | tool | mirrors TestCase `# Covers`, TestCase `# Covers` via its `# Requirements`, TestCase `# Covers` via Task `# Stories` via its `# Planned scope` |  |  |
<!-- generated:schema end -->

## Rules

- The prose between the title and `# Acceptance criteria` is the story
  sentence: "As a …, I want …, so that …".
- `# Acceptance criteria` is a numbered list and nothing else. Each item is
  one pass/fail statement with real values (an input it takes or refuses, a state
  or output it produces, a boundary, a rejection), and links at least one
  Requirement listed under `# Requirements`. Each Requirement under
  `# Requirements` is linked by at least one item. A rule no Requirement
  supports is a gap in the Requirements, not a criterion. Data and steps
  belong to the TestCases. Older stories written as **Given** / **When** /
  **Then** scenarios stay valid.
- `# Requirements` lists at least one Functional Requirement. It links the
  `overview.md` of the story's own folder: in a ChangeRequest's folder, the
  ChangeRequest's copy, never the Feature's, because the Feature has no copy
  of an added Requirement until the design is approved.
- Every Functional Requirement that is not **Wont** is listed by at least one
  story, once the Feature or ChangeRequest has stories. Nonfunctional
  Requirements and Constraints may be listed. One Requirement may be in
  several stories.
- `# Affects` appears only in a ChangeRequest's folder. It links the stories
  of the changed Feature that list a Requirement this request changes.
- `# Changed by` is written by the tool from `# Affects`. A Feature story
  describes the Feature as first delivered; a ChangeRequest never rewrites
  it, and its own stories describe the change.
- The key is `STORY-<feature-name>-<name>`, where `<feature-name>` is the
  Feature key without `FEAT-` (the changed Feature's, for a ChangeRequest).
- `basedOn` is the version of the story's own folder's Feature or
  ChangeRequest that the story was written from. See
  [Spec versions](schema.md#spec-versions).
- A story has no `status`: progress is followed in the tracker. `resource` is
  the tracker ticket URL and `trackerKey` its key; a person adds them.
- A Task links the one story it serves under `# Stories`. `sdlc-plan-tasks`
  links every story to at least one Task of its folder; a story with no Task
  is not a validation error.
- `# Test cases` is written by the tool: the TestCases whose `# Covers` links
  a Requirement under the story's `# Requirements`, and those that cover a
  concept in the `# Planned scope` of a Task linking the story. A case may be
  listed on several stories. QA starts from this list to test the story; it
  may include cases of a shared concept that test more than the story.
- A step that removes a Requirement fixes the stories that list it in the
  same change: it drops the Requirement from `# Requirements` and each
  criterion that links only that Requirement, and deletes a story left with
  no Functional Requirement, with the links to it under `# Stories` and
  `# Affects`. Nothing else in a story is rewritten by that step.
