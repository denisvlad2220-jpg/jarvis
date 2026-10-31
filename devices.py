"""Controllo dispositivi tramite Home Assistant (luci, prese, PC, TV, telefoni, ecc.)."""
import os
import requests


def _h():
    return {"Authorization": f"Bearer {os.getenv('HA_TOKEN','')}", "Content-Type": "application/json"}


def list_devices(domain: str = "") -> str:
    try:
        r = requests.get(f"{os.getenv('HA_URL')}/api/states", headers=_h(), timeout=10)
        r.raise_for_status()
        out = [f"{s['entity_id']} = {s['state']}" for s in r.json()
               if not domain or s["entity_id"].startswith(domain + ".")]
        return "\n".join(out[:150]) or "Nessun dispositivo."
    except Exception as e:
        return f"Errore Home Assistant: {e}"


def call(domain: str, service: str, entity_id: str, data: dict | None = None) -> str:
    try:
        body = {"entity_id": entity_id, **(data or {})}
        r = requests.post(f"{os.getenv('HA_URL')}/api/services/{domain}/{service}",
                          headers=_h(), json=body, timeout=10)
        r.raise_for_status()
        return f"OK: {domain}.{service} su {entity_id}"
    except Exception as e:
        return f"Errore Home Assistant: {e}"
