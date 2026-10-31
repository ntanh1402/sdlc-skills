package com.acme.orders;

import java.util.UUID;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;

/** Shipwell is the shipping vendor. The only call: stop the shipment of a cancelled order. */
@Component
public class ShipwellClient {

    private final RestClient http;

    public ShipwellClient(@Value("${shipwell.base-url}") String baseUrl, @Value("${shipwell.api-key}") String apiKey) {
        this.http = RestClient.builder().baseUrl(baseUrl).defaultHeader("Authorization", "Bearer " + apiKey).build();
    }

    /** DELETE /v1/shipments/{orderId}; 2 s timeout, no retry. 404 means nothing was booked yet, which is fine. */
    public boolean cancelShipment(UUID orderId) {
        try {
            http.delete().uri("/v1/shipments/{orderId}", orderId).retrieve().toBodilessEntity();
            return true;
        } catch (org.springframework.web.client.HttpClientErrorException.NotFound nothingBooked) {
            return true;
        } catch (RestClientException failed) {
            return false;
        }
    }
}
