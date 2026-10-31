# Resume from a Run plan

## Wiki
`forward-tests/seed.sh <dir>`; then, in the wiki repository, `python3 .wiki-llm/tools/wiki_llm.py draft start spec-FEAT-gift-cards`, then `cp <this repository>/forward-tests/sdlc-write-spec/resume-plan.plan.md .worktrees/spec-FEAT-gift-cards/plan.md`, then `mkdir -p .worktrees/spec-FEAT-gift-cards/wiki/shop/references/REF-gift-cards-prd` and `cp <this repository>/forward-tests/sdlc-write-spec/resume-plan.prd.md` to `prd.md` in that folder (a run that ended after its Design gate: the PRD is written, the other four files are not).

## Request
"Continue the gift cards spec"

## Answers
- "yes, it still stands"
- Approve

## Expected
- Resumes the draft `spec-FEAT-gift-cards` in its worktree; does not discard it and starts no second draft
- Shows the Run plan and asks one question: whether it still stands
- Asks no round and no Intent or Design approval again
- Writes the four other files of the plan; the Requirements are the three of answer 5, and the status is `ReqApproved`; `FEAT-gift-cards` links `REF-gift-cards-prd` under `# References`
- Stops at the Change-set gate
- Branch `wiki/spec-FEAT-gift-cards` pushed; `plan.md` is not in it; `validate` ok
