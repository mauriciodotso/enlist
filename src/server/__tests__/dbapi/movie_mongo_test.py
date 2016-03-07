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
movies = []
user_movies = []
user_id = 0

def clean_database():
    database.movies.remove({})
    database.users.remove({})

class MovieMongoTest(unittest.TestCase):
    def setUp(self):
        global user_id
        user_id = database.users.insert({'_id': "testUser", 'password': '123456789', 'movies': [], 'books': []})
        year = 1975

        for i in xrange(total):
            movie = {'title': ("Movie" + str(year)),'year': year, 'edition': 1, 'img': "movie.png"}
            year += 1

            movie_id = database.movies.insert(movie)

            movie['_id'] = movie_id

            if i%2 == 0:
#                movie['status'] = 0
                database.users.update_one({'_id': user_id}, {'$addToSet': {'movies': {'_id': movie_id, 'status': 0}}})
                user_movies.append(movie)

            movies.append(movie)

    def tearDown(self):
        global movies
        movies = []
        global user_movies
        user_movies= []
        clean_database()

    def test_get_all(self):
        result, movies_total = dbapi.movies.get_all(limit, 0)

        self.assertEqual(len(result), limit)

        for i in xrange(limit):
            self.assertEqual(movies[i], result[i])

        result, movies_total = dbapi.movies.get_all(limit, offset)

        self.assertEqual(len(result), min((total - limit), limit))

        for i in xrange(limit*offset, min(total, offset*limit + limit)):
            self.assertEqual(movies[i], result[i%limit])

        self.assertEqual(movies_total, total)

    def test_get_all_by_title(self):
        result, movies_total = dbapi.movies.get_all_by_title('Movie19', limit, 0)
        self.assertEqual(len(result), limit)

        for i in xrange(limit):
            self.assertEqual(movies[i], result[i])

        result, movies_total = dbapi.movies.get_all_by_title('Movie19', limit, offset)

        self.assertEqual(len(result), min((total - limit), limit))

        for i in xrange(limit*offset, min(total, offset*limit + limit)):
            self.assertEqual(movies[i], result[i%limit])

        self.assertEqual(movies_total, 25)

    def test_get_all_by_user(self):
        result, movies_total = dbapi.movies.get_all_by_user(user_id, limit, 0)

        self.assertEqual(len(result), limit)

        for i in xrange(limit):
            user_movies[i]['status'] = 0
            self.assertEqual(user_movies[i], result[i])

        result, movies_total = dbapi.movies.get_all_by_user(user_id, limit, offset)

        self.assertEqual(len(result), min((total - limit), limit))

        for i in xrange(limit*offset, min(total, offset*limit + limit)):
            user_movies[i]['status'] = 0
            self.assertEqual(user_movies[i], result[i%limit])

        self.assertEqual(movies_total, 25)

    def test_get_all_not_listed(self):
        result, movies_total = dbapi.movies.get_all_not_listed(user_id, limit, 0)

        self.assertEqual(len(result), limit)

        for i in xrange(limit):
            self.assertEqual(movies[i*2 + 1], result[i])
    
        result, movies_total = dbapi.movies.get_all_not_listed(user_id, limit, offset)

        self.assertEqual(len(result), min((total - limit), limit))

        for i in xrange(limit*(offset + 1), min(total, offset*limit + limit)):
            self.assertEqual(movies[i + i%10], result[i%limit])

        self.assertEqual(movies_total, 25)

    def test_get_all_not_listed_by_title(self):
        result, mvoies_total = dbapi.movies.get_all_not_listed_by_title('Movie19', user_id, limit, 0)
        self.assertEqual(len(result), limit)

        for i in xrange(limit):
            self.assertEqual(movies[i*2 + 1], result[i])
    
        result, movies_total = dbapi.movies.get_all_not_listed_by_title('Movie19', user_id, limit, offset)

        self.assertEqual(len(result), min((movies_total - limit), limit))

        for i in xrange(limit*offset, min(offset*limit + limit, offset*limit + (movies_total - limit))):
            self.assertEqual(movies[i + 11 + i%10], result[i%limit])

        self.assertEqual(movies_total, 12)

if __name__ == '__main__':
    unittest.main()
