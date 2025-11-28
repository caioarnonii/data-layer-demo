from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
import json, os

DATA_FILE = "data_layer.json"
app = FastAPI(title="Data Layer Demo")

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/sales")
def get_sales(source: Optional[str] = None, status: Optional[str] = None, limit: int = Query(50, le=200)):
    data = load_data()
    if source:
        data = [d for d in data if d["source"] == source]
    if status:
        data = [d for d in data if d["status"] == status]
    return data[:limit]

@app.get("/sales/{tx_id}")
def get_sale(tx_id: str):
    data = load_data()
    for d in data:
        if d["transaction_id"] == tx_id:
            return d
    raise HTTPException(status_code=404, detail="transaction not found")
