package com.acme.orders;

import java.math.BigDecimal;
import java.time.Duration;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

@Service
public class OrderService {

    public enum Outcome { CREATED, DUPLICATE, DECLINED, EMPTY_CART }
    public enum Cancel { CANCELLED, NOT_FOUND, NOT_CANCELLABLE, VENDOR_FAILED }
    public record Result(Outcome outcome, UUID orderId, String status) {}

    private final JdbcTemplate db;
    private final PaymentsClient payments;
    private final ShipwellClient shipwell;
    private final OrderEventPublisher events;
    private final Duration cancelWindow;

    public OrderService(JdbcTemplate db, PaymentsClient payments, ShipwellClient shipwell, OrderEventPublisher events,
                        @Value("${orders.cancel-window-minutes}") long cancelWindowMinutes) {
        this.db = db;
        this.payments = payments;
        this.shipwell = shipwell;
        this.events = events;
        this.cancelWindow = Duration.ofMinutes(cancelWindowMinutes);
    }

    public Result create(OrderController.CreateOrder request) {
        Integer customers = db.queryForObject("SELECT count(*) FROM customers WHERE customer_id = ?", Integer.class, request.customerId());
        Integer open = db.queryForObject(
                "SELECT count(*) FROM carts WHERE cart_id = ? AND customer_id = ? AND status = 'open'",
                Integer.class, request.cartId(), request.customerId());
        // The total is the sum of the prices fixed when each item was added to the cart.
        BigDecimal total = db.queryForObject(
                "SELECT coalesce(sum(unit_price_usd * quantity), 0) FROM cart_items WHERE cart_id = ?",
                BigDecimal.class, request.cartId());
        Integer items = db.queryForObject("SELECT count(*) FROM cart_items WHERE cart_id = ?", Integer.class, request.cartId());
        if (customers == 0 || open == 0 || items == 0) {
            return new Result(Outcome.EMPTY_CART, null, null);
        }
        UUID orderId = UUID.randomUUID();
        try {
            db.update("INSERT INTO orders (order_id, customer_id, cart_id, total_usd, status, client_token, gift_note) "
                    + "VALUES (?, ?, ?, ?, 'pending_payment', ?, ?)",
                    orderId, request.customerId(), request.cartId(), total, request.clientToken(), request.giftNote());
        } catch (DuplicateKeyException retried) {
            // uq_orders_client_token: a retried submit returns the first order and pays nothing.
            Map<String, Object> first = db.queryForMap(
                    "SELECT order_id, status FROM orders WHERE customer_id = ? AND client_token = ?",
                    request.customerId(), request.clientToken());
            return new Result(Outcome.DUPLICATE, (UUID) first.get("order_id"), (String) first.get("status"));
        }
        PaymentsClient.Authorization authorization = payments.authorize(orderId, total, request.paymentMethod());
        if (!authorization.authorized()) {
            return new Result(Outcome.DECLINED, orderId, "pending_payment"); // the order stays pending_payment
        }
        db.update("UPDATE orders SET status = 'confirmed' WHERE order_id = ?", orderId);
        db.update("UPDATE carts SET status = 'ordered' WHERE cart_id = ?", request.cartId());
        events.orderCreated(orderId, request.customerId(), total, items, authorization.paymentId());
        return new Result(Outcome.CREATED, orderId, "confirmed");
    }

    public Optional<Map<String, Object>> find(UUID orderId, UUID customerId) {
        List<Map<String, Object>> rows = db.queryForList(
                "SELECT order_id, customer_id, total_usd, currency, status, gift_note, created_at FROM orders "
                + "WHERE order_id = ? AND customer_id = ?", orderId, customerId);
        return rows.stream().findFirst();
    }

    public List<Map<String, Object>> list(UUID customerId, int limit) {
        return db.queryForList(
                "SELECT order_id, customer_id, total_usd, currency, status, gift_note, created_at FROM orders "
                + "WHERE customer_id = ? ORDER BY created_at DESC LIMIT ?", customerId, limit);
    }

    public Cancel cancel(UUID orderId, UUID customerId) {
        Optional<Map<String, Object>> order = find(orderId, customerId);
        if (order.isEmpty()) {
            return Cancel.NOT_FOUND;
        }
        Instant created = ((java.sql.Timestamp) order.get().get("created_at")).toInstant();
        if (!"confirmed".equals(order.get().get("status")) || created.plus(cancelWindow).isBefore(Instant.now())) {
            return Cancel.NOT_CANCELLABLE;
        }
        if (!shipwell.cancelShipment(orderId)) {
            return Cancel.VENDOR_FAILED; // nothing changed; the caller may try again
        }
        db.update("UPDATE orders SET status = 'cancelled' WHERE order_id = ?", orderId);
        return Cancel.CANCELLED;
    }
}
