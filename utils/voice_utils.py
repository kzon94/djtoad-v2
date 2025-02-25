# utils/voice_utils.py

async def connect_to_voice(ctx):
    if not ctx.author.voice:
        await ctx.send("❌ Debes estar en un canal de voz. ¡Croak!")
        return None

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        return await voice_channel.connect()
    elif ctx.voice_client.channel != voice_channel:
        return await ctx.voice_client.move_to(voice_channel)
    return ctx.voice_client
