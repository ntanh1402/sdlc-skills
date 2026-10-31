package com.acme.orders;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.slf4j.MDC;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

/** Publishes one order.created event per confirmed order. Key: the order id. Body schema version 1.1. */
@Component
public class OrderEventPublisher {

    private final KafkaTemplate<String, Map<String, Object>> kafka;
    private final String topic;

    public OrderEventPublisher(KafkaTemplate<String, Map<String, Object>> kafka, @Value("${orders.topic}") String topic) {
        this.kafka = kafka;
        this.topic = topic;
    }

    public void orderCreated(UUID orderId, UUID customerId, BigDecimal totalUsd, int itemCount, UUID paymentId) {
        String now = Instant.now().toString();
        Map<String, Object> body = new HashMap<>();
        body.put("orderId", orderId);
        body.put("customerId", customerId);
        body.put("totalUsd", totalUsd);
        body.put("currency", "USD");
        body.put("itemCount", itemCount);
        body.put("placedAt", now);
        if (paymentId != null) {
            body.put("paymentId", paymentId);
        }
        ProducerRecord<String, Map<String, Object>> record = new ProducerRecord<>(topic, orderId.toString(), body);
        header(record, "message-id", UUID.randomUUID().toString());
        header(record, "event-type", "order.created");
        header(record, "event-version", "1.1");
        header(record, "occurred-at", now);
        header(record, "correlation-id", MDC.get("correlation-id"));
        header(record, "producer", "SVC-orders");
        kafka.send(record);
    }

    private static void header(ProducerRecord<String, ?> record, String name, String value) {
        record.headers().add(name, value.getBytes(java.nio.charset.StandardCharsets.UTF_8));
    }
}
