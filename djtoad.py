import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Importar los cogs
from commands.music_commands import MusicCommands
from commands.other_commands import OtherCommands
from commands.help_commands import HelpCommands
from commands.trivial_commands import TrivialCommands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)  # Desactivar el comando help predeterminado

@bot.event
async def on_ready():
    print(f'✅ Tu rana favorita conectada como {bot.user}')

async def setup_bot():
    await bot.add_cog(MusicCommands(bot))
    await bot.add_cog(OtherCommands(bot))
    await bot.add_cog(HelpCommands(bot))  # Registrar el cog de ayuda separado
    await bot.add_cog(TrivialCommands(bot)) 

    await bot.start(DISCORD_TOKEN)

if __name__ == '__main__':
    try:
        asyncio.run(setup_bot())
    except KeyboardInterrupt:
        print("❌ Bot detenido manualmente. ¡Hasta pronto!")
