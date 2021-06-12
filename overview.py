import scripts.setup as setup
from classes.downloader import Downloader
from classes.tracks import Track
from classes.queue_builder import QueueBuilder
from classes.player import SpotifyPlayer


if __name__ == '__main__':
    
    #setup which requires properly created 'credentials.txt' file
    setup.prep_env_from_file()
    username  = setup.get_spotify_username()

    #create downloader instance for user
    downloader = Downloader(username)

    #download desired track data by name
    track = Track(downloader.fetch_single_track_by_name('perfect ed sheeran'))

    #build queue
    queue_builder = QueueBuilder()
    raw_queue = queue_builder.create_basic_queue(track)

    #transform ids in queue into Tracks
    tmp = downloader.fetch_tracks_by_ids(raw_queue)['tracks']
    tracks_in_queue = list( map( lambda x: Track(x), tmp))

    #add tracks to real spotify queue
    player = SpotifyPlayer(username, downloader=downloader)
    for t in tracks_in_queue:
        player.add_track_to_queue(t)

    #show overview in debug
    print(f'\n\nQUEUE BASED ON {track} \n')
    for i, t in enumerate(tracks_in_queue):
        print(f'{i}: {t}')
    
