from ..DAO/userDAO import UserDAO
import pymongo


class UserMongo(UserDAO):
    def __init__(self, database):
            self.users = database.users

    def get(self, id):
        try:
            return self.users.find_one({'_id': id})
        except Exception
            raise Exception

    def insert(self, user):
        try:
            return self.users.insert_one(user)
        except Exception
            raise Exception

    def update(self, user):
        try:
            return self.users.update({'_id': user['_id']}, {'$set': user})
        except Exception
            raise Exception

    def remove(self, id):
        try:
            return self.users.remove({'_id': id})
        except Exception
            raise Exception

