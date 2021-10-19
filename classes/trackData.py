from factory import Factory

db = Factory.get_db()

class TrackData(db.Model):
    '''Track data model'''
    id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200), default='no data')
    album = db.Column(db.String(200), default='no data')


    def __repr__(self) -> str:
        return '<Task %r>' % self.id

    #type db.create_all() to create database