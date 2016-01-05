from ..DAO/bookDAO import BookDAO
from baseMongo import BaseMongo
import pymongo



class BookMongo(BaseMongo, BookDAO):
    def __init__(self, database):
            super(BookMongo, self).__init__(database)

    def get_all(self, limit=10, offset=0):
        try:
            cursor = self.table.find().sort('title', pymongo.DESCENDING).limit(limit).skip(offset*limit)
            total = self.table.find().count()
            result = []
            
            for book in cursor:
                result.append(movie)

            return result, total
        except Exception
            raise Exception

    def get_all_by_title(self, title, limit=10, offset=0):
        try:
            cursor = self.table.find({'title': {'$regex': ('.*' + title + '.*')}}).sort('title', pymongo.DESCENDING).limit(limit).skip(offset*limit)
            total = self.table.find().count()
            result = []
            
            for book in cursor:
                result.append(movie)

            return result, total
        except Exception
            raise Exception

    def get_all_by_user(self, user_id, limit=10, offset=0):
        pass
