from fastapi import FastAPI, HTTPException, Query, Request
from typing import List, Optional
from datetime import datetime
import json, os

DATA_FILE = "data_layer.json"
app = FastAPI(title="Data Layer Demo")

# Métricas simples
REQUEST_COUNT = 0
ERROR_COUNT = 0

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Middleware para contar requisições
@app.middleware("http")
async def count_requests(request: Request, call_next):
    global REQUEST_COUNT, ERROR_COUNT
    REQUEST_COUNT += 1
    try:
        response = await call_next(request)
        return response
    except Exception:
        ERROR_COUNT += 1
        raise

@app.get("/metrics")
def get_metrics():
    return {
        "total_requests": REQUEST_COUNT,
        "total_errors": ERROR_COUNT
    }

@app.get("/sales")
def get_sales(
    source: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = Query(50, le=200)
):
    data = load_data()

    # Filtro por source
    if source:
        data = [d for d in data if d["source"] == source]

    # Filtro por status
    if status:
        data = [d for d in data if d["status"] == status]

    # Filtro por data (YYYY-MM-DD)
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            data = [d for d in data if datetime.strptime(d["timestamp"], "%Y-%m-%d") >= start_dt]
        except:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD")

    if end_date:
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            data = [d for d in data if datetime.strptime(d["timestamp"], "%Y-%m-%d") <= end_dt]
        except:
            raise HTTPException(status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD")

    return data[:limit]

@app.get("/sales/{tx_id}")
def get_sale(tx_id: str):
    data = load_data()
    for d in data:
        if d["transaction_id"] == tx_id:
            return d

    raise HTTPException(status_code=404, detail="transaction not found")
