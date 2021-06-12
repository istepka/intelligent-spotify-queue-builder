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

      
    def pause(self) -> None:
        '''Pause current playback.'''
        self.spotify_client.pause_playback()

    def play(self) -> None:
        '''Play/Unpause current playback.'''
        self.spotify_client.start_playback()

    def add_track_to_queue(self, track:Track) -> None:
        '''Add track to queue.'''
        self.add_to_queue(track.get_id())

    def add_track_to_queue(self, _id:str) -> None:
        '''Add track to queue by id.'''
        self.spotify_client.add_to_queue(_id)

    def turn_on_repeat(self) -> None:
        '''Toggle repeat.'''
        self.spotify_client.repeat('track')
        
    def set_volume(self, volume) -> None:
        '''Set volume to value between 0-100.'''
        self.spotify_client.volume(volume)

    def next(self) -> None:
        '''Go to the next track in queue.'''
        self.spotify_client.next_track()

    def previous(self) -> None:
        '''Go back to the previous track.'''
        self.spotify_client.previous_track()

    

    
    
   
