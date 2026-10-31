# Brief: wishlist

**Owner:** web team. **Priority:** P2. **Application:** shop.

## Problem and evidence
Shoppers who are not ready to buy lose track of products. Support logged 140
requests last quarter asking for a way to save products; 30% of sessions that
view a product three or more times end without an add-to-cart.

## Outcome and why now
Signed-in customers can save products to a personal wishlist and come back to
them. The spring campaign (in eight weeks) links to wishlists from email.

## Actors
Signed-in customer. Guests are out of scope.

## Flows
- Trigger: the customer presses "Save" on a product page.
- Happy: the product is added to their wishlist; the wishlist page lists saved
  products with name, price and availability; the customer can remove one or
  move it to the cart.
- Alternate: saving a product already in the wishlist does nothing and says so.
- Failure: if the product is no longer sold, it stays on the list marked
  "unavailable" and cannot be moved to the cart.

## Business rules
- A wishlist belongs to exactly one customer and is never visible to others.
- At most 100 products per wishlist; the 101st save is refused with a message.
- Prices shown are the current catalog prices, not the price when saved.

## Data, events and external parties
- Input: product id from the catalog. Output: the list of saved products.
- No sensitive data beyond the customer id. No external parties.
- Event: "wishlist item saved", for marketing analytics.

## Requirements
1. Must, functional: a signed-in customer can save a product to their
   wishlist. Verified by test.
2. Must, functional: a customer can remove a saved product, or move it to the
   cart. Verified by test.
3. Must, security: only the owner can read or change a wishlist. Verified by
   test.
4. Should, nonfunctional: the wishlist page loads within 500 ms at the 95th
   percentile with 100 items. Verified by load test.
5. Must, constraint: at most 100 products per wishlist. Verified by test.

## Success measures
Within 90 days: 15% of signed-in customers save at least one product; 8% of
saved products are later bought.

## Acceptance
All five requirements verified; the email campaign links open the wishlist.

## Risks, constraints, assumptions
- Risk: wishlists of discontinued products grow stale; mitigated by the
  "unavailable" mark.
- Constraint: no change to the checkout flow.
- Assumption: customers are signed in through the existing accounts feature.

## Open questions
None.

## Out of scope
Sharing wishlists, guest wishlists, price-drop alerts.
