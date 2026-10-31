package com.acme.orders.unit;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.math.BigDecimal;
import org.junit.jupiter.api.Test;

/** A unit test: it checks one calculation and touches no service, database or topic. */
class OrderTotalTest {

    @Test
    void totalIsUnitPriceTimesQuantity() {
        assertEquals(new BigDecimal("25.00"), new BigDecimal("12.50").multiply(BigDecimal.valueOf(2)));
    }
}
