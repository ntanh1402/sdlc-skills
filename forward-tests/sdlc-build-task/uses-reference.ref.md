---
type: Reference
title: Request validation in the orders controller
description: Code example of how the orders service validates a request body and shapes a 400 error; read before building an endpoint of the orders service.
status: Active
resource: https://github.com/acme/orders-service/blob/v1.0.0/src/main/java/com/acme/orders/OrderController.java
generated: { by: human:sample-author, at: 2026-10-06T09:00:00Z }
verified: { by: human:sample-author, at: 2026-10-06T09:00:00Z }
---

# Request validation in the orders controller

`OrderController` checks every required field before it calls the service and
answers a bad request with a 400 whose body names each failing field.

Follow: the validation before any side effect, and the error body.

Do not copy: the request logging, which writes the whole body.

# Contents

None
