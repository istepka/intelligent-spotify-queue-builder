from distutils.core import setup
from classes.downloader import Downloader
from classes.tracks import Track
from scripts.dataset_creator import DatasetCreator
import os
import pandas as pd
from scripts import setup

# creator = DatasetCreator()
# for i in range(53):
#    creator.create_dataset(2022 - i, 1, 850)

#combine
# path = './datasets/datasets_batch'
# out_path = './datasets'
# filenames =os.listdir(path)
# print(filenames)

# for i, filename in enumerate(filenames):
#     if 'full' in filename:
#         df = pd.read_csv(f'{path}/{filename}')
#         if i == 0:
#             df.to_csv(f'{out_path}/Tracks1970-2022_850.csv', mode='w', 
#                 header=True, index=False)
#         else:
#             df.to_csv(f'{out_path}/Tracks1970-2022_850.csv', mode='a', 
#                 header=False, index=False)



# d = Downloader(setup.get_spotify_username())
   
# sonne = Track(d.fetch_single_track_by_name('sonne'))
# sonne.load_additional_song_data(d)

# print(d.get_related_artists(sonne.artist_id))
#print(d.get_artist_top_tracks(sonne.artist_id))

print(pd.read_csv('datasets/full - Copy.csv').dropna().info())