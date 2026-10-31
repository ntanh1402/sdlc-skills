# Forward tests

Each file `forward-tests/<skill>/<scenario>.md` is one scenario: a starting
wiki, a request, the tester's answers, and the expected behaviour. They test a
skill the way a user meets it. Run them by hand, with any agent, after every
change to a skill.

## Running a scenario

1. **Seed** a scratch setup, plus any extra steps in the scenario's `## Wiki`:

   ```bash
   forward-tests/seed.sh /tmp/ft/<skill>-<scenario> [--empty] [--fixture <name>]... \
     [--source <name>]... [--change <source>:<name>]... \
     [--code <name>]... [--merged <code>:<name>[:<Task key>]]...
   ```

   It prints the wiki repository and the workspace. The workspace's
   `AGENTS.md` links the wiki. The wiki has a bare remote, so drafts push.

   `--source <name>` adds a made-up Import source from `forward-tests/sources/`.
   A folder (`orders-service`) becomes a git repository `<dir>/<name>` beside
   the workspace, with the remote URL `https://github.com/acme/<name>.git`
   (a made-up URL: nothing can be fetched from it or pushed to it); a
   document (`checkout-prd.md`) is copied to `<dir>/workspace/docs/`, with the
   files that share its name. `--change <source>:<name>` commits
   `forward-tests/changes/<name>.patch` in that source on a new branch
   `feat/<name>`: a code change for `sdlc-review-code`. The sources are read by
   the skills, never built or run.

   `--code <name>` copies the same folder as a code repository with a real
   remote, the bare repository `<dir>/<name>.git`, and the default branch
   `main`: `sdlc-build-task` builds a Task in it and `sdlc-close-task` reads
   its merged commits. `--merged <code>:<name>[:<Task key>]` commits
   `forward-tests/changes/<name>.patch` on its `main` and pushes it; with a
   Task key the commit message ends with `Task: <Task key>`.
2. **Install** this clone's skills for the tester agent:
   link or copy `skills/*` into the agent's skills folder. For Claude Code,
   `<dir>/workspace/.claude/skills` keeps the test apart from your own skills.
3. **Start a fresh agent session in `<dir>/workspace`.** Send the `## Request`
   exactly. Answer the agent as `## Answers` says; answer anything else with the
   most plausible short answer and note it. Never show the agent the
   `## Expected` section.
4. **Check** every line of `## Expected` against the conversation and the
   repositories: `git -C <dir>/shop-wiki branch -a`,
   `git -C <dir>/remote.git log --all --oneline`, and in the wiki
   `python3 .wiki-llm/tools/wiki_llm.py validate` on the pushed branch
   (`git checkout <branch>` in a copy).
5. **Record** PASS or FAIL with one line of evidence in the plan's
   "Forward-test results" table. A FAIL is fixed in the skill and the scenario
   is run again from step 1.

A tester may also be a fresh sub-agent, given the installed skills' names and
descriptions, the workspace path and the Request. Run it turn by turn: it
ends its turn whenever it needs the user, and you answer from `## Answers`.
Do not ask one agent to play both sides of the conversation; such runs were
cut off by model safeguards.

## Scenario file

```markdown
# <Scenario title>

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec`; then <extra steps>.

## Request
"<what the user types>"

## Answers
- Intent gate: <answer>
- Design gate: <answer>
- Change-set gate: <answer>

## Expected
- <one observable result per line>
```
