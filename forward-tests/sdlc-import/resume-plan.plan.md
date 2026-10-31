# Run plan: sdlc-import, SVC-orders
Intent approved 2026-10-03

## Answers
1. The Import source is the code in `../orders-service`; the kind is code; the run creates, because the wiki has no Service for this repository.
2. The Application is `shop`. The owner team is `checkout`. The service is a backend service, built and running today.
3. The repository URL is `https://github.com/acme/orders-service`. Record the commit that `HEAD` is at when the files are written.
4. The key is `SVC-orders`; the draft is `import-SVC-orders`.
5. Nothing else in the wiki changes. The payments service is imported in a run of its own.

## Files
### The Service page
- [ ] services/SVC-orders/overview.md (add)
- [ ] services/SVC-orders/log.md (add)
### Endpoints
- [ ] services/SVC-orders/EP-create-order.md (add)
- [ ] services/SVC-orders/EP-get-order.md (add)
- [ ] services/SVC-orders/EP-list-orders.md (add)
- [ ] services/SVC-orders/EP-cancel-order.md (add)
### Tables of the database
- [ ] datastores/DB-orders/overview.md (add)
- [ ] datastores/DB-orders/TBL-orders.md (add)
- [ ] datastores/DB-orders/log.md (add)
### Channels
- [ ] channels/CHAN-order-created/overview.md (add, with payload.example.json)
- [ ] channels/CHAN-order-created/log.md (add)
### Externals
- [ ] externals/EXT-shipwell/overview.md (add)
- [ ] externals/EXT-shipwell/OP-create-shipment.md (add)
- [ ] externals/EXT-shipwell/log.md (add)

## For other skills
- The payments service is called and is not in the wiki: sdlc-import on its code
