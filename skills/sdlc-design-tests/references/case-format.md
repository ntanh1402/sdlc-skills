# TestCase format

A TestCase is one file in its suite's folder:
`wiki/<app>/tests/TS-<name>/TC-<name>.md`. Its key is its test case ID in
lower case followed by lower-case words from its title, for example
`TC-cpn-int-001-coupon-expired-rejected` for the ID `TC-CPN-INT-001`. Read
`.wiki-llm/schema/test-case.md` for the rules.

````markdown
---
type: TestCase
title: Expired coupon is rejected
description: Prove an expired coupon never reduces the order total.
risk: high
---

# Expired coupon is rejected

| Field | Value |
|---|---|
| Test case ID | TC-CPN-INT-001 |
| Feature | [FEAT-coupons](../../features/FEAT-coupons/overview.md) |
| Story | [STORY-coupons-apply-code](../../features/FEAT-coupons/STORY-coupons-apply-code.md), AC-2 |
| Priority | `high` |
| Testing type | `functional` |
| Category | `business-rule` |
| Polarity | `negative` |
| API endpoints | [`POST /carts/{id}/coupons`] |

# Covers

* [REQ-coupons-reject-expired](../../features/FEAT-coupons/overview.md#req-coupons-reject-expired)
* [EP-coupon-apply](../../services/SVC-checkout/EP-coupon-apply.md)

# Purpose

AC-2, boundary value analysis: an expired coupon is refused and leaves the
cart total unchanged.

# Preconditions

- A cart with one item at 20.00, created with `POST /carts`.
- Coupon `SPRING10` with an expiry date of yesterday, seeded in table
  `coupons`.
- `SVC-checkout` runs against the coupon store of the test environment; no
  stub.

# Test data

| No | Input | Value |
|---|---|---|
| 1 | Coupon | `code`: `SPRING10` (expired 1 day ago; boundary: a coupon expiring this second) |
| 2 | Cart | `id`: `c-1`, `total`: `20.00` |

# Steps

| Step | Action | Expected result | Validation |
|---|---|---|---|
| 1 | Apply the coupon `POST /carts/{id}/coupons`:<br>- Data 1 on the cart of data 2<br>- Request: see Step 1 | Status code: `422`<br>`code`: `coupon_expired` | **API response**: `POST /carts/c-1/coupons` |
| 2 | Read the cart `GET /carts/{id}`:<br>- Path: `id` = `c-1` | `total`: `20.00` (data 2)<br>`couponCode`: null | **API response**: `GET /carts/c-1` |
| 3 | Query table `coupon_redemptions`:<br>- Filter: `cart_id` = `c-1` | Rows found: 0 | **Database**: `coupon_redemptions` |
| 4 | Search the log of `SVC-checkout`:<br>- Filter: `correlationId` = the one of step 1<br>- Filter: level `WARN` | Lines found: 1<br>`message`: `coupon rejected`<br>`reason`: `expired` | **Log**: `SVC-checkout` |

### Step 1

Request:

```http
POST /carts/c-1/coupons
Authorization: Bearer <shopper token>
Content-Type: application/json

{ "code": "SPRING10" }
```

Expected response:

```http
422 Unprocessable Entity

{ "code": "coupon_expired" }
```

Other fields are ignored.

# Postconditions and cleanup

- The cart total is still `20.00` and no coupon is applied.
- Delete the test cart `DELETE /carts/{id}` with `id` = `c-1`.
````

A step that publishes to a channel shows the message the same way: the
channel name, then the key, the headers and the body, as the channel's
`# Payload` defines them. The expected result of a consumer is then what it
writes or publishes, shown the same way when it is a message.

- `# Covers` links Requirements by full path and anchor (a Requirement key is
  unique only inside its Feature), and the Design concepts and decisions the
  case proves.
- `# Test data` is a `No | Input | Value` table. `No` counts 1, 2, 3, … in
  order; a step refers to data by its number ("data 2").
- When several values of one partition give the same expected result (the
  boundary values inside a limit, for example), each is its own data row and
  the case runs its steps once per row. The step that uses them says so in
  its action: `- Data 1 to 3, one run each`. The `### Step <n>` request shows
  the first row's value, and the expected result holds for every row. When
  the result differs from row to row only in a value the row sets, such as
  the name of the field an error points at, the row's note gives that value
  (`(expect field: email)`) and the expected result says
  `` `field`: the one of the data row ``.
- A value that sets or matches a field is written `<field>: <value>`, and
  the fields of one input are separated by commas on one line, so the table
  stays short. The field is the name the request, message, table or screen
  uses, the same name the steps and the `### Step <n>` request show. A value
  with no field (a URL, a waiting time) is written as it is. A note, such as
  where the value comes from or the boundary it tests, follows in brackets.
- `# Postconditions and cleanup` is a list, one item per line: first the
  state the case leaves, then each clean-up action. A clean-up action starts
  with its verb and names where it acts and what it finds, the same way a
  step's action does, for example "Delete the rows of table
  `coupon_redemptions` with `cart_id` = `c-1`." Something
  that is left on purpose is its own item, with the reason.
- Every step has an observable expected result and names what is inspected.
  "Works" is never a validation.
- An action says where the tester points and how to find what the step
  checks. Its first line is a short verb phrase with the endpoint, channel,
  table, log, screen or system it acts on, ending with `:`, for example
  "Apply the coupon `POST /carts/{id}/coupons`:". Each detail follows on its
  own line starting with `- `, joined with `<br>` inside the table cell:
  - a step that sends something names the data it uses, then
    `- Request: see Step <n>`;
  - a step that reads something names how to find it, one line each:
    `- Filter: <field> = <value>` (the value or the data number it comes
    from), `- Sort: <field> <order>` when the newest or oldest is meant,
    `- Path:` or `- Query:` for a read through an API;
  - a step whose outcome appears later than its cause (a message, a job, a
    callback, a cache or replica update) says how long to wait and how
    often to check: `- Wait: up to <n> s, checking every <m> s`. Expected
    absence is checked only after the full wait.
  A tester who follows the action finds exactly the rows, lines or messages
  the expected result describes.
- An expected result says what must be found, one check per line as
  `<field or item>: <value>`, joined with `<br>` inside the table cell, with
  no `- ` in front. Start with the status code of a response or the count of
  what a read finds (`Rows found: 1`, `Lines found: 1`, `Messages found: 0`),
  then the fields in the order the tester reads them. Do not repeat a field
  the action already filters on.
- A validation starts with the place it is read from, in bold, then what
  exactly is read there:
  - **API response**: the method and path called;
  - **Database**: the table and the key of the row;
  - **Message**: the channel, topic or queue, and the message key;
  - **Log**: the service and the field that finds the line, such as the
    correlation id;
  - **Cache**: the key;
  - **External system**: the system, and the screen, API or report read;
  - **Screen**: the route and the element;
  - **File**: the path and the record;
  - **Metric**: the metric name and its labels;
  - **Alert**: the alert name and where it is raised.
  A step read in two places has one line per place, joined with `<br>`.
- A step that calls an API or publishes to a channel says "Request: see Step
  <n>" in its Action cell, and has a `### Step <n>` block under the table
  with its `Request` (method and path or channel, headers, body, with the
  values of the test data) and its `Expected response` (the status and only
  the fields the step checks, then "Other fields are ignored."). Take the
  fields from the Endpoint's `# Request` and `# Response` or the channel's
  `# Payload`; never invent one. A response with no body shows the status
  only.
- A negative case checks what "Polarity" in `classification.md` says: no
  business effect, and each record the design says a rejection writes,
  checked as written with its values. A negative case with a fallback that
  completes the operation checks the fallback's effect instead, as that
  section says.
- `# Preconditions` is a list, one item per line: each state the case needs
  and how it is reached (the endpoint, the seed of a table, the job or the
  screen that creates it), and, when the suite's seam uses one, the stub or
  simulator that stands in for an external system with the answer it is set
  to give. A clock or a setting the case needs is set here, with its value.
- An information table sits right under the `# <title>` heading, with the
  rows `Test case ID`, `Feature`, `Story`, `Priority`, `Testing type`,
  `Category`, `Polarity` and `API endpoints`, in that order, every row
  filled, in both modes:
  - `Test case ID` holds the ID in capitals;
  - `Feature` links the `overview.md` of the Feature or ChangeRequest the
    case was designed for;
  - `Story` links the story file and names each `AC-<n>` the case serves.
    In feature mode it names the story and `AC-<n>` whose criterion the case
    proves, or `None` when no story's criterion is about it;
  - `Priority`, `Testing type`, `Category` and `Polarity` hold exactly one
    value each, written as the code, for example `field-validation`; the
    category belongs to the testing type;
  - `API endpoints` names each entry point of the system under test that
    the steps call or trigger, as its method and path linked to its
    Endpoint (or its channel, consumer, scheduled job, webhook, screen
    route or file intake), one per line.
- A case has no `tags` field: the information table holds what tags would.
- `# Covers` never links a story, which is in the information table.
- `# Purpose` is one or two plain sentences that name the acceptance
  criterion number and the technique used, never the story or Feature key.
- A case never records a test result; the wiki holds none.
- Do not write `generated` or `verified`; `draft finish` does. It also
  writes the suite's `checklist.csv` from the cases' titles, descriptions,
  `# Covers` and `# Purpose`, so keep the `description` and `# Purpose`
  short and plain: they are the checklist's columns.
