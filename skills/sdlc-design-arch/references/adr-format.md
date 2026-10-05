# Architecture decision format

All decisions of an Application share one folder:
`wiki/<app>/decisions/ADR-<name>.md`, where `<name>` is lower-case words from
the decision's title, for example `ADR-twilio-for-sms`. Read
`.wiki-llm/schema/architecture-decision.md` for the rules.

```markdown
---
type: ArchitectureDecision
title: Twilio for SMS
description: Send order SMS through Twilio's Messages API.
status: Accepted
ownerTeam: notifications
decisionDate: 2026-10-02
---

# Twilio for SMS

# Context

The forces and constraints.

# Decision

The choice, and why.

# Alternatives

What was rejected, and why.

# Consequences

Benefits, costs, risks and follow-up obligations.

# Affected concepts

* [EXT-twilio](../externals/EXT-twilio/overview.md)
* [CR-sms-alerts](../change-requests/CR-sms-alerts/overview.md)
```

- Record only a material choice with a credible alternative. Routine detail
  belongs in the Design concept's contract.
- The Feature or ChangeRequest that produced the decision links it under
  `## Decisions`.
- To replace a decision, write a new one whose `# Supersedes` links the old
  one, and set the old one's status to `Superseded`. Never edit the old
  decision's content. The old one's `# Superseded by` is written by the tool.
- Do not write `generated` or `verified`; `draft finish` does.
