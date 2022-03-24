from scripts import setup
from classes.downloader import Downloader
from classes.tracks import Track
from classes.trackData import TrackData
from classes.player import SpotifyPlayer
from classes.queue_builder import QueueBuilder



def search_for_track(search_string, type) -> TrackData:
    '''
    Search in online db for the track.

    Parameters:
        `search_string`: it can be either track *name* or *id*
        `type`: 'name' or 'id' depending of the search string type 
    '''
    #setup which requires properly created 'credentials.txt' file
    setup.prep_env_from_file()
    username  = setup.get_spotify_username()

    #create downloader instance for user
    downloader = Downloader(username)

    #TODO search in database and then eventually fetch from spoti
    #download desired track data by name
    if type == 'name':
        track = Track(downloader.fetch_single_track_by_name(search_string))
    else:
        track = Track(downloader.fetch_track_by_id(search_string))
    td = TrackData(id=track.id, name=track.name, artist=track.artist_name, album=track.album_name)
    return td


def build_que_by_track(name, params, qb=None) -> list[str]:
    '''Builds queue based on track\n 
    Return list of `ids`'''
    assert params is not dict or params is None, 'You should pass dictionary of queue parameters'
    assert len(name) > 3, 'Song name should be at least 3 characters long'

    username  = setup.get_spotify_username()
    downloader = Downloader(username)

   
    track = Track(downloader.fetch_single_track_by_name(name))

    if qb is None:
        qbuilder = QueueBuilder()
    else:
        qbuilder = qb

    if 'length' in params:
        queue = qbuilder.create_basic_queue(track, length=params['length'])
    else:
        queue = qbuilder.create_basic_queue(track)
    
    return queue

def add_tracks_to_real_queue(track_ids: list[str]) -> None:
    player = SpotifyPlayer(setup.get_spotify_username())
    
    for _id in track_ids:
        player.add_track_to_queue_by_id(_id)

    print(f'Added {len(track_ids)} track to your real spotify queue')
    
    

