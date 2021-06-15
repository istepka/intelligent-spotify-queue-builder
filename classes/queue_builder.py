from sklearn import neighbors
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import numpy as np 
import pandas as pd 
from classes.tracks import Track


class QueueBuilder:
    '''Build queue based on nearest neighbors.'''

    def __init__(self, dataset_path='./datasets/Tracks_14400dp_y1990-2021_full.csv') -> None:
        self.pd_data = pd.read_csv(dataset_path, index_col=0)

        self.labels = self.pd_data.keys()
        self.data =  self.pd_data.iloc[ :, 3::].to_numpy()
        self.neighbors_classifier = None
        self.k_neighbors = 12

        self.fit()
   


    def fit(self):
        '''Fit kNN classifier.'''
        self.normalized_data =  self.normalize_data()

        self.neighbors_classifier = NearestNeighbors(n_neighbors=self.k_neighbors, algorithm='ball_tree').fit(self.normalized_data)
        distances, indices = self.neighbors_classifier.kneighbors(self.normalized_data)

        print(distances, indices)

    def normalize_data(self) -> np.ndarray:
        '''Normalize dataset'''
        self.scaler = MinMaxScaler()
        self.scaler.fit(self.data)
        print(self.scaler.data_max_)
        print(self.scaler.data_min_) 
        return  self.scaler.transform(self.data)



    def find_neigbors(self, track:Track, n:int=4) -> np.ndarray:
        '''Find nearest tracks. \n
        Return numpy list of found ids.'''
        
        #['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness','acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'],
        track_array = np.array( track.convert_to_array_for_classification() )
        track_array = self.scaler.transform([track_array])
        print(track_array.shape)

        distances, neighbors = self.neighbors_classifier.kneighbors(track_array, n_neighbors=n, return_distance=True)
        print( 'distances:' ,distances )
        print('neighbor indexes:', neighbors)

        similar_tracks = list()
        for i in neighbors[0]:
            similar_tracks.append(  self.pd_data.iloc[i].Id )

        return similar_tracks



    def create_basic_queue(self, track: Track, length=5) -> list[str]:
        '''Create queue from track. \n
        Return list of ids.'''
        
        queue = list()
        current_track = track
        for i in range(length):
            candidates = self.find_neigbors(current_track, n=10)
            candidates = list(filter(lambda x: x != track.get_id() and x not in queue, candidates))
        
            queue.append( candidates[0] )
            

            current_track = Track(None, candidates[0])

        return queue






    def test_classifier(self):
        '''Test if classifier works properly.'''
        test_element = self.normalized_data[200]
        distances, neighbors = self.neighbors_classifier.kneighbors([test_element], n_neighbors=5, return_distance=True)
        print( 'distances:' ,distances )
        print('neighbor indexes:', neighbors)

        similar_tracks = list()
        for i in neighbors[0]:
            similar_tracks.append(  self.pd_data.iloc[i].Id )
        return similar_tracks