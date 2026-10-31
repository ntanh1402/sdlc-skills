package com.acme.orders.e2e;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Map;
import java.util.UUID;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/** End-to-end checkout tests. They run against a deployed stack with Stripe in test mode. */
class CheckoutE2ETest {

    private Stack stack;      // helper: seeds data through the public API and reads the database and the topic
    private UUID customer;
    private UUID cart;
    private String session;

    @BeforeEach
    void aCustomerWithOneItemInTheCart() {
        stack = Stack.connect(System.getenv("E2E_BASE_URL"));
        customer = stack.newCustomer();
        session = stack.login(customer);
        cart = stack.cartWith(customer, "SKU-MUG-01", 1, "12.50");
    }

    @AfterEach
    void cleanUp() {
        stack.deleteCustomerData(customer);
    }

    @Test
    void happyPathCreatesAConfirmedOrder() {
        String orderId = given().auth().oauth2(session).contentType("application/json")
                .body(Map.of("cartId", cart, "customerId", customer, "paymentMethod", "tok_visa", "clientToken", "t-1"))
                .when().post("/orders")
                .then().statusCode(201).body("status", equalTo("confirmed"))
                .extract().path("orderId");

        assertEquals("confirmed", stack.orderRow(orderId).get("status"));
        assertEquals("12.50", stack.orderRow(orderId).get("total_usd").toString());
        assertEquals(1, stack.eventsOn("order.created", orderId).size());
    }

    @Test
    void doubleSubmitIsOneOrder() {
        Map<String, Object> body = Map.of("cartId", cart, "customerId", customer, "paymentMethod", "tok_visa", "clientToken", "t-2");
        String first = given().auth().oauth2(session).contentType("application/json").body(body)
                .when().post("/orders").then().statusCode(201).extract().path("orderId");
        String second = given().auth().oauth2(session).contentType("application/json").body(body)
                .when().post("/orders").then().statusCode(409).extract().path("orderId");

        assertEquals(first, second);
        assertEquals(1, stack.ordersOf(customer).size());
        assertEquals(1, stack.paymentsFor(first).size());
    }

    @Test
    void declinedPaymentLeavesTheOrderPending() {
        given().auth().oauth2(session).contentType("application/json")
                .body(Map.of("cartId", cart, "customerId", customer, "paymentMethod", "tok_chargeDeclined", "clientToken", "t-3"))
                .when().post("/orders")
                .then().statusCode(402);

        assertEquals("pending_payment", stack.ordersOf(customer).get(0).get("status"));
        assertEquals(0, stack.eventsOn("order.created", null).size());
        assertEquals("open", stack.cartRow(cart).get("status"));
    }
}
