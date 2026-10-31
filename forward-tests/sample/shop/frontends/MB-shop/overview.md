---
type: MobileFrontend
title: Shop Mobile
description: Native mobile storefront for iOS and Android.
status: Active
ownerTeam: commerce-experience
platform: cross-platform
language: TypeScript
framework: React Native
minimumOsVersion: iOS 17 and Android 12
applicationId: com.acme.shop
bundleId: com.acme.shop
distribution: app-store
buildTool: Expo
version: 1.0.0
offlineCapable: false
resource: https://github.com/acme/shop-mobile
generated: { by: human:sample-author, at: 2026-08-09T00:00:00Z }
verified: { by: human:sample-author, at: 2026-08-09T00:00:00Z }
---

# Shop Mobile

Customer-facing iOS and Android application sharing one React Native runtime.

# Screens and navigation

| Screen | Navigation path | Access | Description |
|---|---|---|---|
| Catalog | Home tab | public | Browse featured products and categories. |
| Cart | Cart tab | authenticated | Review quantities and order total. |
| Checkout | Cart → Checkout | authenticated | Confirm delivery details and submit the order. |
| Order confirmation | Checkout → Confirmation | authenticated | Show confirmed order status. |

# Architecture

```mermaid
flowchart LR
  Device --> Mobile[MB-shop]
  Mobile --> Orders[EP-orders-create]
```

React Navigation owns screen transitions. Feature modules own transient UI
state; API responses remain source of truth for cart and order state.

# Calls

* [EP-orders-create](../../services/SVC-orders/EP-orders-create.md) — submits checkout. The screen disables repeat submission while loading, navigates to confirmation on success, retries transient network failures with backoff, and preserves entered delivery data after terminal failure.

# Runtime behavior

Startup restores the encrypted session before opening authenticated screens.
Server state is cached per account and invalidated after mutations. Checkout
requires connectivity; loss of network preserves form state and exposes retry.
Expired sessions return to login, then resume the intended navigation path.

# Platform integrations

None.

# Quality constraints

Support iOS 17+, Android 12+, phones, and tablets. Meet platform accessibility
guidance and WCAG 2.2 AA. Keep warm startup below 1s, cold startup below 2.5s,
interactive response below 100ms, and release crashes below 0.2% of sessions.
