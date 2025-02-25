# utils/audio_utils.py

import asyncio
import yt_dlp as youtube_dl

async def fetch_audio_info(video_id):
    """Obtiene la información del audio antes de reproducirlo."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
    }
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        data = await asyncio.to_thread(
            youtube_dl.YoutubeDL(ydl_opts).extract_info,
            url,
            download=False
        )
        return data['url'], data.get('title', 'Sin título')
    except Exception as e:
        return None, f"❌ Error obteniendo audio: {e}. ¡Croak!"
