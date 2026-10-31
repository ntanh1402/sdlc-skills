---
type: Reference
title: Idempotency key handling in the orders service
description: Code example of how the orders service makes a create request safe to repeat; read before building an endpoint that must not act twice.
status: Active
resource: https://github.com/acme/orders-service/blob/v1.4.0/src/orders/idempotency.ts
stale_after: 2027-06-01T00:00:00Z
generated: { by: human:sample-author, at: 2026-10-06T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-06T09:00:00Z }
---

# Idempotency key handling in the orders service

The orders service stores the client's idempotency key with the order in one
transaction, and answers a repeated key with the first response. The code is
at `resource`, pinned to the `v1.4.0` tag.

Follow:

* the key is read from the `Idempotency-Key` header and is required;
* the key and the stored response are written in the same transaction as the
  row they protect;
* a repeated key returns the stored status and body, never a new error.

Do not copy:

* the in-memory retry loop around the payment call; a payment retry belongs to
  the caller, as [ADR-idempotent-checkout](../../decisions/ADR-idempotent-checkout.md)
  says.

# Contents

None

# Referenced by

* [Implement order creation endpoint](../../features/FEAT-checkout/TASK-order-creation-endpoint.md)
