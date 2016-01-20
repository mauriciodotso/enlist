from flask import json
from bson import ObjectId
import unittest
import pymongo
import os
import sys
import json

sys.path.insert(0, os.path.realpath('./') + '/..')

from dbapi.api import DBAPI
import urls

connection = pymongo.MongoClient("mongodb://localhost")
database = connection.enlist_test
dbapi = DBAPI(database=database)

total = 51
limit = 10
books = []
movies = []
user_books = []
user_movies = []
user_id = 0
token = 'ATDochTcKxrvCnqncrAcgtlyhCDwQfvbAurhqbYvJMyCUTFMTVZwYkrDbxKHwKXtzMRexjHRBvGVddCnBbpjpXqIaaPsXiaDIVCeOCJxCOCRNnxllFMNGdrBmTcphxbC'

def clean_database():
    database.books.remove({})
    database.movies.remove({})
    database.users.remove({})
    database.sessions.remove({})

class RestAPIUserTest(unittest.TestCase):
    def setUp(self):
        global user_id
        username =  "Test"

        user_id = database.users.insert({'_id': username, 'password': '123456789', 'movies': user_movies, 'books': user_books})
        dbapi.sessions.insert({'_id': token, 'user_id': username})

        year = 1975

        for i in xrange(total):
            book = {'title': ("Book" + str(year)),'year': year, 'edition': 1, 'img': "book.png"}
            movie = {'title': ("Movie" + str(year)),'year': year, 'img': "movie.png"}
            year += 1

            book_id = database.books.insert(book)
            movie_id = database.movies.insert(movie)
            book['_id'] = str(book_id)
            movie['_id'] = str(movie_id)

            books.append(book)
            movies.append(movie)

            if i%2 == 0:
                database.users.update_one({'_id': user_id}, {'$addToSet': {'books': {'_id': book_id, 'status': 0}}})
                user_books.append(book)
            else:
                database.users.update_one({'_id': user_id}, {'$addToSet': {'movies': {'_id': movie_id, 'status': 0}}})
                user_movies.append(movie)

        urls.app.config['TESTING'] = True
        urls.test_database(database)
        self.app = urls.app.test_client()

    def tearDown(self):
        global books
        books = []
        clean_database()

    def test_user_create(self):
        username = "Test2"
        password = "123456789"
        resp = self.app.post('/user/create', data=json.dumps(dict({'username': username, 'password': password})), content_type='application/json')
        users = database.users.find({}).count()

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(users, 2)

        username = "Test"
        resp = self.app.post('/user/create', data=json.dumps(dict({'username': username, 'password': password})), content_type='application/json')
        users = database.users.find({}).count()

        self.assertEqual(resp.status_code, 409)
        self.assertEqual(users, 2)

        resp = self.app.post('/user/create', data=json.dumps(dict({})), content_type='application/json')
        users = database.users.find({}).count()

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(users, 2)

    def test_user_update(self):
        """Update specified user info.

        Method:
            POST

        Args:
            username (str): User's username
            token (str): User's session token
            password(Option[str]): User's updated password

        Returns:
            200: If User's info were updated

        Raises:
            403: If a invalid token is passed, or no token is passed, or invalid permission.
            404: If the specified Id does not exist.
            400: If the user was not updated.
        """
        pass

    def test_user_delete(self):
        """Delete specified user.

        Method:
            POST

        Args:
            username (str): User's username
            token (str): User's session token

        Returns:
            200: If the user was deleted

        Raises:
            403: If a invalid token is passed, or no token is passed or invalid permission.
            404: If the specified Id does not exist.
        """
        pass

    def test_user_add_book(self):
        """Add book to user list.

        Method:
            POST

        Args:
            username (str): User's username
            token (str): User's session token
            book_id(ObjId): Book's id

        Returns:
            200: If User's info were updated

        Raises:
            403: If a invalid token is passed, or no token is passed, or invalid permission.
            404: If the specified Id does not exist.
            400: If the user was not updated.
        """
        pass

    def test_user_update_book(self):
        """Update book status on user list.

        Method:
            POST

        Args:
            username (str): User's username
            token (str): User's session token
            book_id(ObjId): Book's id
            status:(int): Book's status

        Returns:
            200: If User's info were updated

        Raises:
            403: If a invalid token is passed, or no token is passed, or invalid permission.
            404: If the specified Id does not exist.
            400: If the user was not updated.
        """
        pass

    def test_user_add_movie(self):
        """Add movie to user list.

        Method:
            POST

        Args:
            username (str): User's username
            token (str): User's session token
            movie_id(ObjId): Movie's id

        Returns:
            200: If User's info were updated

        Raises:
            403: If a invalid token is passed, or no token is passed, or invalid permission.
            404: If the specified Id does not exist.
            400: If the user was not updated.
        """
        pass

    def test_user_update_movie(self):
        """Update movie status on user list.

        Method:
            POST

        Args:
            username (str): User's username
            token (str): User's session token
            movie_id(ObjId): Movie's id
        status:(int): Movie's status

        Returns:
            200: If User's info were updated

        Raises:
            403: If a invalid token is passed, or no token is passed, or invalid permission.
            404: If the specified Id does not exist.
            400: If the user was not updated.
        """
        pass

if __name__ == "__main__":
    unittest.main()
