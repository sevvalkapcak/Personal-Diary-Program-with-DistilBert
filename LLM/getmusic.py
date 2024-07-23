import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

class MusicRecommendation:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='72bddd956a82499fa51a51bd2d6a1ceb',
                                                            client_secret='e80dacd16db84b4d830025398a685424',
                                                            redirect_uri='http://localhost:8888/callback',
                                                            scope='playlist-modify-public'))

    def get_random_track_from_playlist(self, emotion):
        mood_playlists = {
            'sadness': 'https://open.spotify.com/playlist/37i9dQZF1DXbrUpGvoi3TS?si=17fdae277c0d4018',
            'joy': 'https://open.spotify.com/playlist/37i9dQZF1DX9XIFQuFvzM4?si=1cc04be28e904f1a',
            'love': 'https://open.spotify.com/playlist/37i9dQZF1DWVf1Phr4ZVgO?si=4aec072e2e7541ca',
            'anger': 'https://open.spotify.com/playlist/37i9dQZF1DWZVAVMhIe3pV?si=f712325f58f0412b',
            'fear': 'https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6?si=8bbd7a195c8a48a9',
            'surprise': 'https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0?si=88c2597081b1421f'
        }

        playlist_name = mood_playlists.get(emotion, 'Happy Hits')
        playlist_uri = self.sp.user_playlist(self.sp.me()['id'], playlist_name)['uri']
        tracks = self.sp.playlist_tracks(playlist_uri)['items']

        if not tracks:
            return None  # Eğer listede şarkı yoksa None döndür

        random_track = random.choice(tracks)
        track_uri = random_track['track']['uri']

        return f"https://open.spotify.com/track/{track_uri.split(':')[2]}"
