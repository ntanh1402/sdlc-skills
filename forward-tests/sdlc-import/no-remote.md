# No remote

## Wiki
Seeding: `empty` is `forward-tests/seed.sh <dir> --empty`, `sample` is `forward-tests/seed.sh <dir>`; `+ orders` adds `--source orders-service`, `+ documents` adds the three document sources. See Task 10 of the plan for States A to E.

empty + orders; then `git -C <dir>/orders-service remote remove origin`

## Request
"Import the code in ../orders-service"

## Answers
- repository URL `https://git.acme.example/shop/orders`

## Expected
- Asks for the repository URL
- the Service's `resource` and every `sources` entry use the answer
