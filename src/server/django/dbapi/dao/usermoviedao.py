from dbapi.dao.basedao import BaseDAO
from dbapi.model.usermoviedb import UserMovieDB


class UserMovieDAO(BaseDAO):
    def __init__(self):
        super(UserMovieDAO, self).__init__('user_movie', UserMovieDB())
