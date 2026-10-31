"""Registro unico dei messaggi letti da WhatsApp / Discord / Minecraft."""
import json, time
from pathlib import Path

FILE = Path("data/inbox.jsonl")
FILE.parent.mkdir(parents=True, exist_ok=True)


def add(source: str, sender: str, text: str):
    with FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"t": time.strftime("%Y-%m-%d %H:%M"), "source": source,
                            "from": sender, "text": text}, ensure_ascii=False) + "\n")


def read(source: str = "", limit: int = 20, query: str = "") -> str:
    if not FILE.exists():
        return "Nessun messaggio salvato."
    rows = [json.loads(l) for l in FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    if source:
        rows = [r for r in rows if r["source"] == source]
    if query:
        rows = [r for r in rows if query.lower() in r["text"].lower()]
    rows = rows[-limit:]
    return "\n".join(f'[{r["t"]}] {r["source"]} | {r["from"]}: {r["text"]}' for r in rows) or "Nessun risultato."
