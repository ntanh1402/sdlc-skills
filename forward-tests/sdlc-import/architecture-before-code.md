# Architecture before code

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

empty + orders + documents

Keep the directory.

## Request
"Import docs/architecture-overview.md"

## Answers
- built, except the loyalty part; dated 2026-03-10; orders service: `https://github.com/acme/orders-service`, `payments`, `api`; payments service: `https://github.com/acme/payments-service`, `payments`, `api`

## Expected
- Draft `import-architecture-overview`
- `wiki/shop/references/REF-architecture-overview/` is a Reference: `overview.md` summarises the document and lists `architecture-overview.md` under `# Contents`; that content file holds the whole document, with `architecture-overview.svg` beside it
- the Application's `overview.md`, both Service pages and both decisions link `REF-architecture-overview` under `# References`; no file names it in `sources`
- the Application's `# Architecture` has a `flowchart`
- `SVC-orders` and `SVC-payments` pages, `Active`, with no Endpoint
- two decisions: the replaced one `Superseded`, the other `Accepted` with `# Supersedes`, `decisionDate` 2025-02-03 and 2025-09-18
- `conventions.md` and `glossary.md`
- "not imported" lists the `order.created` topic, Stripe, the database and the web storefront, each with "import its code"
- the loyalty service is in no file but the Reference and is named for `sdlc-write-spec`
- `validate` ok
