from ..DAO.movieDAO import MovieDAO
from baseMongo import BaseMongo
import pymongo


class MovieMongo(BaseMongo, MovieDAO):
    def __init__(self, database):
        super(MovieMongo, self).__init__(database, database.movies)

    def get_all(self, limit=10, offset=0):
        try:
            cursor = self.table.find().sort('title', pymongo.ASCENDING).limit(limit).skip(offset*limit)
            total = self.table.find().count()
            result = []

            for movie in cursor:
                result.append(movie)

            return result, total
        except Exception:
            raise Exception

    def get_all_by_title(self, title, limit=10, offset=0):
        try:
            cursor = self.table.find({'title': {'$regex': title}}).sort('title', pymongo.ASCENDING).limit(limit).skip(offset*limit)
            total = self.table.find({'title': {'$regex': title}}).count()
            result = []

            for movie in cursor:
                result.append(movie)

            return result, total
        except Exception:
            raise Exception

    def get_all_by_user(self, user_id, limit=10, offset=0):
        try:
            movies = self.database.users.find_one({'_id': user_id}, {'_id': 0, 'movies._id': 1, 'movies.status': 1})['movies']
            status = {}

            for movie in movies:
                status[movie['_id']] = movie['status']

            movies = [movie['_id'] for movie in movies]

            cursor = self.table.find({'_id': {'$in': movies}}).sort('title', pymongo.ASCENDING).limit(limit).skip(offset*limit)
            total = len(movies)
            result = []

            for movie in cursor:
                movie['status'] = status[movie['_id']]
                result.append(movie)

            return result, total
        except Exception:
            raise Exception
