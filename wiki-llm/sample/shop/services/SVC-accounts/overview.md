---
type: Service
title: Accounts Service
description: Customer registration, login, and profile; issues session tokens.
resource: https://github.com/acme/accounts-service
status: Active
serviceType: api
ownerTeam: accounts
language: typescript
framework: nestjs
runtime: node20
deployTarget: k8s
slaTier: tier-0
version: "5.2.1"
port: 8080
healthcheckPath: /healthz
generated: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
verified: { by: human:sample-author, at: 2026-07-14T10:00:00Z }
---

# Accounts Service

Owns customer identity: register, log in, read the profile. It is the only writer
of the credential columns on
[customers](../../datastores/DB-shop/TBL-customers.md), and the issuer of the
session tokens every other service trusts. A login writes a session into
[CACHE-session](../../datastores/CACHE-session/overview.md); that cache is the
authority on whether a token is live.

Passwords are stored only as Argon2id hashes — the plaintext is never persisted or
logged. It is `tier-0`: if login is down, nothing behind auth works.

# Reads

* [TBL-customers](../../datastores/DB-shop/TBL-customers.md) — credential and profile lookup.

# Writes

* [TBL-customers](../../datastores/DB-shop/TBL-customers.md) — registration and profile edits.

# Uses

* [CACHE-session](../../datastores/CACHE-session/overview.md) — rw — writes a session on login, reads it on `me`.
