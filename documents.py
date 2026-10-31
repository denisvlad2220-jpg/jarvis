"""Gestione file caricati (orario scolastico, appunti, PDF, foto...)."""
import base64
from pathlib import Path

DOCS = Path("data/docs")
DOCS.mkdir(parents=True, exist_ok=True)
IMAGES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def save(name: str, content: bytes) -> str:
    safe = Path(name).name  # niente path traversal
    (DOCS / safe).write_bytes(content)
    return safe


def list_docs() -> list[str]:
    return sorted(p.name for p in DOCS.iterdir() if p.is_file())


def read_doc(name: str):
    """Ritorna testo (str) oppure lista di blocchi (per le immagini)."""
    path = DOCS / Path(name).name
    if not path.exists():
        return f"File '{name}' non trovato. Disponibili: {list_docs()}"
    ext = path.suffix.lower()
    if ext in IMAGES:
        data = base64.standard_b64encode(path.read_bytes()).decode()
        return [{"type": "image", "source": {"type": "base64", "media_type": IMAGES[ext], "data": data}}]
    if ext == ".pdf":
        from pypdf import PdfReader
        return "\n".join(p.extract_text() or "" for p in PdfReader(str(path)).pages)[:30000]
    if ext == ".docx":
        import docx
        return "\n".join(p.text for p in docx.Document(str(path)).paragraphs)[:30000]
    return path.read_text(errors="replace")[:30000]
