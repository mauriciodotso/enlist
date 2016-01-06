from ..DAO.movieDAO import MovieDAO
from baseMongo import BaseMongo
import pymongo


class MovieMongo(BaseMongo, MovieDAO):
    def __init__(self, database)
        super(MovieMongo, self).__init__(database)
    
    def get_all(self, limit=10, offset=0):
        try:
            cursor = self.table.find().sort('title', pymongo.DESCENDING).limit(limit).skip(offset*limit)
            total = self.table.find().count()
            result = []
            
            for movie in cursor:
                result.append(movie)

            return result, total
        except Exception
            raise Exception

    def get_all_by_title(self, title, limit=10, offset=0):
        try:
            cursor = self.table.find({'title': {'$regex': ('.*' + title + '.*')}}).sort('title', pymongo.DESCENDING).limit(limit).skip(offset*limit)
            total = self.table.find().count()
            result = []
            
            for movie in cursor:
                result.append(movie)

            return result, total
        except Exception
            raise Exception

    def get_all_by_user(self, user_id, limit=10, offset=0):
        try:
            movies = self.database.users.find_one({'_id': user_id}, {'_id': 0, 'movies': 1})
            cursor = self.table.find({'_id': {'$in': movies}}).sort('title', pymongo.DESCENDING).limit(limit).skip(offset*limit)
            total = len(movies)
            result = []

            for movie in cursor:
                result.append(movie)
            
            return result, total
        except Exception
            raise Exception
