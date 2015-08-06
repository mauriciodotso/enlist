from dbapi.dao.basedao import BaseDAO
from dbapi.model.moviedb import MovieDB


class MovieDAO(BaseDAO):
    def __init__(self):
        super(MovieDAO, self).__init__('movie', MovieDB())
