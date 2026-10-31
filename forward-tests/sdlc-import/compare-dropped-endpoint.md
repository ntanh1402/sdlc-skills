# Compare dropped endpoint

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

sample `--fixture order-refund-cr` + orders; then the steps "refund-built" below

Setup, run in `<dir>/shop-wiki`:
```bash
sed -i 's/^status: Approved/status: Implemented/' wiki/shop/change-requests/CR-order-refund/overview.md
sed -i 's/^status: Todo/status: Done/' wiki/shop/change-requests/CR-order-refund/TASK-refund-endpoint.md
R=wiki/shop/services/SVC-orders/EP-orders-refund.md
sed -i 's/^status: Planned/status: Active/' $R
sed -i '/^# Pending changes/,$d' $R
python3 .wiki-llm/tools/wiki_llm.py sync && python3 .wiki-llm/tools/wiki_llm.py validate && git add -A && git commit -qm "scenario setup" && git push -q
```

## Request
"Import the code in ../orders-service"

## Answers
- "take what the code says" for the refund endpoint; "keep the wiki" for the rest; "leave the new files out"

## Expected
- Says the code has no refund endpoint
- finds the `Implemented` ChangeRequest and the `Done` Task that link the file
- keeps the file with `status: Deprecated`
- the ChangeRequest and the Task are unchanged
