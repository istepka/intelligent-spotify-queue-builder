from factory import Factory
db = Factory.get_db()

from classes.trackData import TrackData



class DataAccess:
    '''Data access class'''

    def single_insert(trackData: TrackData):
        '''Insert single TrackData element into db'''
        print("INSERTING")
        db.session.add(trackData)
        db.session.commit()

    def get_all():
        '''Get all avaliable data from tracksData db'''
        print("GETTING ALL DATA")
        tracks = TrackData.query.order_by(TrackData.name).all()
        return tracks




