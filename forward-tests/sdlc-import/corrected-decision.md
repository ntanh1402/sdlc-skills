# Corrected decision

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

a copy of State A; then change "older than seven days" to "older than five days" in `<dir>/workspace/docs/architecture-overview.md`

## Request
"Import docs/architecture-overview.md"

## Answers
- "take what the document says"; approve

## Expected
- Finds `REF-architecture-overview` by the key it would propose and compares
- the decision's `# Consequences` and the Reference's content file are corrected; the Reference has a `**Correction**` entry in its `log.md` and the person's `verified` again
- the proposed commit message has a line `Correction: wiki/shop/decisions/ADR-<name>.md, checked against architecture-overview.md`
