"""Inventory service: how many units of a product are in stock."""
from fastapi import FastAPI, HTTPException

from .db import connection

app = FastAPI(title="Inventory service", version="1")


@app.get("/stock/{sku}")
def get_stock(sku: str) -> dict:
    """200 with the units on hand; 404 when the product is unknown. No authentication: internal network only."""
    row = connection().execute("SELECT sku, on_hand, updated_at FROM stock WHERE sku = %s", (sku,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404)
    return {"sku": row[0], "onHand": row[1], "updatedAt": row[2].isoformat()}
