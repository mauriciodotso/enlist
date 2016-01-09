from ..DAO.userDAO import UserDAO
from baseMongo import BaseMongo


class UserMongo(BaseMongo, UserDAO):
    def __init__(self, database):
        super(UserMongo, self).__init__(database)

    def insert_movie(self, user_id, movie_id):
        try:
            return self.table.update({'_id': user_id}, {'$addToSet': {'movies': movie_id}})
        except Exception:
            raise Exception

    def insert_book(self, user_id, book_id):
        try:
            return self.table.update({'_id': user_id}, {'$addToSet': {'books': movie_id}})
        except Exception:
            raise Exception

    def get_movies(self, user_id):
        try:
            return self.table.find({'_id': user_id}, {'movies':  1, '_id': 0}})
        except Exception:
            raise Exception

    def get_books(self, user_id):
        try:
            return self.table.find({'_id': user_id}, {'books':  1, '_id': 0}})
        except Exception:
            raise Exception
