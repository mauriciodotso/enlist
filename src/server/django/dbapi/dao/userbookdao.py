from dbapi.dao.basedao import BaseDAO
from dbapi.model.userbookdb import UserBookDB


class UserBookDAO(BaseDAO):
    def __init__(self):
        super(UserBookDAO, self).__init__('user_book', UserBookDB())
