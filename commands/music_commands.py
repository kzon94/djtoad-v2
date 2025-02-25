# commands/music_commands.py

import discord
from discord.ext import commands
from ytmusicapi import YTMusic
from utils.audio_utils import fetch_audio_info
from utils.voice_utils import connect_to_voice
from queues.queue_manager import queue_manager
import asyncio

yt = YTMusic()

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando '!play' para reproducir una canción
    @commands.command()
    async def play(self, ctx, *, song_name):
        vc = await connect_to_voice(ctx)
        if not vc:
            return

        await ctx.send(f"🔍 Buscando '{song_name}' y canciones recomendadas... ¡Croak!")

        # Buscar la canción y obtener su ID
        search_results = yt.search(song_name, filter='songs')
        if not search_results or 'videoId' not in search_results[0]:
            await ctx.send("❌ No se encontraron resultados. ¡Croak!")
            return
        song_id = search_results[0]['videoId']

        # Obtener la URL y el título de la canción
        url, title = await fetch_audio_info(song_id)
        if not url:
            await ctx.send(title)  # Mensaje de error
            return

        if vc.is_playing():
            vc.stop()

        # Reproducir la canción
        vc.play(discord.FFmpegPCMAudio(url), after=lambda e: self.bot.loop.create_task(self.play_next_song(ctx)))

        vc.source.title = title  # Guardar el título de la canción actual
        await ctx.send(f"🎶 Reproduciendo: {title}. ¡Croak!")

        # Obtener canciones recomendadas y actualizar la cola
        await ctx.send("⏳ Obteniendo canciones recomendadas... ¡Croak!")
        recommended_songs = queue_manager.get_song_list(song_id, exclude_song_id=song_id)
        queue_manager.set_queue(ctx.guild.id, recommended_songs)
        await ctx.send("✅ Lista de reproducción descargada exitosamente. ¡Croak!")

    # Función para reproducir la siguiente canción en la cola
    async def play_next_song(self, ctx):
        vc = ctx.voice_client
        if not vc:
            return

        next_song = queue_manager.get_next_song(ctx.guild.id)
        if next_song:
            video_id, title = next_song
            url, _ = await fetch_audio_info(video_id)
            if not url:
                await ctx.send(f"❌ Error al obtener el audio para {title}. ¡Croak!")
                return await self.play_next_song(ctx)

            vc.play(discord.FFmpegPCMAudio(url), after=lambda e: self.bot.loop.create_task(self.play_next_song(ctx)))
            vc.source.title = title
            await ctx.send(f"🎶 Reproduciendo: {title}. ¡Croak!")
        else:
            await ctx.send("🚫 No hay más canciones en la cola. Desconectando... ¡Croak!")
            await vc.disconnect()

    # Comando '!add' para añadir una canción al inicio de la cola
    @commands.command()
    async def add(self, ctx, *, song_name):
        """Añade una canción al inicio de la cola de reproducción."""
        await ctx.send(f"🔍 Buscando '{song_name}' en YouTube Music... ¡Croak!")

        # Buscar la canción
        search_results = yt.search(song_name, filter='songs')
        if not search_results or 'videoId' not in search_results[0]:
            await ctx.send("❌ No se encontraron resultados. ¡Croak!")
            return
        song_id = search_results[0]['videoId']
        title = search_results[0].get('title', 'Sin título')

        # Añadir la canción al inicio de la cola
        queue_manager.add_song(ctx.guild.id, (song_id, title))
        await ctx.send(f"✅ '{title}' ha sido añadida al inicio de la cola de reproducción. ¡Croak!")

    # Comando '!next' para saltar a la siguiente canción
    @commands.command()
    async def next(self, ctx):
        """Salta a la siguiente canción en la cola."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭️ Saltando a la siguiente canción... ¡Croak!")
        else:
            await ctx.send("🚫 No hay una canción reproduciéndose actualmente. ¡Croak!")

    # Comando '!list' para mostrar la cola de reproducción actual
    @commands.command()
    async def list(self, ctx):
        """Muestra la canción actual y la lista de canciones en la cola de reproducción."""
        message = ""
        vc = ctx.voice_client
        if vc and vc.is_playing() and hasattr(vc.source, 'title'):
            current_song = vc.source.title
            message += f"🎶 **Canción sonando:** {current_song}\n\n"
        else:
            message += "ℹ️ **No hay una canción reproduciéndose actualmente. ¡Croak!**\n\n"
    
        queue = queue_manager.get_queue(ctx.guild.id)
        if queue:
            message += "**🎵 Cola de reproducción:**\n"
            for index, (video_id, title) in enumerate(queue, start=1):
                message += f"{index}. {title}\n"
        else:
            message += "ℹ️ La cola de reproducción está vacía. ¡Croak!"
    
        await ctx.send(message)

    # Comando '!pause' para pausar la reproducción
    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Reproducción pausada. ¡Croak!")
        else:
            await ctx.send("🚫 No hay una canción reproduciéndose para pausar. ¡Croak!")

    # Comando '!resume' para reanudar la reproducción
    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Reproducción reanudada. ¡Croak!")
        else:
            await ctx.send("🚫 No hay una canción pausada para reanudar. ¡Croak!")

    # Comando '!stop' para detener la reproducción y desconectar al bot
    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            queue_manager.clear_queue(ctx.guild.id)
            await ctx.send("⏹️ Bot desconectado y cola borrada. ¡Croak!")
        else:
            await ctx.send("🚫 No estoy conectado a un canal de voz. ¡Croak!")
