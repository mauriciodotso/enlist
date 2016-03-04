import unittest
import sys
import os
import pymongo
import datetime
import time

sys.path.insert(0, os.path.realpath('./') + '/..')

from dbapi.api import DBAPI

connection = pymongo.MongoClient("mongodb://localhost")
database = connection.enlist_test
dbapi = DBAPI(database=database)

total = 50
limit = 10
offset = 1
books = []
user_books = []
user_id = 0

def clean_database():
    database.books.remove({})
    database.users.remove({})

class BookMongoTest(unittest.TestCase):
    def setUp(self):
        global user_id
        user_id = database.users.insert({'_id': "testUser", 'password': '123456789', 'movies': [], 'books': []})
        year = 1975

        for i in xrange(total):
            book = {'title': ("Book" + str(year)),'year': year, 'edition': 1, 'img': "book.png"}
            year += 1

            book_id = database.books.insert(book)

            book['_id'] = book_id

            if i%2 == 0:
                database.users.update_one({'_id': user_id}, {'$addToSet': {'books': {'_id': book_id, 'status': 0}}})
                user_books.append(book)

            books.append(book)

    def tearDown(self):
        global books 
        books = []
        global user_books 
        user_books= []
        clean_database()

    def test_get_all(self):
        result, books_total = dbapi.books.get_all(limit, 0)

        self.assertEqual(len(result), limit)

        for i in xrange(limit):
            self.assertEqual(books[i], result[i])
    
        result, books_total = dbapi.books.get_all(limit, offset)

        self.assertEqual(len(result), min((total - limit), limit))

        for i in xrange(limit*offset, min(total, offset*limit + limit)):
            self.assertEqual(books[i], result[i%limit])

        self.assertEqual(books_total, total)

    def test_get_all_by_title(self):
        result, books_total = dbapi.books.get_all_by_title('Book19', limit, 0)
        self.assertEqual(len(result), limit)

        for i in xrange(limit):
            self.assertEqual(books[i], result[i])
    
        result, books_total = dbapi.books.get_all_by_title('Book19', limit, offset)

        self.assertEqual(len(result), min((total - limit), limit))

        for i in xrange(limit*offset, min(total, offset*limit + limit)):
            self.assertEqual(books[i], result[i%limit])

        self.assertEqual(books_total, 25)

    def test_get_all_by_user(self):
        result, books_total = dbapi.books.get_all_by_user(user_id, limit, 0)

        self.assertEqual(len(result), limit)

        for i in xrange(limit):
            user_books[i]['status'] = 0
            self.assertEqual(user_books[i], result[i])
    
        result, books_total = dbapi.books.get_all_by_user(user_id, limit, offset)

        self.assertEqual(len(result), min((total - limit), limit))

        for i in xrange(limit*offset, min(total, offset*limit + limit)):
            user_books[i]['status'] = 0
            self.assertEqual(user_books[i], result[i%limit])

        self.assertEqual(books_total, 25)

    def test_get_all_not_listed(self):
        result, books_total = dbapi.books.get_all_not_listed(user_id, limit, 0)

        self.assertEqual(len(result), limit)

        for i in xrange(limit):
            self.assertEqual(books[i*2 + 1], result[i])
    
        result, books_total = dbapi.books.get_all_not_listed(user_id, limit, offset)

        self.assertEqual(len(result), min((total - limit), limit))

        for i in xrange(limit*(offset + 1), min(total, offset*limit + limit)):
            self.assertEqual(books[i + i%10], result[i%limit])

        self.assertEqual(books_total, 25)

if __name__ == '__main__':
    unittest.main()
