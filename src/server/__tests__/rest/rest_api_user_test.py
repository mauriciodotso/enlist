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
        hashed_password = "ec386b1a1081c6298dd5bb632051f265dfc67ea95715eb68c52fc4d74d9f9616,12345"

        user_id = database.users.insert({'_id': username, 'password': hashed_password, 'movies': user_movies, 'books': user_books})
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
        global movies
        global user_books
        global user_movies
        books = []
        movies = []
        user_books = []
        user_movies = []
        clean_database()

    def test_user_create(self):
        username = "Test2"
        password = "123456"

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
        username = "Test"
        password = "987654321"

        resp = self.app.post('/user/update', data=json.dumps(dict({'token': token, 'username': username, 'password': password})), content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        resp = self.app.post('/user/update', data=json.dumps(dict({'token': "token", 'username': username, 'password': password})), content_type='application/json')
        self.assertEqual(resp.status_code, 403)

        resp = self.app.post('/user/update', data=json.dumps(dict({'token': token, 'username': "Test2", 'password': password})), content_type='application/json')
        self.assertEqual(resp.status_code, 404)

        resp = self.app.post('/user/update', data=json.dumps(dict({})), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_user_delete(self):
        username = "Test"
        password = "123456"

        resp = self.app.post('/user/delete', data=json.dumps(dict({})), content_type='application/json')
        users = database.users.find({}).count()

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(users, 1)

        resp = self.app.post('/user/delete', data=json.dumps(dict({'token': "token", 'username': username, 'password': password})), content_type='application/json')
        users = database.users.find({}).count()

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(users, 1)

        resp = self.app.post('/user/delete', data=json.dumps(dict({'token': "token", 'username': "Test2", 'password': password})), content_type='application/json')
        users = database.users.find({}).count()

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(users, 1)

        resp = self.app.post('/user/delete', data=json.dumps(dict({'token': token, 'username': username, 'password': password})), content_type='application/json')
        users = database.users.find({}).count()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(users, 0)

    def test_user_add_book(self):
        username = "Test"

        resp = self.app.post('/user/addbook', data=json.dumps(dict({'token': token, 'username': username, 'book_id': books[1]['_id']})), content_type='application/json')
        count = len(database.users.find_one({'_id': username}, {'books': 1})['books'])

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(user_books) + 1, count)

        resp = self.app.post('/user/addbook', data=json.dumps(dict({'token': "token", 'username': username, 'book_id': books[3]['_id']})), content_type='application/json')
        count = len(database.users.find_one({'_id': username}, {'books': 1})['books'])

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(len(user_books) + 1, count)

        resp = self.app.post('/user/addbook', data=json.dumps(dict({'token': "token", 'username': "Test2", 'book_id': books[3]['_id']})), content_type='application/json')
        count = len(database.users.find_one({'_id': username}, {'books': 1})['books'])

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(len(user_books) + 1, count)

        resp = self.app.post('/user/addbook', data=json.dumps(dict({'token': "token", 'username': "Test2", 'book_id': str(hex(int(books[0]['_id'], 16) - 1)[2:])})), content_type='application/json')
        count = len(database.users.find_one({'_id': username}, {'books': 1})['books'])

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(len(user_books) + 1, count)

        resp = self.app.post('/user/addbook', data=json.dumps(dict({})), content_type='application/json')
        count = len(database.users.find_one({'_id': username}, {'books': 1})['books'])

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(len(user_books) + 1, count)

    def test_user_update_book(self):
        username = "Test"

        resp = self.app.post('/user/updatebook', data=json.dumps(dict({'token': token, 'username': username, 'book_id': books[0]['_id'], 'status': 1})), content_type='application/json')
        status = (database.users.find_one({'_id': username}, {'books': 1})['books'])[0]['status']

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(status, 1)

        resp = self.app.post('/user/updatebook', data=json.dumps(dict({'token': "token", 'username': username, 'book_id': books[3]['_id']})), content_type='application/json')
        status = (database.users.find_one({'_id': username}, {'books': 1})['books'])[1]['status']

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(status, 0)

        resp = self.app.post('/user/updatebook', data=json.dumps(dict({'token': token, 'username': "Test2", 'book_id': books[2]['_id'], 'status': 1})), content_type='application/json')
        status = (database.users.find_one({'_id': username}, {'books': 1})['books'])[1]['status']

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(status, 0)

        resp = self.app.post('/user/updatebook', data=json.dumps(dict({'token': token, 'username': "Test2", 'book_id': str(hex(int(books[0]['_id'], 16) - 1)[2:]), 'status': 1})), content_type='application/json')
        status = (database.users.find_one({'_id': username}, {'books': 1})['books'])[1]['status']

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(status, 0)

        resp = self.app.post('/user/updatebook', data=json.dumps(dict({})), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_user_add_movie(self):
        username = "Test"

        resp = self.app.post('/user/addmovie', data=json.dumps(dict({'token': token, 'username': username, 'movie_id': movies[0]['_id']})), content_type='application/json')
        count = len(database.users.find_one({'_id': username}, {'movies': 1})['movies'])

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(user_movies) + 1, count)

        resp = self.app.post('/user/addmovie', data=json.dumps(dict({'token': "token", 'username': username, 'movie_id': movies[3]['_id']})), content_type='application/json')
        count = len(database.users.find_one({'_id': username}, {'movies': 1})['movies'])

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(len(user_movies) + 1, count)

        resp = self.app.post('/user/addmovie', data=json.dumps(dict({'token': "token", 'username': "Test2", 'movie_id': movies[3]['_id']})), content_type='application/json')
        count = len(database.users.find_one({'_id': username}, {'movies': 1})['movies'])

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(len(user_movies) + 1, count)

        resp = self.app.post('/user/addmovie', data=json.dumps(dict({'token': "token", 'username': "Test2", 'movie_id': str(hex(int(movies[0]['_id'], 16) - 1)[2:])})), content_type='application/json')
        count = len(database.users.find_one({'_id': username}, {'movies': 1})['movies'])

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(len(user_movies) + 1, count)

        resp = self.app.post('/user/addmovie', data=json.dumps(dict({})), content_type='application/json')
        count = len(database.users.find_one({'_id': username}, {'movies': 1})['movies'])

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(len(user_movies) + 1, count)

    def test_user_update_movie(self):
        username = "Test"

        resp = self.app.post('/user/updatemovie', data=json.dumps(dict({'token': token, 'username': username, 'movie_id': movies[1]['_id'], 'status': 1})), content_type='application/json')
        status = (database.users.find_one({'_id': username}, {'movies': 1})['movies'])[0]['status']

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(status, 1)

        resp = self.app.post('/user/updatemovie', data=json.dumps(dict({'token': "token", 'username': username, 'movie_id': movies[3]['_id']})), content_type='application/json')
        status = (database.users.find_one({'_id': username}, {'movies': 1})['movies'])[1]['status']

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(status, 0)

        resp = self.app.post('/user/updatemovie', data=json.dumps(dict({'token': token, 'username': "Test2", 'movie_id': movies[3]['_id'], 'status': 1})), content_type='application/json')
        status = (database.users.find_one({'_id': username}, {'movies': 1})['movies'])[1]['status']

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(status, 0)

        resp = self.app.post('/user/updatemovie', data=json.dumps(dict({'token': token, 'username': "Test2", 'movie_id': str(hex(int(movies[0]['_id'], 16) - 1)[2:]), 'status': 1})), content_type='application/json')
        status = (database.users.find_one({'_id': username}, {'movies': 1})['movies'])[1]['status']

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(status, 0)

        resp = self.app.post('/user/updatemovie', data=json.dumps(dict({})), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

if __name__ == "__main__":
    unittest.main()
