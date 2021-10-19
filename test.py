from classes.tracks import Track
from classes.downloader import Downloader
import pandas as pd
df = pd.read_csv('./datasets/Tracks_14400dp_y1990-2021_full.csv')['Id']
for i, d in enumerate(df):
    track = Track(track_id=d)



    if i % 100 == 0:
        print(f'i/{len(df)}')
    
