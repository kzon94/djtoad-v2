import discord
from discord.ext import commands
from ytmusicapi import YTMusic
from utils.audio_utils import fetch_audio_info
from utils.voice_utils import connect_to_voice
import asyncio
import random
import os

yt = YTMusic()

class TrivialCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scores = {}
        self.active_games = {}
        self.stop_game = {}

    @commands.command()
    async def trivial(self, ctx):
        """Inicia un juego de trivia musical con 7 rondas."""
        if ctx.guild.id in self.active_games:
            await ctx.send("⚠️ Ya hay un trivial en curso en este servidor. ¡Croak!")
            return

        self.active_games[ctx.guild.id] = True
        self.scores[ctx.guild.id] = {}
        self.stop_game[ctx.guild.id] = False

        vc = await connect_to_voice(ctx)
        if not vc:
            del self.active_games[ctx.guild.id]
            return

        # Ruta a la canción de introducción en la carpeta media
        intro_song_path = os.path.join('media', 'trivia_intro.mp3')

        # Reproducir música de introducción
        if os.path.exists(intro_song_path):
            vc.play(discord.FFmpegPCMAudio(intro_song_path))
        else:
            await ctx.send("⚠️ No se encontró la canción de introducción en la carpeta 'media'. ¡Croak!")

        embed = discord.Embed(
            title="🎤 ¡Bienvenido al Trivial Musical!",
            description=(
                "¡Hola, soy DJ Toad! 🐸🎶\n\n"
                "**Prepárate para un reto musical de 7 rondas. 🎵**\n\n"
                "1️⃣ **Escribe un género musical en el chat.**\n\n"
                "2️⃣ **Escucharás un fragmento de una canción.**\n\n"
                "3️⃣ **Responde solo con el título de la canción.**\n\n"
                "4️⃣ **¡Gana ranipuntos 🐸 y compite por la victoria! 🏆**"
            ),
            color=discord.Color.green()
        )
        embed.set_thumbnail(url="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaHBvc3h4ZmlqeWRhNmY1Y2wyaHFrY29jb3M1aDdpdjB6M3QzaWc3ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/gmUM6ag84nFnwaumx8/giphy.gif")
        await ctx.send(embed=embed)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("⏳ No recibí ninguna respuesta. Juego cancelado. ¡Croak!")
            del self.active_games[ctx.guild.id]
            return

        genre = msg.content.strip()

        # Detener la música de introducción si aún se está reproduciendo
        if vc.is_playing():
            vc.stop()
        await asyncio.sleep(1)  # Esperar 1 segundo

        await ctx.send(f"🔍 Creando un Trivial de {genre}... ¡Croak!\n")

        search_results = yt.search(genre, filter='songs')
        if not search_results:
            await ctx.send("❌ No encontré canciones para este estilo. ¡Croak!")
            del self.active_games[ctx.guild.id]
            return

        used_songs = set()
        
        for round_num in range(1, 8):  # 7 rondas
            if self.stop_game[ctx.guild.id]:
                await ctx.send("🚫 Trivial detenido manualmente. ¡Croak!")
                break

            song = None
            while not song or song['title'] in used_songs:
                song = random.choice(search_results)
            used_songs.add(song['title'])
            song_id = song['videoId']
            title = song['title']
            artist = song.get('artists', [{'name': 'Desconocido'}])[0]['name']
            url, _ = await fetch_audio_info(song_id)

            if not url:
                await ctx.send(f"❌ No pude obtener audio para {title}. ¡Croak!")
                continue

            start_time = random.randint(0, 40)
            await ctx.send(f"\n\n🎵 **Ronda {round_num}/7:** ¡Adivina la canción! Responde escribiendo el título en el chat.")
            vc.play(discord.FFmpegPCMAudio(url, options='-vn', before_options=f'-ss {start_time} -t 20'))

            def answer_check(m):
                return m.channel == ctx.channel and title.lower() in m.content.lower()

            try:
                answer = await self.bot.wait_for("message", check=answer_check, timeout=20.0)
                player = answer.author.name
                self.scores[ctx.guild.id][player] = self.scores[ctx.guild.id].get(player, 0) + 1
                await ctx.send(f"✅ ¡Correcto! {player} gana un ranipunto. 🎉 La canción era **{title}** de **{artist}**.\n")
                vc.stop()
            except asyncio.TimeoutError:
                await ctx.send(f"\n❌ Tiempo agotado. La respuesta correcta era: **{title}** de **{artist}**. ¡Croak!\n")
            
            await asyncio.sleep(4)

        # Indicar al ganador y mostrar leaderboard final
        await self.show_winner(ctx)
        del self.active_games[ctx.guild.id]

    @commands.command()
    async def trivial_stop(self, ctx):
        """Detiene el trivial en curso."""
        if ctx.guild.id in self.active_games:
            self.stop_game[ctx.guild.id] = True
            await ctx.send("🛑 Trivial detenido. ¡Croak!")
        else:
            await ctx.send("⚠️ No hay un trivial en curso. ¡Croak!")

    @commands.command()
    async def leaderboard(self, ctx):
        """Muestra el leaderboard actual."""
        await self.show_scores(ctx)

    async def show_scores(self, ctx):
        """Muestra los puntajes actuales del juego."""
        scores = self.scores.get(ctx.guild.id, {})
        if not scores:
            await ctx.send("\n🔹 No hay ranipuntos 🐸 registrados. ¡Croak!")
            return

        leaderboard = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        message = "\n🐸 **Ranipuntos actuales:**\n"
        for player, points in leaderboard:
            message += f"- {player}: {points} puntos\n"

        await ctx.send(message)

    async def show_winner(self, ctx):
        """Indica al ganador y muestra el leaderboard final."""
        scores = self.scores.get(ctx.guild.id, {})
        if not scores:
            await ctx.send("🔹 No hay ranipuntos registrados. ¡Croak!")
            return

        leaderboard = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        max_points = leaderboard[0][1]
        winners = [player for player, points in leaderboard if points == max_points]

        if len(winners) == 1:
            message = f"🎉 **¡Felicidades {winners[0]}!** Eres el ganador con {max_points} puntos. 🏆\n"
        else:
            winners_list = ", ".join(winners)
            message = f"🤝 **¡Tenemos un empate entre {winners_list}!** Cada uno con {max_points} puntos. 🏆\n"

        await ctx.send(message)
        await self.show_scores(ctx)