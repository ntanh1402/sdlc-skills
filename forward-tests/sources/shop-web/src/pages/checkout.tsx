import { useState } from "react";
import { useRouter } from "next/router";
import { createOrder } from "../api/orders";
import { useCart, useSession } from "../state";

/** /checkout: needs a login. The Pay button is disabled while the request runs, so a double click sends one request. */
export default function Checkout() {
  const router = useRouter();
  const session = useSession({ redirectTo: "/login?return=/checkout" });
  const cart = useCart();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [clientToken] = useState(() => crypto.randomUUID());

  async function pay(paymentMethod: string) {
    setBusy(true);
    setError(null);
    try {
      const order = await createOrder(session.token, cart.id, session.customerId, paymentMethod, clientToken);
      router.push(`/orders/${order.orderId}/confirmation`);
    } catch (failure) {
      setError("We could not take the payment. Your cart is unchanged; please try again.");
    } finally {
      setBusy(false);
    }
  }

  return <CheckoutForm cart={cart} busy={busy} error={error} onPay={pay} />;
}
