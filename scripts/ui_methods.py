from scripts import setup
from classes.downloader import Downloader
from classes.tracks import Track
from classes.trackData import TrackData
from classes.player import SpotifyPlayer
from classes.queue_builder import QueueBuilder



def search_for_track(name) -> TrackData:
    '''Search for the track'''
    #setup which requires properly created 'credentials.txt' file
    setup.prep_env_from_file()
    username  = setup.get_spotify_username()

    #create downloader instance for user
    downloader = Downloader(username)

    #TODO search in database and then eventually fetch from spoti
    #download desired track data by name
    track = Track(downloader.fetch_single_track_by_name(name))
    td = TrackData(id=track.id, name=track.name, artist=track.artist_name, album=track.album_name)
    return td


def build_que_by_track(name, params) -> list[str]:
    '''Builds queue based on track\n 
    Return list of `ids`'''
    assert params is dict, 'You should pass dictionary of queue parameters'

    username  = setup.get_spotify_username()
    downloader = Downloader(username)
    track = Track(downloader.fetch_single_track_by_name(name))
    qbuilder = QueueBuilder()
    queue = qbuilder.create_basic_queue(track)
    
    return queue
    

