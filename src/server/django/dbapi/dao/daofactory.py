from dbapi.dao.bookdao import BookDAO
from dbapi.dao.moviedao import MovieDAO
from dbapi.dao.seriesdao import SeriesDAO
from dbapi.dao.userdao import UserDAO
from dbapi.dao.userbookdao import UserBookDAO
from dbapi.dao.usermoviedao import UserMovieDAO
from dbapi.dao.userseriesdao import UserSeriesDAO


class DAOFactory(object):
    def __init__(self):
        self._book_dao_ = None
        self._movie_dao_ = None
        self._series_dao_ = None
        self._user_dao_ = None
        self._userbook_dao_ = None
        self._usermovie_dao_ = None
        self._userseries_dao_ = None

    def book_dao(self):
        if not self._book_dao_:
            self._book_dao_ = BookDAO()

        return self._book_dao_

    def movie_dao(self):
        if not self._movie_dao_:
            self._movie_dao_ = MovieDAO()

        return self._movie_dao_

    def series_dao(self):
        if not self._series_dao_:
            self._series_dao_ = SeriesDAO()

        return self._series_dao_

    def user_dao(self):
        if not self._user_dao_:
            self._user_dao_ = UserDAO()

        return self._user_dao_

    def userbook_dao(self):
        if not self._userbook_dao_:
            self._userbook_dao_ = UserBookDAO()

        return self._userbook_dao_

    def usermovie_dao(self):
        if not self._usermovie_dao_:
            self._usermovie_dao_ = UserMovieDAO()

        return self._usermovie_dao_

    def userseries_dao(self):
        if not self._userseries_dao_:
            self._userseries_dao_ = UserSeriesDAO()

        return self._userseries_dao_

