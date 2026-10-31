---
type: Subscription
title: On product updated
description: Consumes product.updated and upserts the search document.
status: Active
consumerGroup: search-indexer
maxAttempts: 10
concurrency: 3
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# On product updated

Consumes [CHAN-product-updated](../../channels/CHAN-product-updated/overview.md)
as consumer group `search-indexer`, for
[SVC-search-indexer](overview.md). Satisfies
[REQ-catalog-keyword-search](../../features/FEAT-catalog/overview.md#req-catalog-keyword-search).

# Consumes

* [product.updated](../../channels/CHAN-product-updated/overview.md)

# Validations

No validations.

# Handler

1. Read the current product from
   [products](../../datastores/DB-shop/TBL-products.md) by `productId`.
2. If `status = active`, upsert the document into
   [IDX-products](../../datastores/IDX-products/overview.md).
3. Otherwise (archived / deleted), remove the document from the index.

The handler always reads the **current** row rather than trusting the event body,
so a redelivered or out-of-order event converges to the true state.

# Flowchart

```mermaid
flowchart TD
    A[Deliver product.updated] --> B[Read current product by productId]
    B --> C{Product active?}
    C -- yes --> D[Upsert in IDX-products with updated_at version]
    C -- no --> E[Remove the document; already absent is fine]
    D --> F{Index call succeeded, or stale version ignored?}
    E --> F
    F -- yes --> ACK[ack]
    F -- no --> G{Attempts left?}
    G -- yes --> RETRY[retry]
    G -- no --> DL[dead letter]
```

# Sequence diagram

```mermaid
sequenceDiagram
    participant Channel as CHAN-product-updated
    participant Indexer as SVC-search-indexer
    participant Products as TBL-products
    participant Search as IDX-products
    participant DLQ as product.updated.dlq

    Channel->>Indexer: Deliver product.updated
    loop Each delivery attempt, maximum 10
        Indexer->>Products: Read current product by productId
        Products-->>Indexer: Current row and updated_at
        alt Product status is active
            Indexer->>Search: Upsert by productId with updated_at version
            alt Event version is stale or already applied
                Search-->>Indexer: Ignore older or duplicate version
            else Version is current
                Search-->>Indexer: Document upserted
            end
        else Product archived or deleted
            Indexer->>Search: Remove document by productId
            Search-->>Indexer: Removed or already absent
        end
        alt Index operation succeeds or is idempotently ignored
            Indexer-->>Channel: Acknowledge delivery
        else Index operation fails and attempts remain
            Search-->>Indexer: Retryable failure
            Indexer-->>Channel: Reject for exponential-backoff redelivery
        else Tenth attempt fails
            Search-->>Indexer: Retryable failure
            Indexer->>DLQ: Publish failed delivery
            Indexer-->>Channel: Acknowledge exhausted delivery
        end
    end
```

# Idempotency

| | |
|---|---|
| Key | `productId` + the row's `updated_at` |
| Enforced by | OpenSearch `version` / external versioning on upsert |

Upserting by document id is naturally idempotent; using the row's `updated_at` as
the external version means a **stale** event (an older update arriving after a
newer one) is dropped by the index rather than clobbering fresh data. This is why
the topic is ordered per product — belt and braces against re-ranking on a stale
title.

# Failure behavior

| | |
|---|---|
| Retry | exponential backoff, 2s base |
| Max attempts | 10 |
| Then | dead-letter, following the channel's [dead-letter policy](../../channels/CHAN-product-updated/overview.md#dead-letter) |

A dead-lettered product is simply stale in search until the next edit or a bulk
reindex — search being briefly wrong is tolerable, which is why this is `tier-2`,
not `tier-1`.

