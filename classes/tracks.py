import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.downloader import Downloader
from scripts import setup
from typing import Dict



class Track:
    '''Track informations and processing.'''

    def __init__(self, track: Dict) -> None:
        assert len( track.items() ) > 0, 'Track dictionary can\'t be empty'
        
        #init basic properties
        self.id = track['id']
        self.uri = track['uri']
        self.external_url = track['external_urls']['spotify'] 
        self.name = track['name']
        self.artist_name = track['artists'][0]['name']
        self.artist_id = track['artists'][0]['id']
        self.album_name = track['album']['name']
        self.album_id = track['album']['id']

        #init aditional properties
        self.audio_features = track['audio_features'] if 'audio_features' in track else None  

    def __str__(self) -> str:
        return f'{self.artist_name} song \'{self.name}\' from album \'{self.album_name}\''

    def __repr__(self) -> str:
        return f'{self.artist_name} song \'{self.name}\' from album \'{self.album_name}\''

    def get_id(self) -> int:
        return self.id

    def get_uri(self) -> str:
        return self.uri
    def set_additional_info(self, features) -> None:
        self.audio_features = features

    def convert_to_array_for_classification(self) -> list:
        keys = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness','acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
        return [ self.audio_features[k]  for k in keys ]

    def load_additional_song_data(self, downloader=None) -> None:
        '''Download and load song characteristics like loudness, energy, liveness etc.'''
        if not downloader:
            downloader= Downloader(setup.get_spotify_username())  
        
        self.audio_features = downloader.fetch_track_additional_info(self.id)


    def save(self, filename='', downloader=None) -> None:
        '''Save track to file. By default files are named by artist and song name.'''
        if filename == '':
            filename = f'{self.artist_name}_{self.name}.json'
        if not downloader:
            downloader= Downloader(setup.get_spotify_username()) 


        dic = dict()

        try:
            #get currently saved data
            dic = downloader.read_json_from_file(filename)
        except:
            dic['id'] = self.id 
            dic['uri'] = self.uri
            dic['external_url']= self.external_url 
            dic['name']  = self.name 
            dic['artist_name'] = self.artist_name 
            dic['artist_id'] = self.artist_id 
            dic['album_name']= self.album_name  
            dic['album_id'] = self.album_id 
            dic['audio_features'] = self.audio_features



        #save
        downloader.write_json_to_file(filename, dic)








if __name__ == '__main__':
    d = Downloader(setup.get_spotify_username())
   
    sonne = Track(d.read_json_from_file('sonne.json'))
    sonne.load_additional_song_data(d)
    sonne.save()