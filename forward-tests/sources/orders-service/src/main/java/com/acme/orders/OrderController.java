package com.acme.orders;

import java.util.Map;
import java.util.UUID;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

/** The HTTP contract of the orders service. Every route needs a customer session token. */
@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService orders;

    public OrderController(OrderService orders) {
        this.orders = orders;
    }

    public record CreateOrder(UUID cartId, UUID customerId, String paymentMethod, String clientToken, String giftNote) {}

    /** POST /orders: 201 created, 409 already created, 402 declined, 422 empty cart or invalid, 400 malformed. */
    @PostMapping
    public ResponseEntity<?> create(@AuthenticationPrincipal UUID caller, @RequestBody CreateOrder body) {
        if (body.cartId() == null || body.customerId() == null || body.paymentMethod() == null || body.clientToken() == null) {
            return ResponseEntity.badRequest().build();
        }
        if (!caller.equals(body.customerId()) || (body.giftNote() != null && body.giftNote().length() > 200)) {
            return ResponseEntity.unprocessableEntity().build();
        }
        OrderService.Result result = orders.create(body);
        return switch (result.outcome()) {
            case CREATED -> ResponseEntity.status(201).body(Map.of("orderId", result.orderId(), "status", "confirmed"));
            case DUPLICATE -> ResponseEntity.status(409).body(Map.of("orderId", result.orderId(), "status", result.status()));
            case DECLINED -> ResponseEntity.status(402).build();
            case EMPTY_CART -> ResponseEntity.unprocessableEntity().build();
        };
    }

    /** GET /orders/{id}: another customer's order is 404, never 403. */
    @GetMapping("/{id}")
    public ResponseEntity<?> get(@AuthenticationPrincipal UUID caller, @PathVariable UUID id) {
        return orders.find(id, caller)
                .map(order -> ResponseEntity.ok(Map.of("order", order)))
                .orElse(ResponseEntity.notFound().build());
    }

    /** GET /orders?customerId=: the caller's own orders, newest first; limit 1..100, default 20. */
    @GetMapping
    public ResponseEntity<?> list(@AuthenticationPrincipal UUID caller, @RequestParam UUID customerId,
                                  @RequestParam(defaultValue = "20") int limit) {
        if (!caller.equals(customerId)) {
            return ResponseEntity.status(403).build();
        }
        return ResponseEntity.ok(Map.of("orders", orders.list(customerId, Math.min(Math.max(limit, 1), 100))));
    }

    /** POST /orders/{id}/cancel: only a confirmed order, only inside the cancel window. */
    @PostMapping("/{id}/cancel")
    public ResponseEntity<?> cancel(@AuthenticationPrincipal UUID caller, @PathVariable UUID id) {
        return switch (orders.cancel(id, caller)) {
            case CANCELLED -> ResponseEntity.ok(Map.of("orderId", id, "status", "cancelled"));
            case NOT_FOUND -> ResponseEntity.notFound().build();
            case NOT_CANCELLABLE -> ResponseEntity.status(409).build();
            case VENDOR_FAILED -> ResponseEntity.status(502).build();
        };
    }
}
