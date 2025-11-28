import json, os
from datetime import datetime

INPUT = "events/events.jsonl"
OUTPUT = "data_layer.json"

def normalize(event):
    src = event.get("source")
    p = event.get("payload", {})
    # schema alvo: transaction_id, amount (float, BRL), method, status, source, timestamp
    if src == "maquininha":
        tx_id = p.get("tx_id")
        amount = p.get("valor_centavos",0) / 100.0
        method = p.get("tipo")
        status = "approved" if p.get("status") == "approved" else "declined"
    elif src == "ecommerce":
        tx_id = p.get("transactionId")
        amount = float(p.get("amount", 0.0))
        method = p.get("method")
        status = "paid" if p.get("status") == "paid" else "failed"
    else: # link_pagamento
        tx_id = p.get("id")
        amount = p.get("amount_cents",0) / 100.0
        method = p.get("payment_type")
        status = "ok" if p.get("result") == "ok" else "error"

    return {
        "transaction_id": tx_id,
        "amount": round(float(amount),2),
        "method": method,
        "status": status,
        "source": src,
        "timestamp": event.get("timestamp")
    }

def process():
    seen = set()
    output = []
    if not os.path.exists(INPUT):
        print("No events found. Run generator first.")
        return
    with open(INPUT, "r", encoding="utf-8") as f:
        for line in f:
            event = json.loads(line)
            norm = normalize(event)
            tx = norm["transaction_id"]
            # idempotency/deduplication
            if tx in seen:
                continue
            seen.add(tx)
            # simple validation
            if not norm["transaction_id"]:
                continue
            output.append(norm)
    # sort by timestamp (desc)
    output.sort(key=lambda x: x.get("timestamp") or "", reverse=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(output)} normalized transactions to {OUTPUT}")

if __name__ == "__main__":
    process()
