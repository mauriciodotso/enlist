from ..DAO.baseDAO import BaseDAO


class BaseMongo(BaseDAO):
    def __init__(self, database, table):
            self.database = database
            self.table = table

    def get(self, id):
        try:
            return self.table.find_one({'_id': id})
        except Exception:
            raise Exception

    def insert(self, row):
        try:
            return self.table.insert_one(row)
        except Exception:
            raise Exception

    def update(self, row):
        try:
            return self.table.update_one({'_id': row['_id']}, {'$set': row})
        except Exception:
            raise Exception

    def remove(self, id):
        try:
            return self.table.remove({'_id': id})
        except Exception:
            raise Exception

