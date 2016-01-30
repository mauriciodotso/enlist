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
user_id = 0
token = 'ATDochTcKxrvCnqncrAcgtlyhCDwQfvbAurhqbYvJMyCUTFMTVZwYkrDbxKHwKXtzMRexjHRBvGVddCnBbpjpXqIaaPsXiaDIVCeOCJxCOCRNnxllFMNGdrBmTcphxbC'

def clean_database():
    database.books.remove({})
    database.users.remove({})
    database.sessions.remove({})

class RestAPIBookTest(unittest.TestCase):
    def setUp(self):
        global user_id
        username =  "Admin"

        user_id = database.users.insert({'_id': username, 'password': '123456789', 'movies': [], 'books': []})

        dbapi.sessions.insert({'_id': token, 'user_id': username})

        year = 1975

        for i in xrange(total):
            book = {'title': ("Book" + str(year)),'year': year, 'edition': 1, 'img': "book.png"}
            year += 1

            book_id = database.books.insert(book)
            book['_id'] = str(book_id)

            books.append(book)

        urls.app.config['TESTING'] = True
        urls.test_database(database)
        self.app = urls.app.test_client()

    def tearDown(self):
        global books
        books = []
        clean_database()

    def test_book_create(self):
        title = "How to ge away with murder"
        year = "2015"
        edition = "1"
        cover = "img.png"
        resp = self.app.post('/book/create', data=json.dumps(dict({'token': token, 'title': title, 'year': year, 'edition': edition, 'cover': cover})), content_type='application/json')
        books = database.books.find({}).count()

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(books, (total + 1))

        resp = self.app.post('/book/create', data=json.dumps(dict({'token': '', 'title': title, 'year': year, 'edition': edition, 'cover': cover})), content_type='application/json')
        books = database.books.find({}).count()

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(books, (total + 1))

        resp = self.app.post('/book/create', data=json.dumps(dict({'token': token, 'year': year, 'edition': edition, 'cover': cover})), content_type='application/json')
        books = database.books.find({}).count()

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(books, (total + 1))

    def test_book_get(self):
        resp = self.app.post('/book/get', data=json.dumps(dict({'_id': books[0]['_id']})), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(books[0], json.loads(resp.data)['book'])

        resp = self.app.post('/book/get', data=json.dumps(dict({'_id': hex(int(books[0]['_id'], 16) - 1)[2:].rstrip("L")})), content_type='application/json')
        self.assertEqual(resp.status_code, 404)

        resp = self.app.post('/book/create', data=json.dumps(dict({})), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_book_update(self):
        books[0]['title'] = "How to ge away with murder"

        resp = self.app.post('/book/update', data=json.dumps(dict({'token': token, '_id': books[0]['_id'], 'title': books[0]['title']})), content_type='application/json')
        book = database.books.find_one({'_id': ObjectId(books[0]['_id'])})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(books[0]['title'], book['title'])

        resp = self.app.post('/book/update', data=json.dumps(dict({'token': '', '_id': books[0]['_id'], 'title': books[0]['title']})), content_type='application/json')
        self.assertEqual(resp.status_code, 403)

        resp = self.app.post('/book/update', data=json.dumps(dict({'token': token, '_id': hex(int(books[0]['_id'], 16) - 1)[2:].rstrip("L")})), content_type='application/json')
        self.assertEqual(resp.status_code, 404)

        resp = self.app.post('/book/update', data=json.dumps(dict({'token': token})), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_book_search(self):
        resp = self.app.post('/book/search', data=json.dumps(dict({'limit': limit})), content_type='application/json')
        books_resp = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(books_resp['books']), limit)
        self.assertEqual(int(books_resp['limit']), limit)
        self.assertEqual(int(books_resp['total']), total)

        resp = self.app.post('/book/search', data=json.dumps(dict({'limit': limit, 'page': 5})), content_type='application/json')
        books_resp = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(books_resp['books']), 1)

        resp = self.app.post('/book/search', data=json.dumps(dict({'limit': limit, 'title': '197'})), content_type='application/json')
        books_resp = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(books_resp['books']), 5)

if __name__ == "__main__":
    unittest.main()
