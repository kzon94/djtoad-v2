# bot.py

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Cargar variables de entorno
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Configurar el bot con los intents necesarios
intents = discord.Intents.default()
intents.message_content = True  # Necesario para recibir el contenido de los mensajes
bot = commands.Bot(command_prefix="!", intents=intents)

# Cargar los módulos de comandos
from commands.music_commands import MusicCommands
from commands.other_commands import OtherCommands

# Añadir los comandos al bot
bot.add_cog(MusicCommands(bot))
bot.add_cog(OtherCommands(bot))

# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f'✅ Tu rana favorita conectada como {bot.user}')

# Ejecutar el bot
bot.run(DISCORD_TOKEN)
