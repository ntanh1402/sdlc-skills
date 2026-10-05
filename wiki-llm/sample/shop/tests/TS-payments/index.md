# Payments Unit Suite

* [Overview](overview.md) - Unit tests for authorize/capture logic and idempotency.

# Test cases

* [Amount mismatch rejected](TC-amount-mismatch-rejected.md) - Prove caller cannot authorize an amount different from order total.
* [Authorize is idempotent](TC-authorize-is-idempotent.md) - Prove repeated authorization cannot double charge.
* [Authorize success](TC-authorize-success.md) - Prove successful authorization persists and emits once.
* [Decline is terminal](TC-decline-is-terminal.md) - Prove card decline is stable, visible, and not retried.

# History

* [Change log](log.md) - History of Payments Unit Suite.
