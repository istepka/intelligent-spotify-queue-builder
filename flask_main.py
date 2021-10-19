from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import redirect
from scripts import setup
from classes.downloader import Downloader
from classes.tracks import Track

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


db = SQLAlchemy(app)
class TrackData(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200), default='no data')
    album = db.Column(db.String(200), default='no data')


    def __repr__(self) -> str:
        return '<Task %r>' % self.id

    #type db.create_all() to create database

def search_for_track(name):

    #setup which requires properly created 'credentials.txt' file
    setup.prep_env_from_file()
    username  = setup.get_spotify_username()

    #create downloader instance for user
    downloader = Downloader(username)

    #download desired track data by name
   
    track = Track(downloader.fetch_single_track_by_name(name))
    td = TrackData(id=track.id, name=track.name, artist=track.artist_name, album=track.album_name)
    db.session.add(td)
    db.session.commit()
   



@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['search_track']

        if len(task_content) > 0:
            try: 
                search_for_track(task_content)
            except:
                return 'There was an issue searching for your track'

        tracks = TrackData.query.order_by(TrackData.name).all()
        return render_template('index.html', tracks=tracks)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

   