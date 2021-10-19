from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import redirect
from factory import Factory
from scripts import setup
from classes.downloader import Downloader
from classes.tracks import Track
from classes.player import SpotifyPlayer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trackData.db'

db = SQLAlchemy(app)
Factory.set_db(db)

#Imports that rely on Factory variable: db
from classes.data_access import DataAccess
from classes.trackData import TrackData


def search_for_track(name):
    '''Search for the track'''
    #setup which requires properly created 'credentials.txt' file
    setup.prep_env_from_file()
    username  = setup.get_spotify_username()

    #create downloader instance for user
    downloader = Downloader(username)

    #TODO search in database and then eventually fetch from spoti
    #download desired track data by name
    track = Track(downloader.fetch_single_track_by_name(name))
    td = TrackData(id=track.id, name=track.name, artist=track.artist_name, album=track.album_name)
    return td
   

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['search_track']

        if len(task_content) > 0:
            try: 
                td = search_for_track(task_content)
                DataAccess.single_insert(td)
            except:
                return 'There was an issue searching for your track'

        #tracks = TrackData.query.order_by(TrackData.name).all()
        tracks = DataAccess.get_all()
        return render_template('index.html', tracks=tracks)
    else:
        return render_template('index.html')

@app.route('/play/<string:id>')
def play(id):
    player = SpotifyPlayer(setup.get_spotify_username())
    player.add_track_to_queue_by_id(id)

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)

   