# Compare pending other difference

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

sample `--fixture order-refund-cr` + orders; then the steps "pending-other" below

Setup, run in `<dir>/shop-wiki`:
```bash
E=wiki/shop/services/SVC-orders/EP-orders-create.md
sed -i 's/^status: Active/status: Modifying/' $E
printf '\n# Pending changes\n\n* [CR-order-refund](../../change-requests/CR-order-refund/overview.md) — modified — a refunded cart cannot be ordered again; not built yet.\n' >> $E
sed -i 's|^\* \[EP-orders-refund\].*— new — the refund endpoint.$|&\n* [EP-orders-create](../../services/SVC-orders/EP-orders-create.md) — modified — refuses a cart whose order was refunded.|' wiki/shop/change-requests/CR-order-refund/overview.md
python3 .wiki-llm/tools/wiki_llm.py sync && python3 .wiki-llm/tools/wiki_llm.py validate && git add -A && git commit -qm "scenario setup" && git push -q
```

## Request
"Import the code in ../orders-service"

## Answers
- "keep the wiki" for the Table; "leave the new files out"

## Expected
- For `EP-orders-create.md`: reports the pending entry of `CR-order-refund` and the difference it does not describe (`giftNote`)
- writes nothing to that file and names the ChangeRequest. `EP-orders-refund.md` is reported as expected: not built yet
