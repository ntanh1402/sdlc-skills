# Resume from a Run plan

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

empty + orders; then, in the wiki repository, `python3 .wiki-llm/tools/wiki_llm.py draft start import-SVC-orders` and `cp <this repository>/forward-tests/sdlc-import/resume-plan.plan.md .worktrees/import-SVC-orders/plan.md` (a run that ended after its Intent gate, before the first group was shown).

## Request
"Continue the import of the orders service, the code is in ../orders-service"

## Answers
- "yes, it still stands"
- Approve every group and gate

## Expected
- Resumes the draft `import-SVC-orders` in its worktree; does not discard it and starts no second draft
- Shows the Run plan and asks one question: whether it still stands
- Asks no round and no Intent approval again
- Continues at the first group with no answer, the Service page, and shows every group in full; a path of the plan may change when the code shows another name, and the plan is then corrected and said
- Writes the files of each group after its answer, ticks them and records the answer on the group's heading
- The three lists are shown before the Change-set gate
- The Change-set gate shows the diff and the commit message
- Branch `wiki/import-SVC-orders` pushed; `plan.md` is not in it; `validate` ok
