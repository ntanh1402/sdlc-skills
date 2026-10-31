# Run plan: sdlc-design-tests, CR-sms-notifications
Intent approved 2026-10-03 · Design approved 2026-10-03

## Answers
1. The target is `CR-sms-notifications`, `Approved`. Its suite is `TS-order-notifications` (integration); `TC-sms-sent` already covers the opt-out Requirement.
2. One type, `integration`, at the same seams as the suite: a real message in, the Twilio call stubbed, the `notifications` table asserted. No `load` and no `security` suite: the change adds no latency target and no new access rule.
3. Two branches of the SMS sequence have no case: Twilio answers with a failure, and the same `order.created` message is delivered twice. Add one case for each to `TS-order-notifications`:
   - `TC-sms-provider-failure-recorded`, risk medium: Twilio returns a failure; the attempt is stored with the outcome `failed`, the email is still sent, and the message is not retried inside the handler.
   - `TC-sms-redelivery-sends-once`, risk high: the same message arrives twice; one SMS is sent and one row exists for `(order_id, sms)`.
4. No existing case changes.
5. Nothing else in the wiki changes.

## Files
- [ ] tests/TS-order-notifications/TC-sms-provider-failure-recorded.md (add: the failure branch of OP-messages-create)
- [ ] tests/TS-order-notifications/TC-sms-redelivery-sends-once.md (add: the unique index on TBL-notifications)
- [ ] tests/TS-order-notifications/log.md (change)
