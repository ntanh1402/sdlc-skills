# Resume from a Run plan

## Wiki
`forward-tests/seed.sh <dir>`; then, in the wiki repository, `python3 .wiki-llm/tools/wiki_llm.py draft start tests-CR-sms-notifications` and `cp <this repository>/forward-tests/sdlc-design-feature-tests/resume-plan.plan.md .worktrees/tests-CR-sms-notifications/plan.md` (a run that ended right after its Design gate, before the first file).

## Request
"Continue the test design for the SMS change"

## Answers
- "yes, it still stands"
- Approve

## Expected
- Resumes the draft `tests-CR-sms-notifications` in its worktree; does not discard it and starts no second draft
- Shows the Run plan and asks one question: whether it still stands
- Asks no round and no Intent or Design approval again
- Writes the two cases of answer 3 into `TS-sms-notifications/GENERAL/` as `TC-2-…` and `TC-3-…`, each with `testType: integration`, a `testCategory`, `risk`, a `# Steps` table with bold validations and `# Covers` links, and the entry in `GENERAL/log.md`, ticking each
- No existing `TC-*.md` is changed and no new suite is made; no step names a wiki key
- `plan.md` has a `## Self review` section that names `coverage tests`, and the Change-set gate says only what it records
- Branch `wiki/tests-CR-sms-notifications` pushed; `plan.md` is not in it; `validate` ok
