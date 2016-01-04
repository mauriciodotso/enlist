from ..DAO.movieDAO import MovieDAO
from baseMongo import BaseMongo
import pymongo


class MovieMongo(BaseMongo, MovieDAO):
    def __init__(self, database)
        super(MovieMongo, self).__init__(database)
    
    def get_all(self, limit=10, offset=0):
        try:
            cursor = self.table.find().sort('name', pymongo.DESCENDING).limit(limit).skip(offset*limit)
            total = self.table.find().count()
            result = []
            
            for movie in cursor:
                result.append(movie)

            return result, total
        except Exception
            raise Exception
