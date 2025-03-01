# commands/other_commands.py

from discord.ext import commands
import os
import sys

class OtherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando '!dance1' para enviar un GIF de baile
    @commands.command()
    async def dance1(self, ctx):
        """Envía un divertido GIF de baile."""
        gif_url = "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGQweHk5MmpidXJrZDJidzcwbGR6ZzFpZTE1ZzFuMGs3emtwOHFmaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/pBDzxTAYdL6wRRdNTR/giphy.gif"
        await ctx.send(gif_url)
        await ctx.send("💃 ¡A bailar! ¡Croak!")

    # Comando '!dance2' para enviar otro GIF de baile
    @commands.command()
    async def dance2(self, ctx):
        """Envía otro divertido GIF de baile."""
        gif_url = "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaHBvc3h4ZmlqeWRhNmY1Y2wyaHFrY29jb3M1aDdpdjB6M3QzaWc3ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/gmUM6ag84nFnwaumx8/giphy.gif"
        await ctx.send(gif_url)
        await ctx.send("🕺 ¡Que siga la fiesta! ¡Croak!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def restart_bot(self, ctx):
        """Reinicia el bot en el servidor."""
        await ctx.send("♻️ Reiniciando el bot... ¡Croak!")
        os.execv(sys.executable, ['python'] + sys.argv)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def shutdown_bot(self, ctx):
        """Apaga completamente el bot."""
        await ctx.send("🔌 Apagando el bot... ¡Croak!")
        await self.bot.close()