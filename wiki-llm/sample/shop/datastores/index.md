# Datastores

* [Product Images](BLOB-product-images/overview.md) - S3 bucket holding product image assets, served via CDN.
* [Catalog Cache](CACHE-catalog/overview.md) - Redis read-through cache for product and category reads.
* [Session Cache](CACHE-session/overview.md) - Redis store for login sessions and the auth token lookup.
* [Shop Database](DB-shop/overview.md) - PostgreSQL datastore for the shop platform.
* [Product Search Index](IDX-products/overview.md) - OpenSearch index backing product search and faceting.
