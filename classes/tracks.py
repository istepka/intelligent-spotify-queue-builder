from logging import exception
import sys, os
from turtle import down

import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.downloader import Downloader
from scripts import setup
from typing import Dict



class Track:
    '''Track informations and processing.'''

    def __init__(self, track: Dict=None, track_id=None) -> None:
        assert track != None or track_id != None, 'You must pass at least one parameter'
        
        if track:
            self.init_values(track)
        elif track_id:
            track = self.load_basic_song_data(track_id)
            self.init_values(track)
        else:
            exception('Cannot initialize Track')
            

       

    def init_values(self, track:Dict):
        '''Initialize basic Track properties.'''
        #init basic properties
        self.id = track['id']
        self.uri = track['uri']
        self.external_url = track['external_urls']['spotify'] 
        self.name = track['name']
        self.artist_name = track['artists'][0]['name']
        self.artist_id = track['artists'][0]['id']
        self.album_name = track['album']['name']
        self.album_id = track['album']['id']
        self.year = int(track['album']['release_date'][0:4])
        self.explicit = track['explicit']
        #self.genres = track['artists'][0]['genres']

        #init aditional properties
        self.audio_features = track['audio_features'] if 'audio_features' in track else None  

    def __str__(self) -> str:
        return f'{self.artist_name} song \'{self.name}\' from album \'{self.album_name}\''

    def __repr__(self) -> str:
        return f'{self.artist_name} song \'{self.name}\' from album \'{self.album_name}\''

    def get_id(self) -> int:
        '''Get track id.'''
        return self.id

    def get_uri(self) -> str:
        '''Get track uri.'''
        return self.uri
    def set_additional_info(self, features) -> None:
        '''Set track additional audio features property.'''
        self.audio_features = features

    def convert_to_array_for_classification(self) -> list:
        '''
        Convert audio features to array ready to pass into classification method.
        
        Return elementwise list of necessary properties. 
        '''
        if not self.audio_features:
            self.load_additional_song_data()
        keys = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness','acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
        return [self.year] + [ self.audio_features[k]  for k in keys ] + [self.genre]

    def get_dataframe_for_classification(self) -> pd.DataFrame:
        if not self.audio_features:
            self.load_additional_song_data()
        keys = ['Year', 'danceability', 'energy', 'key', 'loudness', 'mode', \
            'speechiness','acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'genre', 'duration_ms']
        
        df = pd.DataFrame(columns=keys)
        df['Year'] = [self.year]
        df['genre'] = [self.genre]
        for k in keys:
            if k in self.audio_features:
                df[k] = self.audio_features[k]

        df['is_long'] = df['duration_ms'] > df['duration_ms'].quantile(0.90)
        df['is_short'] = df['duration_ms'] < df['duration_ms'].quantile(0.05)

        df['under70s'] = df['Year'] < 1970
        df['70s'] = (df['Year'] >= 1970) & (df['Year'] < 1980)
        df['80s'] = (df['Year'] >= 1980) & (df['Year'] < 1990)
        df['90s'] = (df['Year'] >= 1990) & (df['Year'] < 2000)
        df['00s'] = (df['Year'] >= 2000) & (df['Year'] < 2010)
        df['10s'] = (df['Year'] >= 2010) & (df['Year'] < 2020)
        df['20s'] = df['Year'] >= 2020 

        sel_genres = ['rock', 'metal', 'classical', 'progressive', 'pop', 'r&b', 'hop',\
             'latin', 'country', 'electr', 'punk', 'dance']
        for s in sel_genres:
            df[s] = df['genre'].apply(lambda x: s in str.lower(x))

        df = df.drop(['Year', 'genre', 'duration_ms'], axis=1)

        return df    
             

    def load_additional_song_data(self, downloader=None) -> None:
        '''Download and load song characteristics like loudness, energy, liveness etc.'''
        if not downloader:
            downloader= Downloader(setup.get_spotify_username())  
        
        self.audio_features = downloader.fetch_track_additional_info(self.id)
        self.genres = downloader.get_genres_for_artist(self.artist_id)
        
        if len(self.genres) > 0:
            self.genre = self.genres[0]
        else:
            self.genre = 'none'

    def load_basic_song_data(self, _id, downloader=None) -> Dict:
        '''
        Download track's basic data.  

        Return track in dictionary format.
        '''
        if not downloader:
            downloader= Downloader(setup.get_spotify_username()) 
        
        return downloader.fetch_track_by_id(_id)


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
   
    sonne = Track(d.fetch_single_track_by_name('sonne'))
    sonne.load_additional_song_data(d)
    print(sonne.convert_to_array_for_classification())
    print(sonne)
    print(d.fetch_single_track_by_name('sonne'))
    sonne.load_additional_song_data(d)
    print(sonne.audio_features)
    print(sonne.year)
    #sonne.save()