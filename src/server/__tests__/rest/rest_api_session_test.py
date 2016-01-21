from flask import json
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

def clean_database():
    database.sessions.remove({})
    database.users.remove({})

class RestAPISessionTest(unittest.TestCase):
    def setUp(self):
        urls.app.config['TESTING'] = True
        urls.test_database(database)
        self.app = urls.app.test_client()

    def tearDown(self):
        clean_database()

    def test_login(self):
        username = "Test"
        hashed_password = "ec386b1a1081c6298dd5bb632051f265dfc67ea95715eb68c52fc4d74d9f9616,12345"
        password = "123456"

        dbapi.users.insert({'_id': username, 'password': hashed_password, 'movies': [], 'books': []})

        resp = self.app.post('/login', data=json.dumps(dict({'username': username, 'password': password})), content_type='application/json')
        sessions = database.sessions.find({}).count()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(sessions, 1)

    def test_logout(self):
        token = 'ATDochTcKxrvCnqncrAcgtlyhCDwQfvbAurhqbYvJMyCUTFMTVZwYkrDbxKHwKXtzMRexjHRBvGVddCnBbpjpXqIaaPsXiaDIVCeOCJxCOCRNnxllFMNGdrBmTcphxbC'
        username =  "Test"

        dbapi.sessions.insert({'_id': token, 'user_id': username})

        resp = self.app.post('/logout', data=json.dumps(dict({'token': token})), content_type='application/json')
        sessions = database.sessions.find({}).count()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(sessions, 0)

if __name__ == "__main__":
    unittest.main()
