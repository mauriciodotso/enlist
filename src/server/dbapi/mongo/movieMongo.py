from ..DAO.movieDAO import MovieDAO
import pymongo


class MovieMongo(MovieDAO):
    def __init__(self, database)
        self.movies = database.movies
    
    def get(self, id):
        try:
            return self.movies.find_one({'_id': id})
        except Exception
            raise Exception

    def get_all(self, limit=10, offset=0):
        try:
            cursor = self.meals.find().sort('name', pymongo.DESCENDING).limit(limit).skip(offset*limit)
            total = self.meals.find().count()
            result = []
            
            for movie in cursor:
                result.append(movie)

            return result, total
        except Exception
            raise Exception

    def insert(self, movie):
        try:
            return self.movies.insert_one(movie)
        except Exception
            raise Exception

    def update(self, movie):
        try:
            return self.movies.update({'_id': movie['_id']}, {'$set': movie})
        except Exception
            raise Exception

    def remove(self, id):
        try:
            return self.movies.remove({'_id': id})
        except Exception
            raise Exception

