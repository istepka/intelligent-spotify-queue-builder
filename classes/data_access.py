from classes.tracks import Track
from factory import Factory
db = Factory.get_db()

from classes.trackData import TrackData



class DataAccess:
    '''Data access class'''

    def single_insert(trackData: TrackData):
        '''Insert single TrackData element into db'''
        print("INSERTING")
        try:
            db.session.add(trackData)
            db.session.commit()
        except:
            return 'There was a problem inserting that track'

    def get_all():
        '''Get all avaliable data from tracksData db'''
        print("GETTING ALL DATA")
        tracks = TrackData.query.order_by(TrackData.name).all()
        return tracks

    def delete(id):
        track_to_delete = TrackData.query.get_or_404(id)
        try:
            db.session.delete(track_to_delete)
            db.session.commit() 
        except:
            return 'There was a problem deleting that track'

    def get_by_ids(ids):
        tracks = TrackData.query.filter(TrackData.id.in_(ids)).all()
        return tracks



