import os
from fastapi import FastAPI, Header, HTTPException, UploadFile
from pydantic import BaseModel
from . import brain, documents
from .connectors.whatsapp import router as wa_router

app = FastAPI(title="Jarvis")
app.include_router(wa_router)


def _auth(key):
    if key != os.getenv("JARVIS_API_KEY"):
        raise HTTPException(401, "Chiave non valida")


class Msg(BaseModel):
    message: str
    session: str = "default"


@app.post("/chat")
def chat(m: Msg, x_jarvis_key: str = Header(None)):
    _auth(x_jarvis_key)
    return {"reply": brain.chat(m.session, m.message)}


@app.post("/upload")
async def upload(file: UploadFile, x_jarvis_key: str = Header(None)):
    _auth(x_jarvis_key)
    return {"saved": documents.save(file.filename, await file.read())}
