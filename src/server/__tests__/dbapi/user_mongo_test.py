import unittest
import sys
import os
import pymongo

sys.path.insert(0, os.path.realpath('./') + '/..')

from dbapi.api import DBAPI

connection = pymongo.MongoClient("mongodb://localhost")
database = connection.enlist_test
dbapi = DBAPI(database=database)

books = [{'_id': x, 'status': 0} for x in range(0, 50, 2)]
movies = [{'_id': x, 'status': 0} for x in range(1, 51, 2)]
user = {'username': "Test", 'password': "123456789", 'movies': movies, 'books': books}
user_id = 0


def clean_database():
    database.users.remove({})

class UserMongoTest(unittest.TestCase):
    def setUp(self):
        global user_id
        user_id = database.users.insert(user)

    def tearDown(self):
        clean_database()

    def test_insert_movie(self):
        dbapi.users.insert_movie(user_id, 53)
        movies = database.users.find_one({'_id': user_id}, {'movies':  1, '_id': 0})['movies']
        self.assertEqual(len(movies), 26)

        dbapi.users.insert_movie(user_id, 53)
        movies = database.users.find_one({'_id': user_id}, {'movies':  1, '_id': 0})['movies']
        self.assertEqual(len(movies), 26)

    def test_insert_book(self):
        dbapi.users.insert_book(user_id, 52)
        books = database.users.find_one({'_id': user_id}, {'books':  1, '_id': 0})['books']
        self.assertEqual(len(books), 26)

        dbapi.users.insert_book(user_id, 52)
        books = database.users.find_one({'_id': user_id}, {'books':  1, '_id': 0})['books']
        self.assertEqual(len(books), 26)

    def test_update_movie(self):
        movie_id = 49
        dbapi.users.update_movie(user_id, movie_id, 1)
        status = database.users.find_one({'_id': user_id, 'movies': {'$elemMatch': {'_id': movie_id}}}, {'movies.$.status':  1, '_id': 0})['movies'][0]['status']
        self.assertEqual(status, 1)

    def test_update_book(self):
        book_id = 42
        dbapi.users.update_book(user_id, book_id, 1)
        status = database.users.find_one({'_id': user_id, 'books': {'$elemMatch': {'_id': book_id}}}, {'books.$.status': 1, '_id': 0})['books'][0]['status']
        self.assertEqual(status, 1)
        
    def test_get_movies(self):
        movies = dbapi.users.get_movies(user_id)

        self.assertEqual(len(movies), 25)

        for movie in movies:
            self.assertEqual(movie['_id']%2, 1)

    def test_get_books(self):
        books = dbapi.users.get_books(user_id)

        self.assertEqual(len(books), 25)

        for book in books:
            self.assertEqual(book['_id']%2, 0)

if __name__ == '__main__':
    unittest.main()
