# Resume from a Run plan

## Wiki
`forward-tests/seed.sh <dir>`; then, in the wiki repository, `python3 .wiki-llm/tools/wiki_llm.py draft start tasks-CR-sms-notifications` and `cp <this repository>/forward-tests/sdlc-plan-tasks/resume-plan.plan.md .worktrees/tasks-CR-sms-notifications/plan.md` (a run that ended right after its Design gate, before the first file).

## Request
"Continue planning the SMS tasks"

## Answers
- "yes, it still stands"
- Approve

## Expected
- Resumes the draft `tasks-CR-sms-notifications` in its worktree; does not discard it and starts no second draft
- Shows the Run plan and asks one question: whether it still stands
- Asks no round, not which Tasks have started, and no Intent or Design approval again
- Writes `TASK-notifications-sms-value.md` as answer 3 says (`status: Todo`, `TBL-notifications` in `# Planned scope`) and the log entry, ticking each
- `TASK-sms-channel.md` is unchanged
- `plan.md` has a `## Self review` section that names `coverage tasks`, and the Change-set gate says only what it records
- Branch `wiki/tasks-CR-sms-notifications` pushed; `plan.md` is not in it; `coverage tasks --change CR-sms-notifications` reports nothing; `validate` ok
