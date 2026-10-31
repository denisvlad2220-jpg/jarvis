"""Strumenti che Jarvis può usare."""
from datetime import datetime, timedelta
import os
from zoneinfo import ZoneInfo
from . import documents, inbox
from .connectors import minecraft, devices


def _s(props, req=()):
    return {"type": "object", "properties": props, "required": list(req)}


STR = {"type": "string"}
TOOLS = [
    {"name": "get_datetime", "description": "Data/ora attuale, giorno della settimana e domani.", "input_schema": _s({})},
    {"name": "list_documents", "description": "Elenca i file caricati dall'utente.", "input_schema": _s({})},
    {"name": "read_document", "description": "Legge un file caricato (txt, pdf, docx, csv, immagini/foto dell'orario).",
     "input_schema": _s({"name": STR}, ["name"])},
    {"name": "read_inbox", "description": "Legge messaggi recenti salvati da whatsapp o discord.",
     "input_schema": _s({"source": {"type": "string", "enum": ["", "whatsapp", "discord"]},
                         "limit": {"type": "integer"}, "query": STR})},
    {"name": "minecraft_command", "description": "Esegue un comando sul server Minecraft via RCON (es. 'list', 'say ciao').",
     "input_schema": _s({"command": STR}, ["command"])},
    {"name": "minecraft_log", "description": "Ultime righe del log del server Minecraft.",
     "input_schema": _s({"lines": {"type": "integer"}})},
    {"name": "list_devices", "description": "Elenca i dispositivi/entità collegati (Home Assistant).",
     "input_schema": _s({"domain": STR})},
    {"name": "control_device", "description": "Controlla un dispositivo, es. domain=light service=turn_on entity_id=light.camera.",
     "input_schema": _s({"domain": STR, "service": STR, "entity_id": STR}, ["domain", "service", "entity_id"])},
]


def run_tool(name: str, a: dict):
    try:
        if name == "get_datetime":
            now = datetime.now(ZoneInfo(os.getenv("TIMEZONE", "Europe/Rome")))
            t = now + timedelta(days=1)
            return f"Adesso: {now:%A %d/%m/%Y %H:%M}. Domani: {t:%A %d/%m/%Y}."
        if name == "list_documents":
            return str(documents.list_docs())
        if name == "read_document":
            return documents.read_doc(a["name"])
        if name == "read_inbox":
            return inbox.read(a.get("source", ""), a.get("limit", 20), a.get("query", ""))
        if name == "minecraft_command":
            return minecraft.command(a["command"])
        if name == "minecraft_log":
            return minecraft.log(a.get("lines", 50))
        if name == "list_devices":
            return devices.list_devices(a.get("domain", ""))
        if name == "control_device":
            return devices.call(a["domain"], a["service"], a["entity_id"])
        return f"Strumento sconosciuto: {name}"
    except Exception as e:
        return f"Errore strumento {name}: {e}"
