# Order Notifications Suite

* [Overview](overview.md) - Integration tests for the order notification flow.

# Test cases

* [Email sent](TC-email-sent.md) - Prove one order event produces one recorded email delivery.
* [Provider outage does not fail checkout](TC-provider-outage-does-not-fail-checkout.md) - Prove notification outage is isolated from checkout and retried.
* [Redelivery is idempotent](TC-redelivery-is-idempotent.md) - Prove broker redelivery cannot duplicate customer contact.
* [SMS sent](TC-sms-sent.md) - Prove SMS honors customer opt-out.

# History

* [Change log](log.md) - History of Order Notifications Suite.
