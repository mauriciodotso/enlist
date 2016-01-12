from flask import json
import unittest
import pymongo
import os
import sys
import datetime
import time
import json

sys.path.insert(0, os.path.realpath('./') + '/..')

from dbapi.api import DBAPI
import urls
import api_messages

connection = pymongo.MongoClient("mongodb://localhost")
database = connection.caloriescountertest
dbapi = DBAPI(database=database)

def clean_database():
    database.sessions.remove({})
    database.users.remove({})
    database.meals.remove({})

class RestAPITest(unittest.TestCase):
    def setUp(self):
        urls.app.config['TESTING'] = True
        urls.test_database(database)
        self.app = urls.app.test_client()

    def tearDown(self):
        clean_database()

    def test_login(self):
        username = "Test"
        password = "123456"
        role = 0
        goal =  2000

        dbapi.users.insert({'_id': username, 'password': password, 'role': role, 'goal': goal})

        resp = self.app.post('/login', data=json.dumps(dict({'username': username, 'password': password})), content_type='application/json')

        self.assertEqual(resp.status_code, 200)
    
        clean_database()

    def test_logout(self):
        token = 'ATDochTcKxrvCnqncrAcgtlyhCDwQfvbAurhqbYvJMyCUTFMTVZwYkrDbxKHwKXtzMRexjHRBvGVddCnBbpjpXqIaaPsXiaDIVCeOCJxCOCRNnxllFMNGdrBmTcphxbC'
        username =  "Test"

        dbapi.sessions.insert({'_id': token, 'username': username})

        resp = self.app.post('/logout', data=json.dumps(dict({'token': token})), content_type='application/json')

        self.assertEqual(resp.status_code, 200)
    
        clean_database()


    def test_create_user(self):
        username = "Test"
        password = "123456"
        role = 0
        goal =  2000

        resp = self.app.put('/user/create', data=json.dumps(dict({'username': username, 'password': password, 'goal': goal})), content_type='application/json')

        self.assertEqual(resp.status_code, 201)

        clean_database()

    def test_update_user(self):
        #Todo
        self.assertEqual(1, 1)

    def test_create_meal(self):
        username = "Test"
        password = "123456"
        role = 0
        goal =  2000

        dbapi.users.insert({'_id': username, 'password': password, 'role': role, 'goal': goal})

        token = 'ATDochTcKxrvCnqncrAcgtlyhCDwQfvbAurhqbYvJMyCUTFMTVZwYkrDbxKHwKXtzMRexjHRBvGVddCnBbpjpXqIaaPsXiaDIVCeOCJxCOCRNnxllFMNGdrBmTcphxbC'

        dbapi.sessions.insert({'_id': token, 'username': username})
        
        text = "Meal"
        meal_datetime = datetime.datetime.utcnow()
        meal_datetime = meal_datetime.replace(microsecond=0)
        iduser = 'Test'
        cal = 100
       
        resp = self.app.post('/meal/create', data=json.dumps(dict({'token': token,'username': username,'text': text, 'cal': cal, 'date': '01/01/1991','time': '00:00'})), content_type='application/json')

        self.assertEqual(resp.status_code, 201)

        clean_database()

    def test_update_meal(self):
        username = "Test"
        password = "123456"
        role = 0
        goal =  2000

        dbapi.users.insert({'_id': username, 'password': password, 'role': role, 'goal': goal})

        token = 'ATDochTcKxrvCnqncrAcgtlyhCDwQfvbAurhqbYvJMyCUTFMTVZwYkrDbxKHwKXtzMRexjHRBvGVddCnBbpjpXqIaaPsXiaDIVCeOCJxCOCRNnxllFMNGdrBmTcphxbC'

        dbapi.sessions.insert({'_id': token, 'username': username})

        text = "Meal"
        meal_datetime = datetime.datetime.utcnow()
        meal_datetime = meal_datetime.replace(microsecond=0)
        iduser = 'Test'
        cal = 100

        meal_id = dbapi.meals.insert({'iduser': iduser,'text': text, 'datetime': meal_datetime, 'cal': cal}).inserted_id

        newText = '654321'
        newDatetime = meal_datetime.replace(hour=(meal_datetime.hour + 2)%24)
        newCal = 9000

        resp = self.app.post('/meal/update', data=json.dumps(dict({'token': token,'_id': str(meal_id),'text': newText, 'cal': newCal, 'date': '01/01/1991','time': '00:00'})), content_type='application/json')

        self.assertEqual(resp.status_code, 200)

        clean_database()

    def test_delete_meal(self):
        #Todo
        self.assertEqual(1, 1)

    def test_get_all_meals(self):
        username = "Test"
        password = "123456"
        role = 0
        goal =  2000

        dbapi.users.insert({'_id': username, 'password': password, 'role': role, 'goal': goal})

        token = 'ATDochTcKxrvCnqncrAcgtlyhCDwQfvbAurhqbYvJMyCUTFMTVZwYkrDbxKHwKXtzMRexjHRBvGVddCnBbpjpXqIaaPsXiaDIVCeOCJxCOCRNnxllFMNGdrBmTcphxbC'

        dbapi.sessions.insert({'_id': token, 'username': username})

        text = "Meal"
        iduser = 'Test'
        cal = 100
        limit = 10
        total = 15
        meals = []

        for i in xrange(total):
            meal_datetime = datetime.datetime.utcnow()
            meal_datetime = meal_datetime.replace(microsecond=0)
            cal += 10
            meal = {'iduser': iduser,'text': text + str(i), 'datetime': meal_datetime, 'cal': cal}
            
            database.meals.insert(meal)
            meal['_id'] = str(meal['_id'])
            meal['datetime'] = str(meal['datetime'])
            
            meals.append(meal)
            time.sleep(1)

        resp = self.app.post('/meal/all', data=json.dumps(dict({'token': token,'username': username})), content_type='application/json')
        result = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(result['meals']), limit)

        for i in xrange(total - 1, (total - 1) - limit, -1):
            self.assertEqual(meals[i], result['meals'][total - 1 - i])
    
        resp = self.app.post('/meal/all', data=json.dumps(dict({'token': token,'username': username, 'page': 1})), content_type='application/json')
        result = json.loads(resp.data)

        self.assertEqual(len(result['meals']), min((total - limit), limit))

        for i in xrange(max((total - limit) - 1, 0), max((total - 1) - 2*limit, 0), -1):
            self.assertEqual(meals[i], result['meals'][(total - limit - 1) - i])

        clean_database()

if __name__ == "__main__":
    unittest.main()
