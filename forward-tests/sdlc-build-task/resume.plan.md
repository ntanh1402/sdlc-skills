# Run plan: sdlc-build-task, TASK-order-note-put
Intent approved 2026-10-03 · Design approved 2026-10-03

## Answers
1. The Task is `TASK-order-note-put` of `FEAT-order-notes`; the code folder is `../orders-service`.
2. The branch is `task/order-note-put`, the worktree `../orders-service/.worktrees/order-note-put`.
3. The route goes into the existing `OrderController`, next to the other `/orders` routes; the rule for the text (1 to 500 characters) is checked there, and `OrderService` stores it.
4. The column is added by a new migration, `V3`, as `support_note text NULL` with a length check, like `gift_note` in `V2`.
5. Unit tests go in `tests/unit/`, as `OrderTotalTest` does.
6. Nothing in the wiki changes.

## Files
- [x] db/migration/V3__order_support_note.sql (add: column support_note on orders; TBL-orders)
- [ ] src/main/java/com/acme/orders/OrderService.java (change: storeNote, 404 for an unknown order; EP-orders-note-put; acceptance 1 and 3)
- [ ] src/main/java/com/acme/orders/OrderController.java (change: PUT /orders/{id}/note, 204, 422 for a text that is empty or over 500 characters; EP-orders-note-put; acceptance 1 and 2)
- [ ] openapi.yaml (change: the new route)
- [ ] tests/unit/OrderNoteTest.java (add: 204, replace, 422 empty, 422 too long, 404; acceptance 1 to 3)
