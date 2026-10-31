import os
from pathlib import Path

DANGEROUS = {"stop", "op", "deop", "ban", "ban-ip", "pardon", "whitelist", "kill", "save-off"}


def command(cmd: str) -> str:
    from mcrcon import MCRcon
    first = cmd.strip().lstrip("/").split(" ")[0].lower()
    if first in DANGEROUS and os.getenv("MC_ALLOW_DANGEROUS", "false").lower() != "true":
        return f"Comando '{first}' bloccato. Imposta MC_ALLOW_DANGEROUS=true per abilitarlo."
    try:
        with MCRcon(os.getenv("MC_RCON_HOST", "127.0.0.1"), os.getenv("MC_RCON_PASSWORD", ""),
                    port=int(os.getenv("MC_RCON_PORT", "25575"))) as m:
            return m.command(cmd) or "(ok, nessuna risposta)"
    except Exception as e:
        return f"Errore RCON: {e}"


def log(lines: int = 50) -> str:
    p = os.getenv("MC_LOG_PATH")
    if not p or not Path(p).exists():
        return "MC_LOG_PATH non configurato o file inesistente."
    return "\n".join(Path(p).read_text(errors="replace").splitlines()[-lines:])
