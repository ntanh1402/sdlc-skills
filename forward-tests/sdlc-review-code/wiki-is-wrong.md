# Wiki is wrong

## Wiki
Seeding: `refund` is `forward-tests/seed.sh <dir> --fixture order-refund-cr --source orders-service --change orders-service:orders-refund`. In every scenario also check that nothing was written: `git status --short` is empty in the wiki and the code repository, no branch `wiki/*` exists, and the Task's status is unchanged.

as `without-task.md`

## Request
"As `without-task.md`; then: "The wiki is out of date. Refunds were designed last month.""

## Answers
- "there is no Task"

## Expected
- Names the remedy and changes nothing: a ChangeRequest with `sdlc-write-spec` for a design that is not built, or `sdlc-import` on the same folder for a wrong record. The findings stay
