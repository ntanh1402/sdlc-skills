# Upgrade a wiki whose Task serves two stories

## Wiki
`forward-tests/seed.sh <dir>`; then in the wiki copy
`forward-tests/fixtures/task-with-two-stories/.` over `wiki/` (the older
Given/When/Then stories, and `TASK-order-creation-endpoint` linking both),
run `python3 .wiki-llm/tools/wiki_llm.py sync`, set `.wiki-llm/manifest.json`
`release_version` to `0.9.0`, commit, push.

## Request
"upgrade the wiki"

## Answers
- Upgrade: approve
- Which story TASK-order-creation-endpoint keeps: the recommendation
- Every other gate: approve

## Expected
- Offers the upgrade, in a draft `wiki/setup-<version>`
- After `copy install`, names TASK-order-creation-endpoint as serving two stories
- Asks in one round which story it keeps, recommending
  STORY-checkout-pay-and-confirm (its `# Acceptance` cites
  REQ-checkout-complete-purchase, which only that story lists)
- Drops the link to STORY-checkout-retry-safely and changes nothing else in
  the Task
- Adds an `**Upgrade**` entry to `FEAT-checkout/log.md` naming the kept
  story and the dropped one
- Does not rewrite either story: their Given/When/Then criteria stay valid
- `draft finish` is `ok`
- After the commit, says to run sdlc-plan-tasks for FEAT-checkout only if it
  is open; FEAT-checkout is Released, so the retry story keeps no Task and
  nothing is suggested for it
