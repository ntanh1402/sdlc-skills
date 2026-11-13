"""A minimal valid bundle used by every rule test.

`make_bundle(root)` writes it. Tests then break exactly one thing with
`edit`, `write`, or `remove` and assert that one rule reports it.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from wikilib import sync

G = "generated: { by: human:alice, at: 2026-09-01T09:00:00Z }"
V = "verified: { by: human:bob, at: 2026-09-02T09:00:00Z }"
B = "basedOn: { version: 1, at: 2026-08-15 }"
CB = "basedOn: { version: 1, at: 2026-08-20 }"
FV = "version: 1\nversionDate: 2026-08-15\ndesignBasedOn: { version: 1, at: 2026-08-15 }"
CV = "version: 1\nversionDate: 2026-08-20\ndesignBasedOn: { version: 1, at: 2026-08-20 }"


def page(frontmatter: str, body: str) -> str:
    return f"---\n{frontmatter.strip()}\n---\n\n{body.strip()}\n"


LOG = "# Change log\n\n## 2026-09-01\n\n* **Creation**: Created.\n"
INDEX = "# Index\n"

FILES: dict[str, str] = {
    "index.md": '---\nokf_version: "0.2"\nschema_version: "2"\n---\n\n# Applications\n',
    # ----------------------------------------------------------------- application
    "pay/overview.md": page(
        f"type: Application\ntitle: Pay\ndescription: Payment platform.\nstatus: Active\nownerTeam: payments\n{G}",
        "# Pay\n\nTakes payments.\n\n# Architecture\n\n```mermaid\nflowchart LR\n  Web --> Svc\n```",
    ),
    "pay/conventions.md": page(
        f"type: Convention\ntitle: Conventions\ndescription: How we build.\n{G}",
        "# Conventions\n\n# Definition of done\n\nTests pass.",
    ),
    "pay/glossary.md": page(
        f"type: Glossary\ntitle: Glossary\ndescription: Terms and roles.\n{G}",
        "# Glossary\n\n# Terms\n\n| Term | Definition |\n|---|---|\n| Capture | Taking authorized money. |\n\n"
        "# Roles\n\n| Role | Description |\n|---|---|\n| shopper | A paying customer. |",
    ),
    # ------------------------------------------------------------------- decisions
    "pay/decisions/ADR-001.md": page(
        f"type: ArchitectureDecision\ntitle: Charge synchronously\ndescription: Charge during the request.\n"
        f"status: Superseded\nownerTeam: payments\ndecisionDate: 2026-08-01\n{G}",
        "# Charge synchronously\n\n# Context\n\nText.\n\n# Decision\n\nText.\n\n# Alternatives\n\nText.\n\n"
        "# Consequences\n\nText.\n\n# Affected concepts\n\n* [SVC-pay](../services/SVC-pay/overview.md)",
    ),
    "pay/decisions/ADR-002.md": page(
        f"type: ArchitectureDecision\ntitle: Charge through the bank operation\ndescription: Use one bank call.\n"
        f"status: Accepted\nownerTeam: payments\ndecisionDate: 2026-08-20\n{G}",
        "# Charge through the bank operation\n\n# Context\n\nText.\n\n# Decision\n\nText.\n\n# Alternatives\n\nText.\n\n"
        "# Consequences\n\nText.\n\n# Affected concepts\n\n* [SVC-pay](../services/SVC-pay/overview.md)\n"
        "* [FEAT-pay](../features/FEAT-pay/overview.md)\n\n# Supersedes\n\n* [ADR-001](ADR-001.md)",
    ),
    # --------------------------------------------------------------------- feature
    "pay/features/FEAT-pay/overview.md": page(
        f"type: Feature\ntitle: Pay\ndescription: Pay for an order.\nstatus: InDev\nownerTeam: payments\n{G}\n{FV}",
        "# Pay\n\n# Requirements\n\n### REQ-pay-1\n\n**Must** — A shopper pays for an order. Functional. Verified by test.\n\n"
        "# Architecture\n\n## Context and constraints\n\nText.\n\n## High-level architecture\n\n"
        "```mermaid\nflowchart LR\n  Web --> Svc\n```\n\n"
        "## Services\n\n* [SVC-pay](../../services/SVC-pay/overview.md) — takes the payment.\n\n"
        "## Frontends\n\n* [WEB-shop](../../frontends/WEB-shop/overview.md)\n* [MB-shop](../../frontends/MB-shop/overview.md)\n\n"
        "## Runtime sequences\n\n```mermaid\nsequenceDiagram\n  Web->>Svc: pay\n```\n\n"
        "## Decisions\n\n* [ADR-002](../../decisions/ADR-002.md)\n\n"
        "## Traceability\n\n| Requirement | Target concepts |\n|---|---|\n"
        "| [REQ-pay-1](#req-pay-1) | [EP-pay-create](../../services/SVC-pay/EP-pay-create.md), "
        "[EP-pay-refund](../../services/SVC-pay/EP-pay-refund.md) |\n\n"
        "# References\n\n* [REF-pay-prd](../../references/REF-pay-prd/overview.md) — the approved PRD.",
    ),
    "pay/features/FEAT-pay/log.md": LOG,
    "pay/features/FEAT-pay/TASK-pay-001.md": page(
        f"type: Task\ntitle: Create the payments table\ndescription: Add the table.\nstatus: Done\n{G}\n{B}",
        "# Create the payments table\n\n# Acceptance\n\nTable exists. Satisfies [REQ-pay-1](overview.md#req-pay-1).\n\n"
        "# Stories\n\n* [STORY-pay-checkout](STORY-pay-checkout.md)\n\n"
        "# Planned scope\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md) — new — the table.",
    ),
    "pay/features/FEAT-pay/STORY-pay-checkout.md": page(
        f"type: UserStory\ntitle: Pay at checkout\ndescription: A shopper pays for an order.\npriority: P1\n{G}\n{B}",
        "# Pay at checkout\n\nAs a **shopper**, I want to pay for my order, so that it is placed.\n\n"
        "# Acceptance criteria\n\n1. A shopper who pays for a cart gets the order placed.\n"
        "   ([REQ-pay-1](overview.md#req-pay-1))\n\n"
        "# Requirements\n\n* [REQ-pay-1](overview.md#req-pay-1)",
    ),
    "pay/features/FEAT-pay/TASK-pay-002.md": page(
        f"type: Task\ntitle: Build the refund endpoint\ndescription: Add refunds.\nstatus: Todo\n{G}\n{B}",
        "# Build the refund endpoint\n\n# Acceptance\n\nRefund works.\n\n"
        "# Planned scope\n\n* [EP-pay-refund](../../services/SVC-pay/EP-pay-refund.md) — new — the endpoint.\n\n"
        "# Blocked by\n\n* [TASK-pay-001](TASK-pay-001.md)\n\n"
        "# References\n\n* [REF-pay-prd](../../references/REF-pay-prd/overview.md) — the refund rules.",
    ),
    # -------------------------------------------------------------- change request
    "pay/change-requests/CR-1/overview.md": page(
        f"type: ChangeRequest\ntitle: Accept coupons\ndescription: Add a coupon code.\nstatus: Approved\n"
        f"changeType: feature\nriskLevel: low\n{G}\n{CV}",
        "# Accept coupons\n\n# Changes\n\n* [FEAT-pay](../../features/FEAT-pay/overview.md)\n\n# Reason\n\nMarketing.\n\n"
        "# Requirements\n\n### REQ-pay-2\n\n**Should** — A shopper applies one coupon. Functional. Verified by test.\n\n"
        "# Delta\n\n## Target delta\n\n* [EP-pay-create](../../services/SVC-pay/EP-pay-create.md) — modified — adds `couponCode`.\n\n"
        "## Runtime sequences\n\n```mermaid\nsequenceDiagram\n  Web->>Svc: pay with coupon\n```\n\n"
        "## Decisions\n\nNone.\n\n## Traceability\n\n| Requirement | Target concepts |\n|---|---|\n"
        "| [REQ-pay-2](#req-pay-2) | [EP-pay-create](../../services/SVC-pay/EP-pay-create.md) |",
    ),
    "pay/change-requests/CR-1/log.md": LOG,
    "pay/change-requests/CR-1/STORY-pay-coupon.md": page(
        f"type: UserStory\ntitle: Pay with a coupon\ndescription: A shopper applies a coupon.\n{G}\n{CB}",
        "# Pay with a coupon\n\nAs a shopper, I want to apply a coupon, so that I pay less.\n\n"
        "# Acceptance criteria\n\n1. Paying with a valid coupon lowers the price. "
        "([REQ-pay-2](overview.md#req-pay-2))\n\n"
        "# Requirements\n\n* [REQ-pay-2](overview.md#req-pay-2)\n\n"
        "# Affects\n\n* [STORY-pay-checkout](../../features/FEAT-pay/STORY-pay-checkout.md) — paying now takes a coupon.",
    ),
    "pay/change-requests/CR-1/TASK-pay-003.md": page(
        f"type: Task\ntitle: Add the coupon field\ndescription: Accept a coupon.\nstatus: Todo\n{G}\n{CB}",
        "# Add the coupon field\n\n# Acceptance\n\nCoupon accepted.\n\n"
        "# Stories\n\n* [STORY-pay-coupon](STORY-pay-coupon.md)\n\n"
        "# Planned scope\n\n* [EP-pay-create](../../services/SVC-pay/EP-pay-create.md) — modified — the new field.",
    ),
    # -------------------------------------------------------------------- service
    "pay/services/SVC-pay/overview.md": page(
        f"type: Service\ntitle: Pay Service\ndescription: Takes payments.\nstatus: Active\nserviceType: api\n"
        f"ownerTeam: payments\nresource: https://example.com/acme/pay\n{G}",
        "# Pay Service\n\nTakes payments.\n\n"
        "# Publishes\n\n* [CHAN-pay-events](../../channels/CHAN-pay-events/overview.md) — after a charge.\n\n"
        "# Calls\n\n* [OP-charge](../../externals/EXT-bank/OP-charge.md) — charges the card.\n\n"
        "# Reads\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md)\n\n"
        "# Writes\n\n* [TBL-payments](../../datastores/DB-main/TBL-payments.md)\n\n"
        "# Uses\n\n* [CACHE-pay](../../datastores/CACHE-pay/overview.md) — rw — idempotency keys.\n"
        "* [BLOB-receipts](../../datastores/BLOB-receipts/overview.md) — write — receipts.\n"
        "* [IDX-payments](../../datastores/IDX-payments/overview.md) — read — search.\n\n"
        "# Depends on\n\n* [EXT-bank](../../externals/EXT-bank/overview.md) — critical — the payment rail.",
    ),
    "pay/services/SVC-pay/log.md": LOG,
    "pay/services/SVC-pay/EP-pay-create.md": page(
        f"type: Endpoint\ntitle: Create payment\ndescription: POST /payments.\nstatus: Modifying\nmethod: POST\n"
        f"path: /payments\nprotocol: http\n{G}",
        "# Create payment\n\n# Request\n\nNo request fields.\n\n# Response\n\nNo body.\n\n## Status codes\n\n| Code | When |\n|---|---|\n| 201 | Created. |\n\n# Validations\n\nNo validations.\n\n# Behavior\n\n1. Charge.\n\n# Flowchart\n\n```mermaid\nflowchart TD\n    A[Request] --> B[201 Created]\n```\n\n# Sequence diagram\n\n```mermaid\nsequenceDiagram\n    Client->>Service: Call\n    Service-->>Client: 201\n```\n\n"
        "# Pending changes\n\n* [CR-1](../../change-requests/CR-1/overview.md) — modified — adds `couponCode`.",
    ),
    "pay/services/SVC-pay/EP-pay-refund.md": page(
        f"type: Endpoint\ntitle: Refund payment\ndescription: POST /refunds.\nstatus: Planned\nmethod: POST\n"
        f"path: /refunds\nprotocol: http\n{G}",
        "# Refund payment\n\n# Request\n\nNo request fields.\n\n# Response\n\nNo body.\n\n## Status codes\n\n| Code | When |\n|---|---|\n| 201 | Created. |\n\n# Validations\n\nNo validations.\n\n# Behavior\n\n1. Refund.\n\n# Flowchart\n\n```mermaid\nflowchart TD\n    A[Request] --> B[201 Created]\n```\n\n# Sequence diagram\n\n```mermaid\nsequenceDiagram\n    Client->>Service: Call\n    Service-->>Client: 201\n```\n\n"
        "# Pending changes\n\n* [FEAT-pay](../../features/FEAT-pay/overview.md) — new — not built yet.",
    ),
    "pay/services/SVC-pay/SUB-pay-events.md": page(
        f"type: Subscription\ntitle: On payment event\ndescription: Sends a receipt.\nstatus: Active\n"
        f"consumerGroup: receipts\nmaxAttempts: 5\n{G}",
        "# On payment event\n\n# Consumes\n\n* [CHAN-pay-events](../../channels/CHAN-pay-events/overview.md)\n\n"
        "# Validations\n\nNo validations.\n\n# Handler\n\n1. Send.\n\n# Flowchart\n\n```mermaid\nflowchart TD\n    A[Message] --> B[ack]\n```\n\n# Sequence diagram\n\n```mermaid\nsequenceDiagram\n    Channel->>Service: Deliver\n    Service-->>Channel: ack\n```\n\n# Idempotency\n\nBy payment id.\n\n# Failure behavior\n\nRetry five times.",
    ),
    # -------------------------------------------------------------------- channel
    "pay/channels/CHAN-pay-events/overview.md": page(
        f"type: MessageChannel\ntitle: pay.events\ndescription: Payment events.\nstatus: Active\n"
        f"channelName: pay.events\nkind: kafka\nchannelType: topic\n{G}",
        "# Overview\n\nPayment events.\n\n## Dead letter\n\n| | |\n|---|---|\n| DLQ channel | `pay.events.dlq` |\n\n"
        "# Payload\n\n## Key\n\n| | |\n|---|---|\n| Key | `paymentId` |\n\n"
        "## Header\n\n| Name | Required | Type | Description |\n|---|---|---|---|\n| `event-type` | yes | string | Kind. |\n"
        "| `retry-count` | no | integer | Retries. |\n\n"
        "## Body\n\n| Field | Required | Type | Description |\n|---|---|---|---|\n| `paymentId` | yes | string | Id. |\n\n"
        "# Payload example\n\n[payload.example.json](payload.example.json)",
    ),
    "pay/channels/CHAN-pay-events/log.md": LOG,
    "pay/channels/CHAN-pay-events/payload.example.json": (
        '{\n  "key": "p1",\n  "headers": {"event-type": "pay.done"},\n  "body": {"paymentId": "p1"}\n}\n'
    ),
    # ----------------------------------------------------------------- datastores
    "pay/datastores/DB-main/overview.md": page(
        f"type: Database\ntitle: Main Database\ndescription: Relational store.\nstatus: Active\nengine: PostgreSQL\n{G}",
        "# Main Database\n\nOne schema.",
    ),
    "pay/datastores/DB-main/log.md": LOG,
    "pay/datastores/DB-main/TBL-payments.md": page(
        f"type: Table\ntitle: payments\ndescription: One row per payment.\nstatus: Active\ntableName: payments\n{G}",
        "# payments\n\n# Schema\n\n| Column | Type | Required | Notes |\n|---|---|---|---|\n| `id` | uuid | yes | key |",
    ),
    "pay/datastores/CACHE-pay/overview.md": page(
        f"type: Cache\ntitle: Pay Cache\ndescription: Idempotency keys.\nstatus: Active\nengine: redis\n{G}",
        "# Pay Cache\n\n# Value\n\nA payment id.\n\n# Caches\n\n* [TBL-payments](../DB-main/TBL-payments.md)",
    ),
    "pay/datastores/CACHE-pay/log.md": LOG,
    "pay/datastores/BLOB-receipts/overview.md": page(
        f"type: BlobStore\ntitle: Receipts\ndescription: Receipt PDFs.\nstatus: Active\nprovider: s3\n{G}",
        "# Receipts\n\n# Content types\n\n* application/pdf",
    ),
    "pay/datastores/BLOB-receipts/log.md": LOG,
    "pay/datastores/IDX-payments/overview.md": page(
        f"type: SearchIndex\ntitle: Payment Search\ndescription: Search payments.\nstatus: Active\nengine: opensearch\n{G}",
        "# Payment Search\n\n# Indexed fields\n\n`id` (keyword).",
    ),
    "pay/datastores/IDX-payments/log.md": LOG,
    # ------------------------------------------------------------------ externals
    "pay/externals/EXT-bank/overview.md": page(
        f"type: ExternalService\ntitle: Bank\ndescription: Card rail.\nstatus: Active\nvendor: Bank\n"
        f"apiUrl: https://api.bank.example\n{G}",
        "# Bank\n\n# Fallback\n\nFail the payment.",
    ),
    "pay/externals/EXT-bank/log.md": LOG,
    "pay/externals/EXT-bank/OP-charge.md": page(
        f"type: Operation\ntitle: Charge\ndescription: POST /charge.\nstatus: Active\nmethod: POST\npath: /charge\n{G}",
        "# Charge\n\n# Schema\n\n| Direction | Field | Type | Required |\n|---|---|---|---|\n| request | amount | number | yes |\n\n"
        "# Failure handling\n\nRetry once.",
    ),
    # ------------------------------------------------------------------ frontends
    "pay/frontends/WEB-shop/overview.md": page(
        f"type: WebFrontend\ntitle: Web Shop\ndescription: Browser shop.\nstatus: Active\nownerTeam: web\n"
        f"resource: https://example.com/acme/web\n{G}",
        "# Web Shop\n\nBrowser shop.\n\n# Routes\n\n| Route | Surface | Access | Description |\n|---|---|---|---|\n"
        "| `/pay` | Pay | authenticated | Pay page. |\n\n# Architecture\n\n```mermaid\nflowchart LR\n  Web --> Svc\n```\n\n"
        "# Calls\n\n* [EP-pay-create](../../services/SVC-pay/EP-pay-create.md) — pays.\n\n"
        "# Runtime behavior\n\nText.\n\n# Quality constraints\n\nText.",
    ),
    "pay/frontends/WEB-shop/log.md": LOG,
    "pay/frontends/MB-shop/overview.md": page(
        f"type: MobileFrontend\ntitle: Mobile Shop\ndescription: Phone shop.\nstatus: Active\nownerTeam: mobile\n"
        f"resource: https://example.com/acme/mobile\nplatform: cross-platform\n{G}",
        "# Mobile Shop\n\nPhone shop.\n\n# Screens and navigation\n\n| Screen | Navigation path | Access | Description |\n"
        "|---|---|---|---|\n| Pay | Cart > Pay | authenticated | Pay screen. |\n\n"
        "# Architecture\n\n```mermaid\nflowchart LR\n  App --> Svc\n```\n\n# Calls\n\nNone.\n\n"
        "# Runtime behavior\n\nText.\n\n# Platform integrations\n\nNone.\n\n# Quality constraints\n\nText.",
    ),
    "pay/frontends/MB-shop/log.md": LOG,
    # ---------------------------------------------------------------------- tests
    "pay/tests/TS-pay/overview.md": page(
        f"type: TestSuite\ntitle: Pay Suite\ndescription: Tests of paying.\n{G}",
        "# Pay Suite\n\n# Verifies\n\n* [FEAT-pay](../../features/FEAT-pay/overview.md)",
    ),
    "pay/tests/TS-pay/STORY-pay-checkout/overview.md": page(
        f"type: TestGroup\ntitle: Pay at checkout\ndescription: Cases of the pay at checkout story.\nstatus: Approved\n{G}\n{B}",
        "# Pay at checkout\n\n# Story\n\n* [STORY-pay-checkout](../../../features/FEAT-pay/STORY-pay-checkout.md)",
    ),
    "pay/tests/TS-pay/STORY-pay-checkout/log.md": LOG,
    "pay/tests/TS-pay/STORY-pay-checkout/TC-1-pay-ok.md": page(
        f"type: TestCase\ntitle: Payment succeeds\ndescription: A valid payment is taken.\nrisk: high\ntestType: e2e\ntestCategory: functional\n{G}",
        "# Payment succeeds\n\n# Covers\n\n* [STORY-pay-checkout](../../../features/FEAT-pay/STORY-pay-checkout.md) — AC 1\n"
        "* [REQ-pay-1](../../../features/FEAT-pay/overview.md#req-pay-1)\n"
        "* [EP-pay-create](../../../services/SVC-pay/EP-pay-create.md)\n\n# Purpose\n\nProve a payment works.\n\n"
        "# Preconditions\n\nA cart; card 4242 4242 4242 4242.\n\n# Steps\n\n"
        "| Step | Action | Expected result | Validation |\n|---|---|---|---|\n| 1 | Pay | Paid | Row **status** |\n\n"
        "# Postconditions and cleanup\n\nDelete the payment.",
    ),
    # ----------------------------------------------------------------- references
    "pay/references/REF-pay-prd/overview.md": page(
        f"type: Reference\ntitle: Pay PRD\ndescription: Approved product requirements; read before changing payments.\n"
        f"status: Active\n{G}\n{V}",
        "# Pay PRD\n\nThe product requirements for paying, as approved.\n\n"
        "# Contents\n\n* [prd.md](prd.md) — the full PRD.",
    ),
    "pay/references/REF-pay-prd/log.md": LOG,
    "pay/references/REF-pay-prd/prd.md": "# Pay PRD\n\nShoppers pay for orders.\n\n![Flow](images/flow.png)\n",
    "pay/references/REF-pay-prd/images/flow.png": "not really a picture\n",
}

INDEX_DIRS = [
    "pay", "pay/decisions", "pay/features", "pay/features/FEAT-pay", "pay/change-requests",
    "pay/change-requests/CR-1", "pay/services", "pay/services/SVC-pay", "pay/channels",
    "pay/channels/CHAN-pay-events", "pay/datastores", "pay/datastores/DB-main", "pay/datastores/CACHE-pay",
    "pay/datastores/BLOB-receipts", "pay/datastores/IDX-payments", "pay/externals", "pay/externals/EXT-bank",
    "pay/frontends", "pay/frontends/WEB-shop", "pay/frontends/MB-shop", "pay/tests", "pay/tests/TS-pay", "pay/tests/TS-pay/STORY-pay-checkout",
    "pay/references", "pay/references/REF-pay-prd",
]


def general_case(text: str) -> str:
    """A copy of the fixture case for GENERAL: no link to the story."""
    return text.replace("* [STORY-pay-checkout](../../../features/FEAT-pay/STORY-pay-checkout.md) — AC 1\n", "")


def add_general(root: Path) -> None:
    """Give the fixture suite a GENERAL group with no cases yet."""
    write(root, "pay/tests/TS-pay/GENERAL/overview.md", page(
        f"type: TestGroup\ntitle: General\ndescription: Cases of no single story.\nstatus: Draft\n{G}\n{B}",
        "# General\n\n# Scope\n\nPaying end to end.",
    ))
    write(root, "pay/tests/TS-pay/GENERAL/log.md", LOG)
    sync.write(root)


def make_bundle(root: Path) -> Path:
    """Write the fixture bundle under `root` and return `root`."""
    if root.exists():
        shutil.rmtree(root)
    for rel, text in FILES.items():
        write(root, rel, text)
    for directory in INDEX_DIRS:
        write(root, f"{directory}/index.md", INDEX)
    sync.write(root)
    return root


def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8")


def edit(root: Path, rel: str, old: str, new: str) -> None:
    """Replace `old` with `new` in one file; fail loudly when `old` is absent."""
    text = read(root, rel)
    if old not in text:
        raise AssertionError(f"{old!r} not found in {rel}")
    write(root, rel, text.replace(old, new))


def remove(root: Path, rel: str) -> None:
    path = root / rel
    shutil.rmtree(path) if path.is_dir() else path.unlink()
