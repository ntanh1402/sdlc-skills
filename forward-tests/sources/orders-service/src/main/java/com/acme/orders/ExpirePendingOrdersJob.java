package com.acme.orders;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/** Every night at 03:00 UTC, cancels orders that waited for payment for more than 24 hours. */
@Component
public class ExpirePendingOrdersJob {

    private final JdbcTemplate db;

    public ExpirePendingOrdersJob(JdbcTemplate db) {
        this.db = db;
    }

    @Scheduled(cron = "0 0 3 * * *", zone = "UTC")
    public void run() {
        db.update("UPDATE orders SET status = 'cancelled' "
                + "WHERE status = 'pending_payment' AND created_at < now() - interval '24 hours'");
    }
}
