# A person confirms a file

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"I read the carts table page, TBL-carts, and it is right. Record that I confirmed it"

## Answers
- Approve each gate

## Expected
- Runs `verify` on `wiki/shop/datastores/DB-shop/TBL-carts.md` in the draft worktree
- The file's `verified` gains a stamp `human:tester`; the earlier stamp is kept as a list entry, and its content is otherwise unchanged
- A `**Verification**` entry in `DB-shop/log.md`
- `validate` ok
