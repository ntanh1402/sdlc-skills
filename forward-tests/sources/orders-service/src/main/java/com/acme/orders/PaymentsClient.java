package com.acme.orders;

import java.math.BigDecimal;
import java.util.Map;
import java.util.UUID;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestClient;

/** Calls the payments service, another service of the shop. Synchronous, 3 s timeout, no retry. */
@Component
public class PaymentsClient {

    public record Authorization(boolean authorized, UUID paymentId) {}

    private final RestClient http;

    public PaymentsClient(@Value("${payments.base-url}") String baseUrl) {
        this.http = RestClient.create(baseUrl);
    }

    /** POST /payments/authorize with orderId, amountUsd and paymentMethod; 402 means declined. */
    public Authorization authorize(UUID orderId, BigDecimal amountUsd, String paymentMethod) {
        try {
            Map<?, ?> body = http.post().uri("/payments/authorize")
                    .body(Map.of("orderId", orderId, "amountUsd", amountUsd, "paymentMethod", paymentMethod))
                    .retrieve().body(Map.class);
            return new Authorization(true, UUID.fromString((String) body.get("paymentId")));
        } catch (HttpClientErrorException.PaymentRequired declined) {
            return new Authorization(false, null);
        }
    }
}
