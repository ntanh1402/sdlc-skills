CREATE TABLE orders (
    order_id     uuid        PRIMARY KEY,
    customer_id  uuid        NOT NULL REFERENCES customers (customer_id),
    cart_id      uuid        NOT NULL REFERENCES carts (cart_id),
    total_usd    numeric     NOT NULL,
    currency     text        NOT NULL DEFAULT 'USD',
    status       text        NOT NULL CHECK (status IN ('pending_payment', 'confirmed', 'cancelled')),
    client_token text        NOT NULL,
    created_at   timestamptz NOT NULL DEFAULT now()
) PARTITION BY RANGE (created_at);

CREATE UNIQUE INDEX uq_orders_client_token ON orders (customer_id, client_token);
CREATE INDEX ix_orders_customer ON orders (customer_id, created_at);
