import sys, threading, os
from dotenv import load_dotenv

load_dotenv()

from jarvis import brain  # noqa: E402


def cli():
    print("Jarvis pronto (CTRL+C per uscire).")
    while True:
        print("\nJarvis:", brain.chat("cli", input("\nTu: ")))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        cli()
    else:
        if os.getenv("DISCORD_TOKEN"):
            from jarvis.connectors import discord_bot
            threading.Thread(target=discord_bot.run, daemon=True).start()
        import uvicorn
        uvicorn.run("jarvis.api:app", host="0.0.0.0", port=8000)
