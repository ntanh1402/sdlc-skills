# Run plan: sdlc-design-feature-tests, CR-sms-notifications
Intent approved 2026-10-03 · Design approved 2026-10-03

## Answers
1. The target is `CR-sms-notifications`, `Approved`. Its suite is `TS-sms-notifications`; `GENERAL/TC-1-sms-sent` (integration) already covers the opt-out Requirement.
2. One test type, `integration`, at the same seams as the group: a real message in, the Twilio call stubbed, the `notifications` table asserted. No `security-validation` cases: the change adds no new access rule.
3. Two branches of the SMS sequence have no case: Twilio answers with a failure, and the same `order.created` message is delivered twice. Add one case for each to `TS-sms-notifications/GENERAL/` (the CR has no user story):
   - `TC-2-sms-provider-failure-recorded`, `error-handling`, risk med: Twilio returns a failure; the attempt is stored with the outcome `failed`, the email is still sent, and the message is not retried inside the handler.
   - `TC-3-sms-redelivery-sends-once`, `error-handling`, risk high: the same message arrives twice; one SMS is sent and one row exists for `(order_id, sms)`.
4. No existing case changes.
5. Nothing else in the wiki changes.

## Files
- [ ] tests/TS-sms-notifications/GENERAL/TC-2-sms-provider-failure-recorded.md (add: the failure branch of OP-messages-create)
- [ ] tests/TS-sms-notifications/GENERAL/TC-3-sms-redelivery-sends-once.md (add: the unique index on TBL-notifications)
- [ ] tests/TS-sms-notifications/GENERAL/log.md (change)
