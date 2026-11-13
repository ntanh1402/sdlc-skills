# TestCase format

This skill writes TestCases in the `GENERAL/` group of the suite:
`wiki/<app>/tests/TS-<name>/GENERAL/TC-<id>-<name>.md`. Its id is the highest
id in the suite + 1, across all its groups; its name is lower-case words from
its title, for example `TC-5-coupon-applied-and-paid`. Read
`.wiki-llm/schema/test-case.md` for the rules.

````markdown
---
type: TestCase
title: Coupon applied and paid
description: Prove a shopper applies a coupon and pays the reduced total.
risk: high
testType: e2e
testCategory: functional
---

# Coupon applied and paid

# Covers

* [REQ-coupons-redeem](../../../features/FEAT-coupons/overview.md#req-coupons-redeem)
* [EP-coupon-apply](../../../services/SVC-checkout/EP-coupon-apply.md)
* [EP-orders-create](../../../services/SVC-orders/EP-orders-create.md)
* [TBL-coupon-redemptions](../../../datastores/DB-checkout/TBL-coupon-redemptions.md)

# Purpose

Prove the coupon flow from applying a coupon to paying the reduced total.

# Preconditions

The checkout and orders services run against empty `orders` and
`coupon_redemptions` tables; Stripe is in test mode; the shopper is signed in.

Data that must exist:

* cart `c-1` with one item at 20.00, owned by the shopper
* coupon `SPRING10`, 10% off, valid until next month

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Call API `POST /carts/c-1/coupons` with coupon `SPRING10` | Response POST /carts/c-1/coupons:<br>- status: 200<br>- total: 18.00 | Read the response; check **status** and **total** |
| 2 | Call API `POST /orders` with cart `c-1` and payment method `tok_visa` | Response POST /orders:<br>- status: 201<br>Table orders:<br>- Rows found for cart `c-1`: 1<br>- total_usd: 18.00 | Read the response and query table `orders` by cart; check **status**, **rows found** and **total_usd** |
| 3 | Query table `coupon_redemptions` for cart `c-1` | Table coupon_redemptions:<br>- Rows found: 1<br>- code: SPRING10 | Count the rows of cart `c-1`; check **rows found** and **code** |

### Step 2

Request:

```http
POST /orders
Authorization: Bearer <shopper token>
Content-Type: application/json

{ "cartId": "c-1", "paymentMethod": "tok_visa" }
```

Expected response:

```http
201 Created

{ "status": "confirmed" }
```

Other fields are ignored.

# Postconditions and cleanup

Delete the order of cart `c-1`, cart `c-1` and coupon `SPRING10`.
````

A step that publishes to a channel says so with the topic's real name
("Publish message to topic `coupons.applied`") and shows the message the same
way: the channel name, then the key, the headers and the body, as the
channel's `# Payload` defines them. The expected result of a consumer is then
what it writes or publishes, shown the same way when it is a message.

- `# Covers` links Requirements by full path and anchor (a Requirement key is
  unique only inside its Feature), and the Design concepts and decisions the
  case proves. A `GENERAL/` case never links a user story: a case that
  proves a story's acceptance criteria belongs in that story's group.
- `testType` is how the case runs (`integration` or `e2e`); `testCategory`
  is what it checks: `functional`, `field-validation`, `negative`,
  `error-handling`, `data-validation`, `security-validation` or
  `integration` (`test-case.md` defines each).
- `# Preconditions` says the state before the test and lists the data that
  must exist, with concrete values, including boundary values.
- Each Action starts with what to do and its target ("Call API", "Publish
  message to topic", "Query table", "Open page") and copies every value it
  needs. It never says "data 2", "see Step 1" or "the cart above".
- `# Preconditions`, `# Steps` and `# Postconditions and cleanup` use the
  real names from the design files (`tableName`, `channelName`, `method` and
  `path`, `keyPattern`, `bucket`, `indexName`), never a wiki key such as
  `TBL-coupon-redemptions`; the wiki keys belong in `# Covers`.
- Every step has an observable expected result. The Expected result is one
  checkpoint per table, topic, cache entry, page or group of API fields: its
  kind and real name and a colon, then one `- <field>: <value>` line per
  point, joined with `<br>` because a table cell holds one line:
  `Table orders:<br>- Rows found: 2<br>- status: DECLINED<br>Table order_events:<br>- Rows found: 1 per order`.
  Other headers: `Response POST /orders:`, `Topic order.created:`,
  `Cache cart:{id}:`, `Page Order confirmation:`.
- The Validation says how the result is checked and names each field it
  checks in bold: "Query table `orders` by order id; check **status** and
  **rows found**". "Works" is never a validation; `validate` reports a
  Validation with no bold field.
- A step that calls an API or publishes to a channel has a `### Step <n>`
  block under the table with its `Request` (method and path or channel,
  headers, body, with the concrete values) and its `Expected response` (the
  status and only the fields the step checks, then "Other fields are
  ignored."). Take the fields from the Endpoint's `# Request` and
  `# Response` or the channel's `# Payload`; never invent one. A response
  with no body shows the status only.
- Include negative checks, such as no row, no message or no external call,
  when they matter.
- A case never records a test result; the wiki holds none.
- Do not write `generated` or `verified`; `draft finish` does. It also
  writes the suite's `checklist.csv` from the cases' ids, titles,
  descriptions, `# Covers` and `# Purpose`, so keep the `description` and
  `# Purpose` short and plain: they are the checklist's columns, with the
  group and the category.
