from ..DAO.sessionDAO import SessionDAO
from baseMongo import BaseMongo


class SessionMongo(BaseMongo, SessionDAO):
    def __init__(self, database):
        super(SessionMongo, self).__init__(database, database.sessions)

    def remove_all(self, query):
        try:
            return self.table.remove(query)
        except Exception:
            raise Exception
