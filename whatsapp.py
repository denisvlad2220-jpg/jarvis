"""WhatsApp Cloud API (ufficiale Meta). Usata come router FastAPI."""
import os
import requests
from fastapi import APIRouter, Request, Response
from .. import brain, inbox

router = APIRouter()


def send(to: str, text: str):
    requests.post(f"https://graph.facebook.com/v20.0/{os.getenv('WHATSAPP_PHONE_ID')}/messages",
                  headers={"Authorization": f"Bearer {os.getenv('WHATSAPP_TOKEN')}"},
                  json={"messaging_product": "whatsapp", "to": to,
                        "type": "text", "text": {"body": text[:4000]}}, timeout=15)


@router.get("/whatsapp")
def verify(request: Request):
    q = request.query_params
    if q.get("hub.verify_token") == os.getenv("WHATSAPP_VERIFY_TOKEN"):
        return Response(q.get("hub.challenge"))
    return Response(status_code=403)


@router.post("/whatsapp")
async def incoming(request: Request):
    body = await request.json()
    allowed = {x.strip() for x in os.getenv("WHATSAPP_ALLOWED_NUMBERS", "").split(",") if x.strip()}
    for entry in body.get("entry", []):
        for ch in entry.get("changes", []):
            for msg in ch["value"].get("messages", []):
                if msg.get("type") != "text":
                    continue
                sender, text = msg["from"], msg["text"]["body"]
                inbox.add("whatsapp", sender, text)
                if sender in allowed:
                    send(sender, brain.chat(f"wa:{sender}", text))
    return {"ok": True}
