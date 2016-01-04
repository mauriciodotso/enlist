from ..DAO/userDAO import UserDAO
from baseMongo import BaseMongo


class UserMongo(BaseMongo, UserDAO):
    def __init__(self, database):
        super(UserMongo, self).__init__(database)

    def get_all_movies(self, limit=10, offset=0):
        pass

    def get_all_books(self, limit=10, offset=0):
        pass
