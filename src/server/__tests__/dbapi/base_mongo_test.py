import unittest
import sys
import os
import pymongo
import datetime
import time

sys.path.insert(0, os.path.realpath('./') + '/..')

from dbapi.mongo.baseMongo import BaseMongo

connection = pymongo.MongoClient("mongodb://localhost")
database = connection.enlist_test
base_mongo = BaseMongo(database, database.base)

test = {'_id': 0, 'name': "Test", 'datetime': datetime.datetime.utcnow().replace(microsecond=0), 'year': 1900}

def clean_database():
    database.base.remove({})


class BaseMongoTest(unittest.TestCase):
    def test_insert_one(self):
        test['_id'] = base_mongo.insert({'name': test['name'], 'datetime': test['datetime'], 'year': test['year']}).inserted_id
        result = database.base.find_one({'_id': test['_id']})
       
        self.assertEqual(test['_id'], result['_id'])
        self.assertEqual(test['name'], result['name'])
        self.assertEqual(test['datetime'], result['datetime'])
        self.assertEqual(test['year'], result['year'])

        clean_database()

    def test_update_one(self):
        test['_id'] = database.base.insert_one({'name': test['name'], 'datetime': test['datetime'], 'year': test['year']}).inserted_id

        test['name'] = "Test2"
        test['year'] = 2000

        base_mongo.update(test)
        result = database.base.find_one({'_id': test['_id']})

        self.assertEqual(test['_id'], result['_id'])
        self.assertEqual(test['name'], result['name'])
        self.assertEqual(test['datetime'], result['datetime'])
        self.assertEqual(test['year'], result['year'])

        clean_database()

    def test_get(self):
        test['_id'] = database.base.insert_one({'name': test['name'], 'datetime': test['datetime'], 'year': test['year']}).inserted_id

        result = database.base.find_one({'_id': test['_id']})

        self.assertEqual(test['_id'], result['_id'])
        self.assertEqual(test['name'], result['name'])
        self.assertEqual(test['datetime'], result['datetime'])
        self.assertEqual(test['year'], result['year'])

        clean_database()

    def test_remove_one(self):
        database.base.insert_one({'name': test['name'], 'datetime': test['datetime'], 'year': test['year']}).inserted_id
        test['_id'] = database.base.insert_one({'name': test['name'], 'datetime': test['datetime'], 'year': test['year']}).inserted_id

        result = base_mongo.remove(test['_id'])
        count = database.base.count()
       
        self.assertEqual(count, 1)

        clean_database()

if __name__ == '__main__':
    unittest.main()
