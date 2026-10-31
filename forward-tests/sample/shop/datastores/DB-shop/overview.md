---
type: Database
title: Shop Database
description: PostgreSQL datastore for the shop platform.
status: Active
engine: PostgreSQL
version: "16"
schemaName: shop
replication: true
backupPolicy: PITR, 7-day window; nightly base backup to S3
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Shop Database

PostgreSQL datastore for the [Shop Platform](../../overview.md). It sits in
`datastores/` beside the caches, blob store, and search index.

One physical database, one `shop` schema, shared by every API service — this is a
modular monolith at the data tier, not a database-per-service split. A streaming
replica serves read-heavy catalog queries; point-in-time recovery covers a
seven-day window.

Its tables are the files in this folder — that is the ownership record. Service
`# Reads` and `# Writes` sections are the access source of truth; each table's
`# Used by` section is written from them by the tool.
