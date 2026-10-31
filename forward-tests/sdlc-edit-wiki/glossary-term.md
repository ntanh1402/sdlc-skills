# A glossary term

## Wiki
`forward-tests/seed.sh <dir>`.

## Request
"Add 'Gift note' to the shop glossary: a short message the buyer adds to an order, up to 200 characters"

## Answers
- Approve each gate

## Expected
- Draft `edit-glossary`
- `wiki/shop/glossary.md` gains one row under `# Terms`; no other row changes
- No log entry is invented for the Application's files; the commit message says what changed
- `validate` ok
