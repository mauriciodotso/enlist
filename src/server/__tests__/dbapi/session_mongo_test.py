import unittest
import sys
import os
import pymongo

sys.path.insert(0, os.path.realpath('./') + '/..')

from dbapi.api import DBAPI

connection = pymongo.MongoClient("mongodb://localhost")
database = connection.enlist_test
dbapi = DBAPI(database=database)

session = {'_id': "ATDochTcKxrvCnqncrAcgtlyhCDwQfvbAurhqbYvJMyCUTFMTVZwYkrDbxKHwKXtzMRexjHRBvGVddCnBbpjpXqIaaPsXiaDIVCeOCJxCOCRNnxllFMNGdrBmTcphxbC",
        'username': "Test"}

def clean_database():
    database.sessions.remove({})

class SessionMongoTest(unittest.TestCase):
    def setUp(self):
        dbapi.sessions.insert(session)

    def tearDown(self):
        clean_database()

    def test_insert_one(self):
        token = 'ASDochTcKxrvCnqncrAcgtlyhCDwQfvbAurhqbYvJMyCUTFMTVZwYkrDbxKHwKXtzMRexjHRBvGVddCnBbpjpXqIaaPsXiaDIVCeOCJxCOCRNnxllFMNGdrBmTcphxbC'
        username =  "Test2"

        dbapi.sessions.insert({'_id': token, 'username': username})

        result = database.sessions.find_one({'_id': token})
        count = database.sessions.count()
       
        self.assertEqual(token, result['_id'])
        self.assertEqual(username, result['username'])
        self.assertEqual(count, 2)

    def test_remove_one(self):
        result = dbapi.sessions.remove(session['_id'])
        count = database.sessions.count()

        self.assertEqual(count, 0)

    def test_get(self):
        result = dbapi.sessions.get(session['_id'])

        self.assertEqual(result, session)

if __name__ == '__main__':
    unittest.main()
