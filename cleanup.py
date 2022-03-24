import pandas as pd
from scripts import setup

from classes.downloader import Downloader

# full = pd.read_csv('./datasets/72k.csv').dropna()
# print(full.info())
# full = full.drop_duplicates().reset_index(drop=True)
# print(full.info())

# artist_ids = full['Artist_id'].tolist()

# downloader = Downloader(setup.get_spotify_username())

# lensum = 0
# genres = list()

# for i in range(0, len(artist_ids), 50):
#     ids = artist_ids[i:i+50]
#     lensum += len(ids)
#     genres+=downloader.get_genres_for_artists(ids)
#     print(f'{i//50} / {len(artist_ids) // 50}')

# print(genres)
# print(f'Lensum check {lensum}, {len(artist_ids)}: ', lensum == len(artist_ids))

# full['genres'] = genres
# full.to_csv('72kwith_genres.csv', index=False)
# print('done')

df = pd.read_csv('72kwith_genres.csv').dropna()
print(eval(df['genres'][0])[0])

def getfirst(x):
    l = eval(x)
    if len(l) > 0:
        
        return l[0]
    else:
        return 'none'

df['genre'] = df['genres'].apply(lambda x: getfirst(x))

print(pd.get_dummies(df.genre.apply(pd.Series), prefix="", prefix_sep="").columns)
print(df.columns)
df.to_csv('72k_with_dummies.csv')