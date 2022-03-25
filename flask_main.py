from classes.queue_builder import QueueBuilder
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import redirect
from factory import Factory
from scripts import setup
from classes.downloader import Downloader
from classes.tracks import Track
from classes.player import SpotifyPlayer
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trackData.db'

db = SQLAlchemy(app)
Factory.set_db(db)

#Imports that rely on Factory variable: db
from classes.data_access import DataAccess
from classes.trackData import TrackData
from scripts.ui_methods import add_tracks_to_real_queue, search_for_track, build_que_by_track

queBuilder = QueueBuilder()
print(f'Queue builder initialized')
   

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['track_name']

        if len(task_content) > 0:
            try: 
                td = search_for_track(task_content, 'name')
                DataAccess.single_insert(td)
            except:
                return 'There was an issue searching for your track'

        #tracks = TrackData.query.order_by(TrackData.name).all()
        tracks = DataAccess.get_all()
        
        return render_template('index.html', tracks=tracks)
    else:
        tracks = DataAccess.get_all()
        #print(tracks)
        random.shuffle(tracks)
        return render_template('index.html', tracks=tracks[0:50])

@app.route('/build', methods=['POST'])
def build():
    if request.method == 'POST':
        task_content = request.form['track_name']

        try:
            checkbox: bool = request.form['checkbox_autobuild']
        except:
            checkbox = False

        print(checkbox)

        #TODO building queue
        queue = build_que_by_track(task_content, {'length': 10}, qb=queBuilder)
        tracks = DataAccess.get_by_ids(queue)
        found_ids = [i.id for i in tracks]

        #Check if track was in db. Otherwise fetch.
        for track in queue:
            if track not in found_ids:
                try: 
                    td = search_for_track(track, 'id')
                    DataAccess.single_insert(td)
                    tracks.append(td)
                except:
                    print(f'Cannot find {track} in spotify db')

            

        print(f'Q: {queue}\nT:{tracks}')



        if checkbox:
            add_tracks_to_real_queue(queue)

        return render_template('index.html', tracks=tracks)
    else:
        return render_template('index.html')
    # import pandas as pd
    # df = pd.read_csv('./datasets/Tracks_14400dp_y1990-2021_full.csv')['Id']
    # for i, d in enumerate(df):
    #     track = Track(track_id=d)
    #     td = TrackData(id=track.id, name=track.name, artist=track.artist_name, album=track.album_name)
    #     DataAccess.single_insert(td)


    #     if i % 100 == 0:
    #         print(f'{i}/{len(df)}')
    # return render_template('index.html')


@app.route('/play/<string:id>')
def play(id):
    player = SpotifyPlayer(setup.get_spotify_username())
    player.play_now(id)

    return render_template('index.html')

@app.route('/queue/<string:id>')
def queue(id):
    player = SpotifyPlayer(setup.get_spotify_username())
    player.add_track_to_queue_by_id(id)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)


   

   