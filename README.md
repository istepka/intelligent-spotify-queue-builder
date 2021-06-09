## Spotify - similar vibe - queue builder
***
#### Goal and motivation
Spotify does a great job at creating custom playlists and recommending personal queues.  
But for me, the lack of manual personalization is something that should definitely be changed. Often times I just want to vibe and listen to some music regardless of genre, artist, album etc, but Spotify constantly tries to prove me wrong, and recommend stuff from pretty closed area. 

I want to create an app that will be capable of creating Spotify queues built from tracks that have similar vibe to the music you play no matter what genre they are or who is the artist.  

Detailed explanation will be provided at the later stage of development.

#### Project steps:
1. [DONE] Create data downloader that will be able to fetch data from Spotify API
1. [CURRENT] Fetch tracks data and create dataset. For now let's say we get a few thousand records
1. Explore, find correlations and understand the data
1. Implement some kNN calssification and find out whether we can distinguish similar tracks
1. (optional) experiment with different types of classification
1. Build first queue builder
1. Build simple platform that can connect with spotify and send play requests
1. Test whole project manually to see if it works acceptably
1. Procceed to the next project iteration

***
#### Tech stack
* Python 3.9
* Jupyter Notebook
* Pandas
* Matplotlib
* Spotipy
 
