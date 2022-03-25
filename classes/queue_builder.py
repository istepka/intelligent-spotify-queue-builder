import pickle
from typing import List
from scipy.sparse import data
from sklearn import neighbors
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import numpy as np 
import pandas as pd 
from classes.tracks import Track
from sklearn import cluster, preprocessing, metrics

SEED = 1232

class QueueBuilder:
    '''Build queue based on nearest neighbors.'''
    np.random.seed(SEED)

    def __init__(self, dataset_path='./datasets/72k.csv') -> None:
        try:
            self.pd_data = pd.read_csv('new_format1.csv').dropna()
        except:
            self.pd_data = pd.read_csv(dataset_path)#.drop(['Unnamed: 0'], axis=1)
        print(self.pd_data.info())

        self.pd_data.dropna(axis=0, inplace=True)
        print(self.pd_data.columns)

        self.columns_to_drop = ['Id']#['Name', 'Id', 'Artist', 'Artist_id', 'duration_ms'] # = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                            #'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                             #               'duration_ms']

        self.labels = self.pd_data.keys()
        self.data =  self.pd_data.drop(self.columns_to_drop, axis=1).to_numpy()
        self.neighbors_classifier = None
        self.k_neighbors = 12

        #self.__prep_data()
        np.random.seed(SEED)
        self.normalized_data =  self.normalize_data()
        print("Normalized data:", self.normalized_data.shape)

        #if it is not already clustered
        try:
            with open("modelKMEANS.pkl", "rb") as f:
                self.clustering_model = pickle.load(f)
            self.pd_data['cluster'] = self.clustering_model.predict(self.normalized_data)
        except:
            np.random.seed(SEED)
            self.pd_data['cluster'] = self.cluster_kmeans(X=self.normalized_data)
            with open("modelKMEANS.pkl", "wb") as f:
                pickle.dump(self.clustering_model, f)
            print('Done clustering')
        

        self.pd_data.to_csv('clustered.csv')

   
    def __prep_data(self):
        '''Remove NaNs'''
        self.data = self.data[~np.isnan(self.data).any(axis=1), :] 
        print("Input data: ", self.data.shape)


    def fit(self):
        '''Fit kNN classifier.'''
        print(f'Starting kNN fit')
        # try:
        #     if self.neighbors_classifier is None: 
        #         with open("knn.pkl", "rb") as f:
        #             self.neighbors_classifier = pickle.load(f)
        # except:
        np.random.seed(SEED)
        self.neighbors_classifier = NearestNeighbors(n_neighbors=self.k_neighbors, 
                                        algorithm='ball_tree').fit(self.normalized_data)
            # with open("knn.pkl", "wb") as f:
            #     pickle.dump(self.clustering_model, f)

        distances, indices = self.neighbors_classifier.kneighbors(self.normalized_data)

        #print(distances, indices)

    def normalize_data(self) -> np.ndarray:
        '''Normalize dataset'''
        self.scaler = MinMaxScaler()
        print(self.data.shape)
        self.scaler.fit(self.data)

        transformed = self.scaler.transform(self.data)
        assert np.any(np.isnan(transformed)) == False, "There is a NaN value in array"
        assert np.all(np.isfinite(transformed)), "There is a infinite number in array"
        return  transformed



    def find_neigbors(self, track_array, n:int=4) -> np.ndarray:
        '''Find nearest tracks. \n
        Return numpy list of found ids.'''
        print(f'Find neighbors')
        
        #['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness','acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'],
        # track_array = np.array( track.convert_to_array_for_classification() )
        # print(track_array.shape)
        # track_array = self.scaler.transform([track_array])
       

        distances, neighbors = self.neighbors_classifier.kneighbors(track_array, n_neighbors=n, return_distance=True)
        #print( 'distances:' ,distances )
        #print('neighbor indexes:', neighbors)

        similar_tracks = list()
        for i in neighbors[0]:
            similar_tracks.append(  self.data_trim.iloc[i].Id )

        return similar_tracks

    # def get_dataframe_with_genre_dummies(self, track_df):
    #     print(track_df)

    #     empty_df = pd.DataFrame(columns=self.pd_data.columns).drop(['cluster'] + self.columns_to_drop, axis=1)
    #     for col in empty_df.columns:

    #         print(col, type(col))
    #         if col in track_df.columns.tolist():
    #             empty_df[col] = [track_df[col]]
    #         else:
    #             if col in track_df['genre']:
    #                 empty_df[col] = [1]
    #             else:
    #                 empty_df[col] = 0
    #     print(empty_df.columns)
    #     return empty_df


    def create_basic_queue(self, track: Track, length=5) -> list[str]:
        '''Create queue from track. \n
        Return list of ids.'''

        #['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness','acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'],
        track_df = track.get_dataframe_for_classification()
        # track_array = self.get_dataframe_with_genre_dummies(track_df).to_numpy()
        track_array = track_df.to_numpy()
        #track_array = np.array( track.convert_to_array_for_classification() )

        print(track_array.shape)
        track_array = self.scaler.transform(track_array)

        cluster = self.get_cluster_for_track(track=track_array)
        print(f'Cluster assigned = {cluster}')
        self.data_trim = self.pd_data[self.pd_data['cluster'] == cluster]
        print(f'New df = {self.data_trim.shape} {self.data_trim.columns}')
        self.data_trim = self.data_trim.drop(['cluster'], axis=1)
        print(f'New df = {self.data_trim.shape} {self.data_trim.columns}')
        #self.labels = self.pd_data.keys()
        self.data =  self.data_trim.drop(self.columns_to_drop, axis=1).to_numpy()
        #print(f'Labels: {self.labels.shape} {self.labels}')
        print(f'Data: {self.data.shape}')
        self.normalized_data =  self.normalize_data()
        print("Normalized data:", self.normalized_data.shape)

        self.fit()

        
        queue = list()
        current_track = track
        for i in range(length):
            candidates = self.find_neigbors(track_array, n=10)
            candidates = list(filter(lambda x: x != track.get_id() and x not in queue, candidates))
        
            if len(candidates) > 0:
                queue.append( candidates[0] )
                current_track = Track(None, candidates[0])

        print(queue)
        return queue

    def cluster_kmeans(self, X: np.array, n_clusters: int = 100) -> np.array:
        '''
        Perform clustering on the df.

        Params:
            `X`: numpy array of the data to be fit
            `n_clusters`: number of clusters to be created

        Return:
            np.array of clusters assigned
        '''
        np.random.seed(SEED)
        self.clustering_model = cluster.KMeans(n_clusters=25)
        clusters = self.clustering_model.fit_predict(X)
        print(f'Clusters: {np.unique(clusters)}')
        return clusters

    def get_cluster_for_track(self, track: np.array) -> int:
        '''
        Get cluster index for track.
        '''
        np.random.seed(SEED)
        transformed_track = self.scaler.transform(track.reshape((1, -1)))
        predicted_cluster = self.clustering_model.predict(transformed_track)[0]
        print(f'Cluster predicted: {predicted_cluster}')
        return predicted_cluster
        



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