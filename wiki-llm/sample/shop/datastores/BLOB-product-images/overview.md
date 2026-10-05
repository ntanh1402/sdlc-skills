---
type: BlobStore
title: Product Images
description: S3 bucket holding product image assets, served via CDN.
status: Active
provider: s3
bucket: acme-shop-product-images
pathPattern: products/{product_id}/{size}.webp
region: us-east-1
publicAccess: false
encryption: true
lifecyclePolicy: noncurrent versions expire after 30 days
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Product Images

S3 bucket for product imagery. Objects are **not** public: the bucket is fronted
by a CDN, and [SVC-catalog](../../services/SVC-catalog/overview.md) hands out
short-lived signed URLs rather than exposing the bucket directly. The
`image_key` column on [products](../DB-shop/TBL-products.md) is the
object key; the bytes live only here.

Each product has one original upload plus rendered sizes (`thumb`, `card`,
`full`), all WebP. Server-side encryption is on; superseded versions age out after
30 days so a re-upload does not accumulate storage forever.

# Content types

| Path | Content type | Notes |
|---|---|---|
| `products/{id}/original.webp` | `image/webp` | the uploaded master |
| `products/{id}/thumb.webp` | `image/webp` | 128px, listing grids |
| `products/{id}/card.webp` | `image/webp` | 512px, product cards |
| `products/{id}/full.webp` | `image/webp` | 1600px, the detail page |

# Used by

* [Catalog Service](../../services/SVC-catalog/overview.md) — read
