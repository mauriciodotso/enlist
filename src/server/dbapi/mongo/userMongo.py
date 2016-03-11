from ..DAO.userDAO import UserDAO
from baseMongo import BaseMongo


class UserMongo(BaseMongo, UserDAO):
    def __init__(self, database):
        super(UserMongo, self).__init__(database, database.users)

    def insert_movie(self, user_id, movie_id, status=0):
        try:
            return self.table.update({'_id': user_id, 'movies._id': {'$ne': movie_id}}, {'$addToSet': {'movies': {'_id': movie_id, 'status': status}}})
        except Exception:
            raise Exception

    def insert_book(self, user_id, book_id, status=0):
        try:
            return self.table.update({'_id': user_id, 'books._id': {'$ne': book_id}}, {'$addToSet': {'books': {'_id': book_id, 'status': status}}})
        except Exception:
            raise Exception

    def delete_movie(self, user_id, movie_id):
        try:
            return self.table.update({'_id': user_id, 'movies._id':  movie_id}, {'$pull': {'movies': {'_id': movie_id}}})
        except Exception:
            raise Exception

    def delete_book(self, user_id, book_id):
        try:
            return self.table.update({'_id': user_id, 'books._id': book_id}, {'$pull': {'books': {'_id': book_id}}})
        except Exception:
            raise Exception

    def update_movie(self, user_id, movie_id, status):
        try:
            return self.table.update({'_id': user_id, 'movies._id': movie_id}, {'$set': {'movies.$.status': status}})
        except Exception:
            raise Exception

    def update_book(self, user_id, book_id, status):
        try:
            return self.table.update({'_id': user_id, 'books._id': book_id}, {'$set': {'books.$.status': status}})
        except Exception:
            raise Exception

    def get_movies(self, user_id):
        try:
            return self.table.find_one({'_id': user_id}, {'movies':  1, '_id': 0})['movies']
        except Exception:
            raise Exception

    def get_books(self, user_id):
        try:
            return self.table.find_one({'_id': user_id}, {'books':  1, '_id': 0})['books']
        except Exception:
            raise Exception
