# commands/help_commands.py

import discord
from discord.ext import commands

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        """Muestra la ayuda con los comandos disponibles."""
        embed = discord.Embed(
            title="📖 Comandos Disponibles de DJ Toad",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="🔹 ¡Comandos de Música!",
            value=(
                "`!play [canción/artista]` - Busca y reproduce una canción.\n"
                "`!add [canción/artista]` - Añade una canción al inicio de la cola.\n"
                "`!list` - Muestra la canción actual y la cola de reproducción.\n"
                "`!next` - Salta a la siguiente canción.\n"
                "`!pause` - Pausa la canción actual.\n"
                "`!resume` - Reanuda la canción pausada.\n"
                "`!stop` - Detiene la música y desconecta al bot."
            ),
            inline=False
        )
        embed.add_field(
            name="🔹 ¡Comandos de Trivia!",
            value=(
                "`!trivial` - Inicia un juego de trivia musical.\n"
                "`!trivial_stop` - Detiene el juego de trivia en curso.\n"
                "`!leaderboard` - Muestra el ranking del trivial."
            ),
            inline=False
        )
        embed.add_field(
            name="🔹 ¡Comandos Divertidos!",
            value=(
                "`!dance1`, `!dance2` - ¡Saca a Toad a bailar!"
            ),
            inline=False
        )
        embed.add_field(
            name="🔹 ¡Comandos Administrativos!",
            value=(
                "`!restart_bot` - Reinicia el bot en el servidor (solo admin).\n"
                "`!shutdown_bot` - Apaga el bot completamente (solo admin)."
            ),
            inline=False
        )
        
        embed.set_footer(text="¡Disfruta de la música y la diversión con DJ Toad! ¡Croak!")

        await ctx.send(embed=embed)