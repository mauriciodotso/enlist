from ..DAO.sessionDAO import SessionDAO

class SessionMongo(SessionDAO):
    def __init__(self, database):
        self sessions = database.sessions

    def get(self, id):
        try:
            return self.sessions.find_one({"_id": id})
        except Exception:
            raise Exception

    def insert(self, session):
        try:
            return self.sessions.insert_one(session)
        except Exception:
            raise Exception

    def update(self, session):
        try:
            return self.sessions.update({'$set': session})
        except Exception:
            raise Exception

    def remove(self, id):
        try:
            return self.sessions.remove({'_id': id})
        except Exception:
            raise Exception

    def remove_all(self, query):
        try:
            return self.sessions.remove(query)
        except Exception:
            raise Exception
	
	
