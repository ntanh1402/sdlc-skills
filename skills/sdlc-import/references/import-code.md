# Importing code

One run reads one service's or one frontend's folder and writes what that code
is today. Read these schema pages in `.wiki-llm/schema/` first: `service.md`
or `frontend-web.md` / `frontend-mobile.md`, `endpoint.md`, `subscription.md`,
`message-channel.md`, `datastore-database.md`, `datastore-table.md`, the page
of any other store the code uses, `external-service.md` and
`external-operation.md`. They are the only definition of each type.

Read only. Never run the code, its build or its tests.

## 1. What to read, in this order

1. **Machine-readable contracts**, when the folder has them: an OpenAPI or
   AsyncAPI file, protocol definitions (`.proto`, GraphQL schema), database
   migrations or schema files. They are the most reliable statement of a
   contract.
2. **Routes and handlers**: what each endpoint accepts, returns and does,
   including its status codes and validation.
3. **Message publishers and consumers**: the channel names, the payloads, the
   consumer groups, retries and dead letters.
4. **Data access**: which tables the code reads and which it writes; caches,
   blob stores and search indexes.
5. **Clients for other services and for vendors**: which endpoints and
   operations the code calls, with timeouts and fallbacks.
6. **Configuration and build files**, for the language, framework, runtime,
   port and health check. Never copy a value that is a secret, a credential or
   personal data; name the setting only.

When a contract file and the handler code disagree, the handler code is what
runs: write what the code does and list the difference under "Disagreements".

## 2. What to write

| Found in the code | File |
|---|---|
| The service | `services/SVC-<name>/overview.md` and `log.md`, `status: Active` |
| A web or mobile client | `frontends/WEB-<name>/` or `frontends/MB-<name>/`, with `overview.md` and `log.md` |
| Each endpoint the service serves | `services/SVC-<name>/EP-<name>.md` |
| Each message consumer | `services/SVC-<name>/SUB-<name>.md` |
| A channel the wiki lacks | `channels/CHAN-<name>/` with `overview.md`, `log.md` and `payload.example.json` |
| A database or table the wiki lacks | `datastores/DB-<name>/` and `TBL-<name>.md` inside it |
| A cache, blob store or search index the wiki lacks | `datastores/CACHE-<name>/`, `BLOB-<name>/`, `IDX-<name>/` |
| A vendor the wiki lacks, and each call to it | `externals/EXT-<name>/` and `OP-<name>.md` inside it |

Rules:

- **Keys** come from the code's own names: the service's name, the handler or
  route name, the table name.
- **Link, do not rewrite.** A Table, Channel, store or external that is
  already in the wiki is linked from the Service (`# Reads`, `# Writes`,
  `# Publishes`, `# Uses`, `# Depends on`). If the code disagrees with that
  file, it is a difference: handle it as `compare.md` says.
- **Calls to another service** go under `# Calls` only when that Endpoint is in
  the wiki. Otherwise list the call under "Could not determine" with the
  other service's name: "calls the payments service's capture endpoint; import
  its code".
- **Fields the code does not state** (`serviceType`, `ownerTeam`, a table's
  `pii`) are proposed and confirmed by the person.
- **`payload.example.json`** is built from the payload's fields with made-up
  values of the right type. Never copy a real message.
- **A frontend's `# Architecture`** is one Mermaid `flowchart` of its main
  modules and the services it calls, drawn from the code.
- **Not modelled.** A scheduled job, a store that is not relational, or
  anything else the schema has no type for is described in the Service page's
  prose and listed under "Not modelled".
- Every file is `status: Active`. A file that describes something planned is
  not this skill's to write.

## 3. What to ask

- The owner team, the service type, and whether each table holds personal data.
- For every required section the code cannot fill (a Subscription's
  `# Idempotency`, an external's `# Fallback`): ask once at the gate; with no
  answer write `Not determined by the import.`
- When a route exists in the code but is switched off or unreachable: whether
  it is live. Import only what runs.

## 4. Before the Design gate

Check by reading:

- every endpoint, consumer, table and vendor call you found is in a file or in
  one of the three lists;
- every link resolves to a file that is in the wiki or in this draft;
- no file holds a secret, a credential or a real person's data.
