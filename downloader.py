import os, json, spotipy
from typing import Dict
import setup

#Directory name where jsons are gonna be saved.  
JSON_CATALOG = 'data_jsons' 

class Downloader:
    '''Spotify data downloader.'''

    def __init__(self, user_id) -> None:
        os.environ['SPOTIPY_CLIENT_ID'] = "14ec728c0d5b476a8389811d474a7172"
        os.environ['SPOTIPY_CLIENT_SECRET'] = "12ec47de2b334c0984299a30e721557b"

        self.spotify = spotipy.Spotify(
            client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())
        
        self.user_id = user_id
          


    def write_json_to_file(self, filename, data ) -> None:
        '''Write data to file.'''
        assert '.' in filename, 'You should provide extension to your filename'

        with open(JSON_CATALOG + '/'+filename, 'w') as f:
            json.dump(data, f)

    def read_json_from_file(self, filename) -> Dict:
        '''Read json data from file.'''
        with open(JSON_CATALOG + '/' + filename, 'r') as f:
            return json.load(f)


    def fetch_all_user_playlists(self) -> Dict:
        '''Download all user's playlists (json).'''
        return self.spotify.user_playlists(self.user_id)
            
    def fetch_single_track_by_name(self, name) -> Dict:
        '''Download track by its name (json). \n 
        e.g. \'Sonne\' '''
        assert len(name) > 3, "Track name should have at least 3 characters" 
        
        result = self.spotify.search(q=f'{name}', limit=1, type='track')
        
        #Strip raw query result to single track data
        if result: 
            return result['tracks']['items'][0]

        return None






if __name__ == '__main__':
    
    #set environmental variables required by authorization
    setup.prep_env_from_file('credentials.txt')

    #intantiate downloader for user
    downloader = Downloader('swagnacy') 

    #download single Rammstein track and write it to file 
    track = downloader.fetch_single_track_by_name('Sonne')
    downloader.write_json_to_file('sonne.json', track)

    #read track id from saved json
    tack = downloader.read_json_from_file('sonne.json')
    print( tack['id'] )
