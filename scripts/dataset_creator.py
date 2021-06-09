import pandas as pd
import numpy as np 
from classes.downloader import Downloader
from scripts import setup
from classes.tracks import Track


def create_dataset(starting_year=2021, how_many_years=32, tracks_per_year=200):     


    downloader = Downloader(setup.get_spotify_username())

    ITERATIONS = how_many_years
    TRACKS_PER_YEAR = tracks_per_year
    RECORDS_PER_REQUEST = 50
    YEAR = 2021
    raw_tracks = list()
    


    def download_base_data():
        '''Build dataframe with tracks base info'''
        nonlocal raw_tracks, YEAR
        for i in range(ITERATIONS):
            for k in range(int(TRACKS_PER_YEAR/RECORDS_PER_REQUEST) + 1):
                query=f'year:{YEAR}'
                data = downloader.fetch_tracks_by_custom_query(query, records=RECORDS_PER_REQUEST,                          
                type='track', offset=k*RECORDS_PER_REQUEST)
                
                tmp_tracks = list( map( lambda x: Track(x), data['tracks']['items'] ) )
                raw_tracks += list( map( lambda x: (x.id, YEAR ,x.name),  tmp_tracks))

            YEAR -= 1


        print('Downloaded:', len(raw_tracks))
        return raw_tracks


    def download_features(data):
        '''Extend dataframe with additional features info.'''
        raw_jsons = list()

        #Download additional stuff
        for i in range(0, len(data), 100):
            raw_jsons += downloader.fetch_tracks_additional_info(data['Id'][i : i+100])
            print(i, raw_jsons[i])

        print(len(raw_jsons))

        r = raw_jsons[:]
        for item in r: 
            for key in item.keys():
                item[key] =   item[key] 

        raw_features_df = pd.DataFrame.from_dict(r)
        

        features_df = raw_features_df.iloc[:, 0:11]
    

        merged_df = pd.concat([data, features_df], axis=1)
        return merged_df
    


    raw_tracks = download_base_data()
   

    #Build proper dataframe
    data = pd.DataFrame( { 'Name': [i[2] for i in raw_tracks],
    'Id': [i[0] for i in raw_tracks],
    'Year': [i[1] for i in raw_tracks]
    })

    
    #merge additional features
    merged_df = download_features(data)


    #save to file
    csv_name = f'./datasets/Tracks_{data.shape[0]}dp_y' + str(data['Year'].min()) + '-' +  str(data['Year'].max())+  '_full.csv' 
    merged_df.to_csv(csv_name)