## Spotify similar tracks queue builder
***
#### Goal
To create an app that is capable of creating Spotify queue which is built from tracks that have similar vibe to the music you play.  
Further explanation will be provided later.

#### Project steps:
1. Create data downloader that will be able to fetch data from Spotify API
1. Fetch tracks data and create dataset. For now let's say we get a few thousand records
1. Explore data, find correlations and understand how does this set works
1. Implement some kNN calssification and find out whether we can distinguish similar tracks
1. (optional) experiment with different types of classification
1. Build first queue builder
1. Build simple platform that can connect with spotify and send play requests
1. Test whole project manually to see if it works acceptably
1. Procceed to the next project iteration

***
#### Tech stack
* Python 3.8.5
* Jupyter Notebook
* Pandas
* Spotipy
 
