import os
import asyncio
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Setup logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("main")

# ---------------------------------------------------------------------------
# Load environment variables (.env in locale, variabili Railway in produzione)
# ---------------------------------------------------------------------------
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError(
        "Variabile d'ambiente DISCORD_TOKEN mancante. "
        "Impostala nelle Variables del progetto su Railway."
    )

PREFIX = os.getenv("BOT_PREFIX", "!")

# ---------------------------------------------------------------------------
# Intents: abilita quelli di cui il bot ha effettivamente bisogno
# ---------------------------------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True  # necessario per i comandi con prefisso
intents.members = True          # necessario se usi eventi/legati ai membri

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ---------------------------------------------------------------------------
# Cartella dei cogs: modifica "cogs" se i tuoi comandi sono organizzati
# diversamente (es. "commands", "modules", ecc.)
# ---------------------------------------------------------------------------
COGS_FOLDER = "cogs"


async def load_extensions() -> None:
    """Carica automaticamente tutti i cogs presenti nella cartella COGS_FOLDER."""
    if not os.path.isdir(COGS_FOLDER):
        log.warning(
            "Cartella '%s' non trovata: nessun cog caricato automaticamente.",
            COGS_FOLDER,
        )
        return

    for filename in os.listdir(COGS_FOLDER):
        if filename.endswith(".py") and not filename.startswith("_"):
            extension = f"{COGS_FOLDER}.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
                log.info("Cog caricato: %s", extension)
            except Exception:
                log.exception("Errore nel caricamento del cog: %s", extension)


@bot.event
async def on_ready() -> None:
    log.info("Bot connesso come %s (ID: %s)", bot.user, bot.user.id)


async def main() -> None:
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
