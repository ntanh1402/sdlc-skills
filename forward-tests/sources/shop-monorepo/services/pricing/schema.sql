CREATE TABLE prices (
    sku        text        NOT NULL,
    price_usd  numeric     NOT NULL CHECK (price_usd >= 0),
    valid_from timestamptz NOT NULL,
    PRIMARY KEY (sku, valid_from)
);
