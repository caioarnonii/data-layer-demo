import json, random, uuid, os
from datetime import datetime, timedelta

os.makedirs("events", exist_ok=True)

sources = ["maquininha", "ecommerce", "link_pagamento"]

def fake_tx(source, i):
    base = {
        "event_id": str(uuid.uuid4()),
        "timestamp": (datetime.utcnow() - timedelta(minutes=random.randint(0, 1000))).isoformat() + "Z",
        "source": source,
    }
    if source == "maquininha":
        payload = {
            "tx_id": f"tx-{source}-{i}",
            "valor_centavos": random.randint(100, 20000),
            "tipo": random.choice(["credito","debito"]),
            "status": random.choice(["approved","declined"])
        }
    elif source == "ecommerce":
        payload = {
            "transactionId": f"tx-{source}-{i}",
            "amount": round(random.uniform(1,200),2),
            "method": random.choice(["credit_card","pix"]),
            "status": random.choice(["paid","failed"])
        }
    else: # link_pagamento
        payload = {
            "id": f"tx-{source}-{i}",
            "amount_cents": random.randint(50,15000),
            "payment_type": random.choice(["credit","pix","boleto"]),
            "result": random.choice(["ok","error"])
        }
    base["payload"] = payload
    return base

events = []
for s in sources:
    for i in range(10):
        events.append(fake_tx(s, i))

with open("events/events.jsonl", "w", encoding="utf-8") as f:
    for e in events:
        f.write(json.dumps(e)+"\n")

print("Generated", len(events), "events in events/events.jsonl")
