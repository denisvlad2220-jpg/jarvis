# Jarvis

Assistente personale basato su Claude. Capisce italiano, legge i tuoi file (es. orario scolastico, anche foto),
legge WhatsApp e Discord, controlla un server Minecraft e i dispositivi di casa.

## Avvio
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env     # compila almeno ANTHROPIC_API_KEY
python main.py cli       # chat da terminale
python main.py           # server (API + Discord) su :8000
```

## Usare i file
```bash
curl -F "file=@orario.pdf" -H "X-Jarvis-Key: LA_TUA_CHIAVE" http://localhost:8000/upload
curl -H "X-Jarvis-Key: LA_TUA_CHIAVE" -H "Content-Type: application/json" \
     -d '{"message":"Che materie ho domani?"}' http://localhost:8000/chat
```
Su Discord: scrivi al bot in DM allegando il file, poi chiedi "che materie ho domani?".

## Collegamenti
| Servizio | Come |
|---|---|
| Discord | Crea un bot, abilita *Message Content Intent*, metti `DISCORD_TOKEN` e i tuoi ID in `DISCORD_ALLOWED_USER_IDS` |
| WhatsApp | API ufficiale Meta Cloud: webhook su `https://TUO-DOMINIO/whatsapp` (usa ngrok/Cloudflare Tunnel in locale) |
| Minecraft | `enable-rcon=true` in `server.properties`, compila `MC_RCON_*` e `MC_LOG_PATH` |
| Dispositivi | Collega tutto a Home Assistant e metti `HA_URL` + `HA_TOKEN` |

## Sicurezza
- Solo gli ID/numeri in `*_ALLOWED_*` possono dare ordini; gli altri messaggi vengono solo registrati.
- Comandi Minecraft pericolosi (`stop`, `op`, `ban`...) bloccati finché `MC_ALLOW_DANGEROUS=true`.
- Non committare mai `.env`. Cambia `JARVIS_API_KEY`.
- WhatsApp personale non ufficiale (es. librerie che emulano WhatsApp Web) viola i termini e rischia il ban: qui uso solo l'API ufficiale.
