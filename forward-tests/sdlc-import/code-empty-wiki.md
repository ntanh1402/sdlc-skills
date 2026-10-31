# Code empty wiki

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

empty + orders

Keep the directory.

## Request
"Import the code in ../orders-service"

## Answers
- Approve every group and gate as the usual answers.

## Expected
- The questions come in numbered rounds, each with the answer the code shows as its recommendation; the first round names the kind (code) and "create", and asks what else in the wiki this source touches
- One Intent gate, after the rounds
- the Intent gate names the kind (code), "create", the draft `import-SVC-orders`, the URL `https://github.com/acme/orders-service` and the commit
- the Run plan is shown before the first group: `<wiki>/.worktrees/import-SVC-orders/plan.md` lists the files under their groups
- the Design gate shows the groups in order (Service page, Endpoints, Tables, Channel, external with its Operation), every file in full; the files of a group are written after its answer, and the Run plan records each answer on the group's heading
- the three lists are shown after the last group, before the Change-set gate, and not again after the commit
- the Change-set gate shows the diff and the commit message
- branch `wiki/import-SVC-orders` pushed; `plan.md` is not in it
- the last message is the summary, at most four lines; "Next" names the next run
- `services/SVC-orders/overview.md` has `status: Active` and that `resource`
- four `EP-*.md` (create, get, list, cancel)
- a Table for `orders` with `gift_note`
- a Channel for `order.created` with `payload.example.json`
- `EXT-shipwell` with one Operation
- every file has a `sources` entry `id: code` with that URL and a `title` "`<path> at <commit>`"
- `generated.by` is `sdlc-import/2.5.<n>` and `verified.by` `human:tester`
- no file has `# Pending changes`
- "Could not determine" names the call to the payments service ("import its code"), the tables `carts`, `cart_items` and `customers` (read, with no schema in this repository) and the Channel's `## Dead letter`, which holds `Not determined by the import.`
- "Not modelled" names the nightly job, which the Service page describes in prose
- `grep -r "Xk9-orders" wiki/` finds nothing
- `validate` ok
