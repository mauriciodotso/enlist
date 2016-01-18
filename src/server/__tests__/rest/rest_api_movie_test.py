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
movies = []
user_id = 0
token = 'ATDochTcKxrvCnqncrAcgtlyhCDwQfvbAurhqbYvJMyCUTFMTVZwYkrDbxKHwKXtzMRexjHRBvGVddCnBbpjpXqIaaPsXiaDIVCeOCJxCOCRNnxllFMNGdrBmTcphxbC'

def clean_database():
    database.movies.remove({})
    database.users.remove({})
    database.sessions.remove({})

class RestAPIMovieTest(unittest.TestCase):
    def setUp(self):
        global user_id
        username =  "Admin"

        user_id = database.users.insert({'_id': username, 'password': '123456789', 'movies': [], 'movies': []})

        dbapi.sessions.insert({'_id': token, 'user_id': username})

        year = 1975

        for i in xrange(total):
            movie = {'title': ("Movie" + str(year)),'year': year, 'img': "movie.png"}
            year += 1

            movie_id = database.movies.insert(movie)
            movie['_id'] = str(movie_id)

            movies.append(movie)

        urls.app.config['TESTING'] = True
        urls.test_database(database)
        self.app = urls.app.test_client()

    def tearDown(self):
        global movies
        movies = []
        clean_database()

    def test_movie_create(self):
        title = "How to ge away with murder"
        year = "2015"
        edition = "1"
        cover = "img.png"
        resp = self.app.post('/movie/create', data=json.dumps(dict({'token': token, 'title': title, 'year': year, 'edition': edition, 'cover': cover})), content_type='application/json')
        movies = database.movies.find({}).count()

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(movies, (total + 1))

        resp = self.app.post('/movie/create', data=json.dumps(dict({'token': '', 'title': title, 'year': year, 'edition': edition, 'cover': cover})), content_type='application/json')
        movies = database.movies.find({}).count()

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(movies, (total + 1))

        resp = self.app.post('/movie/create', data=json.dumps(dict({'token': token, 'year': year, 'edition': edition, 'cover': cover})), content_type='application/json')
        movies = database.movies.find({}).count()

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(movies, (total + 1))

    def test_movie_get(self):
        resp = self.app.post('/movie/get', data=json.dumps(dict({'_id': movies[0]['_id']})), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(movies[0], json.loads(resp.data)['movie'])

        resp = self.app.post('/movie/get', data=json.dumps(dict({'_id': movies[0]['_id'].replace('1', '0')})), content_type='application/json')
        self.assertEqual(resp.status_code, 404)

        resp = self.app.post('/movie/create', data=json.dumps(dict({})), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_movie_update(self):
        movies[0]['title'] = "How to ge away with murder"

        resp = self.app.post('/movie/update', data=json.dumps(dict({'token': token, '_id': movies[0]['_id'], 'title': movies[0]['title']})), content_type='application/json')
        movie = database.movies.find_one({'_id': ObjectId(movies[0]['_id'])})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(movies[0]['title'], movie['title'])

        resp = self.app.post('/movie/update', data=json.dumps(dict({'token': '', '_id': movies[0]['_id'], 'title': movies[0]['title']})), content_type='application/json')
        self.assertEqual(resp.status_code, 403)

        resp = self.app.post('/movie/update', data=json.dumps(dict({'token': token, '_id': movies[0]['_id'].replace('1', '0')})), content_type='application/json')
        self.assertEqual(resp.status_code, 404)

        resp = self.app.post('/movie/update', data=json.dumps(dict({'token': token})), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_movie_search(self):
        resp = self.app.post('/movie/search', data=json.dumps(dict({'limit': limit})), content_type='application/json')
        movies_resp = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(movies_resp['movies']), limit)
        self.assertEqual(int(movies_resp['limit']), limit)
        self.assertEqual(int(movies_resp['total']), total)

        resp = self.app.post('/movie/search', data=json.dumps(dict({'limit': limit, 'page': 5})), content_type='application/json')
        movies_resp = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(movies_resp['movies']), 1)

        resp = self.app.post('/movie/search', data=json.dumps(dict({'limit': limit, 'title': '197'})), content_type='application/json')
        movies_resp = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(movies_resp['movies']), 5)

if __name__ == "__main__":
    unittest.main()
