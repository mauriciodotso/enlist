from dbapi.dao.basedao import BaseDAO
from dbapi.model.bookdb import BookDB


class BookDAO(BaseDAO):
    def __init__(self):
        super(BookDAO, self).__init__('book', BookDB())
