# Order Notifications — change log

Append-only history. Newest first.

## 2026-10-03

* **Status correction**: Marked the Feature Released; its only Task is Done and the email notification is live. The SMS channel is the open [CR-sms-notifications](../../change-requests/CR-sms-notifications/overview.md).

## 2026-10-01

* **Documentation**: Removed the stale "Pattern" sentence from `# Architecture`; the schema has no `pattern` field.

## 2026-07-14

* **Decision traceability**: Linked the approved Twilio ADR while implementation remains in progress.
* **Target architecture**: Added high-level/runtime diagrams and requirement traceability.

## 2026-07-13

* **SMS change**: Applied approved [CR-sms-notifications](../../change-requests/CR-sms-notifications/overview.md) target delta before implementation completion.
* **Documentation**: Added notification requirements, email/SMS architecture, tasks, and integration suite.
* **Documentation**: Added complete planned scope and traceability to Order Notifications.

## 2026-07-08

* **Email implementation**: [TASK-notifications-consumer](TASK-notifications-consumer.md) completed event consumption and confirmation email.
* **Completion**: Merged [PR 88](https://github.com/acme/notifications-service/pull/88) from `feat/notifications-consumer`.
