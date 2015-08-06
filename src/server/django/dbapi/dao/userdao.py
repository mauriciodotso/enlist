from dbapi.dao.basedao import BaseDAO
from dbapi.model.userdb import UserDB


class UserDAO(BaseDAO):
    def __init__(self):
        super(UserDAO, self).__init__('user', UserDB())
