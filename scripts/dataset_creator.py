from typing import List
import pandas as pd
import numpy as np
import os
from pandas.core.frame import DataFrame 
from classes.downloader import Downloader
from scripts import setup
from classes.tracks import Track

class DatasetCreator():
    '''Dataset builder class.'''
    def __init__(self, downloader=None) -> None:
        self.downloader = downloader if downloader else Downloader(setup.get_spotify_username())


    def combine_datasets(self, from_year=1970, to_year=2021, string_in_filename="Tracks") -> str: 
        '''Combine smaller datasets created for specific years into the bigger one.
        Return name of combined file.'''

        #create all valid dates
        dates = [f'{d}-{d}_full' for d in range(from_year, to_year+1)]
        
        #filter directory to only desired files
        filenames =  list(filter( 
            lambda x:  string_in_filename in x 
                and any([d in x for d in dates])  
            ,os.listdir('./datasets/datasets_batch')
            ))

        print('first: ', filenames[0], '\nlast: ',  filenames[len(filenames)-1])

        #concatenate only if there is something to merge
        if filenames:
            #concatenate
            frames = list()
            for f in filenames:
                frames.append(pd.read_csv(f'./datasets/datasets_batch/{f}', index_col=0))
                merged_df = pd.concat(frames,ignore_index=True)

            #save concatenated file
            csv_name_raw = f'./datasets/TracksCombined_{len(merged_df)}datapoints_{from_year}-{to_year}.csv' 
            merged_df.to_csv(csv_name_raw)
            return csv_name_raw

        else:
            print("There is no matching files in dataset directory")
            return ""

    def create_dataset(self, starting_year=2021, how_many_years=32, tracks_per_year=200) -> str:     
        '''Create full dataset. \n
        Return name of the dataset.'''
     
        ITERATIONS = how_many_years
        TRACKS_PER_YEAR = tracks_per_year
        RECORDS_PER_REQUEST = 50
        YEAR = starting_year
        raw_tracks = list()

        def download_base_data():
            '''Build dataframe with tracks base info'''
            nonlocal raw_tracks, YEAR
            for i in range(ITERATIONS):
                for k in range(int(TRACKS_PER_YEAR/RECORDS_PER_REQUEST) + 1):
                    #fetch data in samples
                    query=f'year:{YEAR}'
                    data = self.downloader.fetch_tracks_by_custom_query(query, records=RECORDS_PER_REQUEST,                          
                                type='track', offset=k*RECORDS_PER_REQUEST + 1)
                    #combine to larger dataset
                    tmp_tracks = list( map( lambda x: Track(x), data['tracks']['items'] ) )
                    raw_tracks += list( map( lambda x: (x.id, YEAR ,x.name, x.artist_name, x.artist_id),  tmp_tracks))

                YEAR -= 1
                print(YEAR, 'downloaded')

            print('Downloaded:', len(raw_tracks))
            return raw_tracks


        def download_features(data: DataFrame):
            '''Extend dataframe with additional features info.'''
            raw_jsons = list()

            #Download additional stuff
            for i in range(0, len(data), 100):
                raw_jsons += self.downloader.fetch_tracks_additional_info(data['Id'][i : i+100])
                print(i, raw_jsons[i])

            print(len(raw_jsons))

            to_del = 0
            #search for bad rows
            none_rows = set()
            for i, r in enumerate(raw_jsons):
                if not r or type(r) is not dict or len(r) != len(raw_jsons[0]):
                    print('none', i, r)
                    none_rows.add(i)
                    to_del+=1
                else:
                    try:
                        r.keys()
                    except:
                        print(f'BAD {i}: {type(r)}, {r}')
                        none_rows.add(i)
                        to_del+=1
            print(f'To delete {to_del}')

            #remove bad rows from data and raw_data
            data.drop(index=list(none_rows), inplace=True)
            for i in none_rows:
                del raw_jsons[i]
            print(f'After deletion {len(raw_jsons)}')
            
            #print(raw_jsons)
            #extract features
            raw_features_df = pd.DataFrame.from_records(raw_jsons)
            print('Done')
            features_df = raw_features_df[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                                            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                                            'duration_ms']]
            print(raw_features_df.columns)

            #merge basic data with features
            merged_df = pd.concat([data, features_df], axis=1)
            return merged_df
        

        raw_tracks = download_base_data()
        print(raw_tracks)
    
        #Build proper dataframe
        data = pd.DataFrame( { 'Name': [i[2] for i in raw_tracks],
        'Id': [i[0] for i in raw_tracks],
        'Year': [i[1] for i in raw_tracks],
        'Artist': [i[3] for i in raw_tracks],
        'Artist_id': [i[4] for i in raw_tracks]
        })

        #save basic data to file
        csv_name_raw = f'./datasets/datasets_batch/Tracks_{len(raw_tracks)}dp_y' + str(data['Year'].min()) + '-' +  str(data['Year'].max())+  '_raw.csv' 
        data.to_csv(csv_name_raw, index=False)

        #merge additional features
        merged_df = download_features(data)

        #save to file
        csv_name = f'./datasets/datasets_batch/Tracks_{len(raw_tracks)}dp_y' + str(data['Year'].min()) + '-' +  str(data['Year'].max())+  '_full.csv' 
        merged_df.to_csv(csv_name, index=False)

        return csv_name