from ..mongo import bookMongo, movieMongo,  userMongo, sessionMongo


class DBFactory(object):
    def __init__(self, database, db_type=0):
        self.db_type = db_type
        self.database = database

    def books(self):
        if self.db_type == 0:
            return bookMongo.BookMongo(self.database)

    def movies(self):
        if self.db_type == 0:
            return movieMongo.MovieMongo(self.database)
	
    def users(self):
        if self.db_type == 0:
            return userMongo.UserMongo(self.database)

    def sessions(self):
        if self.db_type == 0:
            return sessionMongo.SessionMongo(self.database)
