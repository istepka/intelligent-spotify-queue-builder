import os, sys, json, spotipy
from typing import Dict, List

#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts import setup



#Directory name where jsons are gonna be saved.  
JSON_CATALOG = 'data_jsons' 

class Downloader:
    '''Spotify data downloader.'''

    def __init__(self, user_id) -> None:
        #set environment variables if they don't already exist
        if os.getenv('SPOTIPY_CLIENT_ID') is None:
            setup.prep_env_from_file()

        #spotipy client setup 
        self.spotify = spotipy.Spotify(
            client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())
        
       
        #user's spotify unique name. Must match real user id
        self.user_id = user_id
          


    def write_json_to_file(self, filename, data ) -> None:
        '''Write data to file.'''
        assert '.' in filename, 'You should provide extension to your filename'

        #check if directory exists
        if not os.path.exists(f'./{JSON_CATALOG}'): 
            os.mkdir(f'./{JSON_CATALOG}')

        #save data
        with open(JSON_CATALOG + '/'+filename, 'w') as f:
            json.dump(data, f)


    def read_json_from_file(self, filename) -> Dict:
        '''Read json data from file.'''
        assert os.path.exists(f'./{JSON_CATALOG}/{filename}'), 'File does not exist'

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

    def fetch_track_additional_info(self, track_id) -> Dict:
        '''Download track additional audio features like loudness, energy, liveness etc.'''
        features = self.spotify.audio_features(tracks=[track_id])
        return features[0]

    def fetch_tracks_additional_info(self, tracks_id) -> Dict:
        '''Download tracks additional audio features like loudness, energy, liveness etc.\n
        Return list of jsons'''

        assert len(tracks_id) > 0, 'List should contain at least one entry'

        features = self.spotify.audio_features(tracks=tracks_id)
        return features
    

    def fetch_tracks_by_custom_query(self, query, records=10, type="track", offset=0) -> Dict:
        '''Download tracks found with custom query.'''
        result = self.spotify.search(query, limit=records, offset=offset, type=type)

        if not result: 
            return None
        else:
            return result

    def send_custom_query(self, query, records=10, type="track", offset=0) -> Dict:
        '''Download with custom query.'''
        return self.spotify.search(query, limit=records, offset=offset, type=type)

   
    def fetch_tracks_by_ids(self, id_list) -> Dict:
        '''Download tracks by list of ids'''
        return self.spotify.tracks(id_list)

    def fetch_track_by_id(self, _id) -> Dict:
        '''Download tracks by list of ids'''
        return self.spotify.track(_id)

    def get_artist(self, artist_id) -> Dict:
        '''Get artist info'''
        return self.spotify.artist(artist_id)
    
    def get_related_artists(self, artist_id) -> Dict:
        '''Get related artist'''
        return self.spotify.artist_related_artists(artist_id)

    def get_artist_top_tracks(self, artist_id, country='US') -> Dict:
        '''Get artist 10 top tracks in country'''
        return self.spotify.artist_top_tracks(artist_id, country)

    def get_genres_for_artist(self, artist_id) -> List[str]:
        '''Get artist genres'''
        return self.get_artist(artist_id)['genres']   

    def get_all_avaliable_genres(self) -> List[str]:
        '''Get all avaliable genres in spotify'''
        return self.spotify.recommendation_genre_seeds()['genres'] 
    
    def get_genres_for_artists(self, list_artist_id) -> List[str]:
        genres = []
        for e in self.spotify.artists(list_artist_id)['artists']:
            genres.append(e['genres'])
        return genres



if __name__ == '__main__':
    #set environmental variables required by authorization
    setup.prep_env_from_file('credentials.txt')
  

    #intantiate downloader for user
    downloader = Downloader(setup.get_spotify_username()) 

    #download single Rammstein track and write it to file 
    track = downloader.fetch_single_track_by_name('Sonne')
    downloader.write_json_to_file('rammstein_sonne.json', track)

    #read track id from saved json
    tack = downloader.read_json_from_file('rammstein_sonne.json')
    print( tack['id'] )

    a = downloader.fetch_track_additional_info(tack['id'])
    print(a.keys())
