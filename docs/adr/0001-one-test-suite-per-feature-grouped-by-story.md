# One test suite per Feature or ChangeRequest, grouped by user story

Schema version 2 replaces one TestSuite per Feature and test type with one TestSuite per Feature or ChangeRequest (`TS-<name>`). The suite is only a container: `# Verifies` and the tool-written `checklist.csv`, with no status, spec version or log. It owns TestGroups: a `STORY-<name>/` group for each user story whose cases are written, and `GENERAL/` for cases that prove no single story. Each group has its own overview, log, status, `basedOn` and open questions, because two skills write it: `sdlc-design-story-tests` writes one story's group and `sdlc-design-feature-tests` writes `GENERAL/`, and each approves only its own. Each case file is `TC-<id>-<name>.md` with an id unique in the suite, from 1, never reused; the id is in the filename only, so it cannot drift from a second copy. A story case links its story under `# Covers` with the acceptance criteria it proves (`— AC 1, 3`).

A case has `testType` (how it runs: integration or e2e) and an optional `testCategory` (what it checks: functional, field-validation, negative, error-handling, data-validation, security-validation, integration). Security is a category, not a type, because it says what is checked, not how the case runs.

## Considered Options

- Suite per test type (schema 1): rejected, a story's cases were spread over several suites.
- One skill for the whole suite: rejected, one story's tests could not be designed or approved without the whole Feature's.
- Status and `basedOn` on the suite: rejected, two skills approving one status would block each other, and a spec change often touches one story only.
- Naming the no-story folder `E2E` and keeping it e2e-only: rejected, cases for a nonfunctional Requirement or moved from a gone story have nowhere else to go.
- Anchors on each acceptance criterion: rejected, it changes the story format, its paste-ready tracker copy and every existing story, and the numbers still shift on renumbering.
- Keeping `load`: rejected; load tests are not designed or imported into the wiki.

## Consequences

- Schema 1 suites are removed by `migrate`; the test design skills write them again.
- Story drift is a warning, not an error: a deleted story, a criterion number that no longer exists, a criterion no case proves. `sdlc-write-stories` changes stories without touching tests and still finishes; the test skills fix the warnings before approving. A rename moves the story's group.
- Renumbering a story's criteria silently shifts the AC numbers its cases name; the story skill rereads the criteria on each run.
- Steps carry real resource names (table `account`, topic `orders.created`), so a design without `tableName`, `channelName` or `path` blocks test design until `sdlc-design-arch` adds it.
