# queues/queue_manager.py

from ytmusicapi import YTMusic

yt = YTMusic()

class QueueManager:
    def __init__(self):
        self.queues = {}

    def get_song_list(self, song_id, exclude_song_id=None):
        recommendations = yt.get_watch_playlist(song_id)['tracks']
        recommended_songs = []
        for track in recommendations:
            if 'videoId' in track:
                video_id = track['videoId']
                if video_id != exclude_song_id:
                    title = track.get('title', 'Sin título')
                    recommended_songs.append((video_id, title))
                if len(recommended_songs) >= 10:
                    break
        return recommended_songs

    def set_queue(self, guild_id, songs):
        self.queues[guild_id] = songs

    def add_song(self, guild_id, song):
        if guild_id not in self.queues:
            self.queues[guild_id] = []
        self.queues[guild_id].insert(0, song)

    def get_next_song(self, guild_id):
        if guild_id in self.queues and self.queues[guild_id]:
            return self.queues[guild_id].pop(0)
        return None

    def has_songs(self, guild_id):
        return guild_id in self.queues and bool(self.queues[guild_id])

# Instancia única de QueueManager
queue_manager = QueueManager()
