import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from classes.tracks import Track
from classes.downloader import Downloader



class SpotifyPlayer:
    '''Player which can schedule and play music on your account.'''


    def __init__(self, spotify_username, downloader=None) -> None:
        self.downloader = downloader if downloader else Downloader(spotify_username)
        self.username = spotify_username 

        scope = 'user-modify-playback-state'
        self.spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

      
    def pause(self):
        self.spotify_client.pause_playback()

    def play(self):
        self.spotify_client.start_playback()

    def add_track_to_queue(self, track:Track):
        self.add_to_queue(track.get_id())

    def add_to_queue(self, _id):
        self.spotify_client.add_to_queue(_id)

    def turn_on_repeat(self):
        self.spotify_client.repeat('track')
        
    def set_volume(self, volume):
        self.spotify_client.volume(volume)

    def next(self):
        self.spotify_client.next_track()

    def previous(self):
        self.spotify_client.previous_track()

    # def get_current_playback(self):
    #     print( self.spotify_client.current_playback() )

    
    
   
