# Run plan: sdlc-plan-tasks, CR-sms-notifications
Intent approved 2026-10-03 · Design approved 2026-10-03

## Answers
1. The target is `CR-sms-notifications`, `Approved`. `coverage tasks --change CR-sms-notifications` reports one concept no Task plans: `TBL-notifications`.
2. `TASK-sms-channel` has started. It is not rewritten.
3. One new Task, `TASK-notifications-sms-value`: `dev`, size XS, in the notifications service's repository. Its planned scope is `TBL-notifications` — modified — `channel` accepts the value `sms`. Acceptance: a notification attempt with channel `sms` is stored, and a second attempt for the same order and channel is refused by the unique index. It satisfies REQ-order-notifications-channel-opt-out. It is blocked by nothing; `TASK-sms-channel` does not wait for it.
4. Nothing else in the wiki changes.

## Files
- [ ] change-requests/CR-sms-notifications/TASK-notifications-sms-value.md (add: TBL-notifications, modified)
- [ ] change-requests/CR-sms-notifications/log.md (change)
