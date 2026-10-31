// Calls to the orders service. Every call sends the customer's session token.
const ORDERS_URL = process.env.NEXT_PUBLIC_ORDERS_URL ?? "https://api.shop.example.com";

export type OrderRef = { orderId: string; status: string };

/** POST /orders: 201 and 409 both carry the order; anything else is an error the page shows. */
export async function createOrder(session: string, cartId: string, customerId: string, paymentMethod: string,
                                  clientToken: string): Promise<OrderRef> {
  const response = await fetch(`${ORDERS_URL}/orders`, {
    method: "POST",
    headers: { Authorization: `Bearer ${session}`, "Content-Type": "application/json" },
    body: JSON.stringify({ cartId, customerId, paymentMethod, clientToken }),
  });
  if (response.status !== 201 && response.status !== 409) {
    throw new Error(`checkout failed: ${response.status}`);
  }
  return response.json();
}
