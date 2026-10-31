# Resume from a Run plan

## Wiki
`forward-tests/seed.sh <dir> --fixture checkout-endpoint-cr`; then, in the wiki repository, `python3 .wiki-llm/tools/wiki_llm.py draft start arch-CR-checkout-address-validation` and `cp <this repository>/forward-tests/sdlc-design-arch/resume-plan.plan.md .worktrees/arch-CR-checkout-address-validation/plan.md` (a run that ended right after its Design gate, before the first file).

## Request
"Continue the design of the address validation change"

## Answers
- "yes, it still stands"
- Approve

## Expected
- Resumes the draft `arch-CR-checkout-address-validation` in its worktree; does not discard it and starts no second draft
- Shows the Run plan and asks one question: whether it still stands
- Asks no round and no Intent or Design approval again
- Writes the six files of the plan, `overview.md` of the ChangeRequest first, ticking each; the design is the one of the answers: the check is in `SVC-orders`, `EP-orders-create` is `Modifying` with `422` and a pending entry, no new concept and no new decision
- `CR-checkout-address-validation` is `Approved`; `FEAT-checkout` has `REQ-checkout-deliverable-address`
- `plan.md` has a `## Self review` section, and the Change-set gate says only what it records
- `TASK-order-creation-endpoint` and `TS-checkout` are not edited; the summary has a "For other skills" line
- Branch `wiki/arch-CR-checkout-address-validation` pushed; `plan.md` is not in it; `validate` ok
