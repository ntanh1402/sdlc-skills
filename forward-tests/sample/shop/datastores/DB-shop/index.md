# Shop Database

* [Overview](overview.md) - PostgreSQL datastore for the shop platform.

# Tables

* [cart_items](TBL-cart-items.md) - One row per (cart, product) line — quantity and the price captured at add time.
* [carts](TBL-carts.md) - One open cart per customer; the checkout reads it to build the order.
* [categories](TBL-categories.md) - The product category tree — one row per category, self-referencing.
* [customers](TBL-customers.md) - One row per customer, with contact details and per-channel opt-outs.
* [notifications](TBL-notifications.md) - One row per (order, channel) send attempt — the idempotency and audit record.
* [orders](TBL-orders.md) - One row per customer order.
* [payments](TBL-payments.md) - One row per payment attempt against an order — the Stripe authorization record.
* [products](TBL-products.md) - One row per sellable product, the catalog's source of truth.

# History

* [Change log](log.md) - History of Shop Database.
