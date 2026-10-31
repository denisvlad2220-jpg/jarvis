import asyncio, os
import discord
from .. import brain, inbox, documents

ALLOWED = {x.strip() for x in os.getenv("DISCORD_ALLOWED_USER_IDS", "").split(",") if x.strip()}


class JarvisBot(discord.Client):
    async def on_message(self, m: discord.Message):
        if m.author == self.user:
            return
        where = f"{m.guild.name}/#{m.channel}" if m.guild else "DM"
        inbox.add("discord", f"{m.author} ({where})", m.content)
        for a in m.attachments:
            documents.save(a.filename, await a.read())
        addressed = isinstance(m.channel, discord.DMChannel) or (self.user in m.mentions)
        if not addressed or str(m.author.id) not in ALLOWED:
            return
        text = m.content.replace(f"<@{self.user.id}>", "").strip() or "Ho caricato un file."
        if m.attachments:
            text += f"\n(File caricati: {[a.filename for a in m.attachments]})"
        async with m.channel.typing():
            reply = await asyncio.to_thread(brain.chat, f"discord:{m.author.id}", text)
        await m.reply(reply[:1900])


def run():
    intents = discord.Intents.default()
    intents.message_content = True
    asyncio.run(JarvisBot(intents=intents).start(os.environ["DISCORD_TOKEN"]))
