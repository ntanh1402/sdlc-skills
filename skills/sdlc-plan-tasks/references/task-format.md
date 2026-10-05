# Task format

A Task is one file in its parent's folder:
`wiki/<app>/features/FEAT-<name>/TASK-<name>.md` or
`wiki/<app>/change-requests/CR-<name>/TASK-<name>.md`. Its key is lower-case
words from its title, for example `TASK-refund-endpoint`. Read
`.wiki-llm/schema/task.md` for the rules.

```markdown
---
type: Task
title: Build the refund endpoint
description: Let support staff refund a captured payment.
status: Todo
taskType: dev
estimate: M
priority: P1
---

# Build the refund endpoint

# Acceptance

`POST /payments/{id}/refunds` refunds a captured payment once, returns 409 for a
second refund of the same request, and emits `payment.refunded`. Satisfies
[REQ-payments-refund](overview.md#req-payments-refund). In a ChangeRequest's
folder, link the Feature's copy:
`../../features/FEAT-payments/overview.md#req-payments-refund`.

# Stories

* [STORY-payments-refund-order](STORY-payments-refund-order.md)

# Planned scope

* [EP-refund-create](../../services/SVC-payments/EP-refund-create.md) — new — the endpoint.
* [TBL-refunds](../../datastores/DB-payments/TBL-refunds.md) — new — one row per refund.

# Blocked by

* [TASK-refunds-table](TASK-refunds-table.md)
```

- `status` starts at `Todo`. Leave `trackerKey` and `resource` out unless the
  user gave them: a person adds them when the ticket exists. Never write
  `mergedAt`, `mergeCommitSha` or `prUrl`; they are written when the Task is
  closed.
- Every link in `# Planned scope` points at a Design concept with the
  qualifier the design gave it, and that concept has a `# Pending changes`
  entry for this Task's parent.
- `# Stories` links user stories of this Task's own folder, and is left out
  when the Task serves none.
- `# Blocked by` is left out when the Task has no blocker.
- Do not write `generated` or `verified`; `draft finish` does.
