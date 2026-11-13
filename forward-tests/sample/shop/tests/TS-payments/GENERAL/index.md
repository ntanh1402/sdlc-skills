# General

* [Overview](overview.md) - Payment cases tied to no single story.

# Test cases

* [Authorize success](TC-1-authorize-success.md) - Prove successful authorization persists and emits once.
* [Authorize is idempotent](TC-2-authorize-is-idempotent.md) - Prove repeated authorization cannot double charge.
* [Amount mismatch rejected](TC-3-amount-mismatch-rejected.md) - Prove caller cannot authorize an amount different from order total.
* [Decline is terminal](TC-4-decline-is-terminal.md) - Prove card decline is stable, visible, and not retried.

# History

* [Change log](log.md) - History of General.
