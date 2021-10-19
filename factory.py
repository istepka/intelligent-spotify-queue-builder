class Factory:
    '''Factory class that allows global access to certain variables and objects'''
    db = None

    @classmethod 
    def get_db(cls):
        return cls.db
    
    @classmethod
    def set_db(cls, _db):
        cls.db = _db