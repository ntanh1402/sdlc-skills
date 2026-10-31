# Resume from a Run plan

## Wiki
`forward-tests/seed.sh <dir> --fixture gift-cards-spec`; then, in the wiki repository, `python3 .wiki-llm/tools/wiki_llm.py draft start stories-FEAT-gift-cards` and `cp <this repository>/forward-tests/sdlc-write-stories/resume-plan.plan.md .worktrees/stories-FEAT-gift-cards/plan.md` (a run that ended right after its Design gate, before the first file).

## Request
"Continue the gift card stories"

## Answers
- "yes, it still stands"
- Approve

## Expected
- Resumes the draft `stories-FEAT-gift-cards` in its worktree; does not discard it and starts no second draft
- Shows the Run plan and asks one question: whether it still stands
- Asks no round and no Intent or Design approval again
- Writes the two stories as answers 2 and 3 say, and the log entry, ticking each
- `plan.md` has a `## Self review` section that names `coverage stories`
- Branch `wiki/stories-FEAT-gift-cards` pushed; `plan.md` is not in it; `coverage stories --feature FEAT-gift-cards` empty; `validate` ok
- The paste-ready copy of both stories is printed before the summary
