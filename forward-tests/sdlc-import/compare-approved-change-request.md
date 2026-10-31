# Compare approved change request

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

sample `--fixture order-refund-cr` + orders; then the steps "feature-holds-target" below

Setup, run in `<dir>/shop-wiki`:
```bash
sed -i 's|^# Architecture$|### REQ-checkout-refund-order\n\n**Should** — A confirmed order can be refunded in full, once, with a reason. Functional. Verified by test.\n\n# Architecture|' wiki/shop/features/FEAT-checkout/overview.md
python3 .wiki-llm/tools/wiki_llm.py sync && python3 .wiki-llm/tools/wiki_llm.py validate && git add -A && git commit -qm "scenario setup" && git push -q
```

## Request
"Compare FEAT-checkout with what is built; the code is in ../orders-service"

## Answers
- "keep the wiki" for any other difference

## Expected
- Reports `REQ-checkout-refund-order` as expected, naming `CR-order-refund` (`Approved`, not built)
- writes nothing about it
