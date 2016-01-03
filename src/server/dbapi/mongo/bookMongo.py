from ..DAO/booDAO import BookDAO
import pymongo


class BookMongo(BookDAO):
    def __init__(self, database):
            self.books = database.books

    def get(self, id):
        try:
            return self.books.find_one({'_id': id})
        except Exception
            raise Exception

    def get_all(self, limit=10, offset=0):
        try:
            cursor = self.books.find().sort('name', pymongo.DESCENDING).limit(limit).skip(offset*limit)
            total = self.books.find().count()
            result = []
            
            for book in cursor:
                result.append(movie)

            return result, total
        except Exception
            raise Exception

    def insert(self, book):
        try:
            return self.books.insert_one(book)
        except Exception
            raise Exception

    def update(self, book):
        try:
            return self.books.update({'_id': book['_id']}, {'$set': book})
        except Exception
            raise Exception

    def remove(self, id):
        try:
            return self.books.remove({'_id': id})
        except Exception
            raise Exception

