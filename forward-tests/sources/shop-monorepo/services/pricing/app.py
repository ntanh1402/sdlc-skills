"""Pricing service: what a product costs today."""
from fastapi import FastAPI, HTTPException

from .db import connection

app = FastAPI(title="Pricing service", version="1")


@app.get("/prices/{sku}")
def get_price(sku: str) -> dict:
    """200 with the current price in USD; 404 when the product has no price. No authentication: internal network only."""
    row = connection().execute(
        "SELECT sku, price_usd FROM prices WHERE sku = %s AND valid_from <= now() ORDER BY valid_from DESC LIMIT 1", (sku,)
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404)
    return {"sku": row[0], "priceUsd": float(row[1])}
