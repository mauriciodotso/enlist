from ..DAO/userDAO import UserDAO
from baseMongo import BaseMongo


class UserMongo(BaseMongo, UserDAO):
    def __init__(self, database):
        super(UserMongo, self).__init__(database)

    def insert_movie(self, user_id, movie_id):
        pass

    def insert_book(self, user_id, book_id):
        pass
