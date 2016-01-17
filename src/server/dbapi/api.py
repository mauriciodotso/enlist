import pymongo
from factory.DBFactory import DBFactory


class DBAPI(object):
    def __init__(self, db_type=0, **kwargs):
        if db_type == 0:
            if not 'database' in kwargs:
                connection = pymongo.MongoClient("mongodb://localhost")
                self.database = connection.enlist
            else:
                self.database = kwargs['database']

        factory = DBFactory(self.database, db_type)

        self.books = factory.books()
        self.users = factory.users()
        self.movies =  factory.movies()
        self.sessions = factory.sessions()
