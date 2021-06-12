## Spotify - similar vibe - queue builder
***
### Goal and motivation
Spotify does a great job at creating custom playlists and recommending personal queues. 
But for me, the lack of manual personalization is something that should definitely be changed. Often times I just want to vibe and listen to some music regardless of genre, artist, album etc.

This app is meant to be capable of creating Spotify queues built from tracks that have similar vibe to the music you play no matter what genre they are or who is the artist.  


### Project steps:
1. `[DONE]` Create data downloader that will be able to fetch data from Spotify API
1. `[DONE]` Fetch tracks data and create dataset. For now let's say we get a few thousand records
1. `[DONE]` Explore, find correlations and understand the data
1. `[DONE]` Implement kNN calssification and find out whether we can distinguish similar tracks
1. (optional) experiment with different types of classification
1. `[DONE]` Build first queue builder
1. Build simple platform that can connect with spotify and send play requests. 
1. Test whole project manually to see if it works acceptably
1. Procceed to the next project iteration

***
### How to use
There is an entry point, `overview.py`, from which you can easily run the project and see how the basic functionality of creating queue and adding it to your spotify works.

####  **Requirements**
1. `credentials.txt` in the main project folder should contain: 

    ```
    spotfy_unique_username
    client_id
    client_secret
    ```
    Client id and secret can be obtained from Spotify developer application dashboard.
1. Python stuff:  
    * Python=3.9
    * Spotipy=2.18.0
    * Scikit-learn= 0.24.2
    * Pandas=1.2.2
    * Numpy=1.20.1


***
#### Tech stack
* Python 3.9
* Jupyter Notebook
* Pandas
* Matplotlib
* ScikitLearn
* Spotipy
* Numpy
 
