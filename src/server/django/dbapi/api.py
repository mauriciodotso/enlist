from dbapi.dao.daofactory import DAOFactory
from dbapi.daobridge.bookbridge import BookBridge
from dbapi.daobridge.moviebridge import MovieBridge
from dbapi.daobridge.seriesbridge import SeriesBridge
from dbapi.daobridge.userbridge import UserBridge
from dbapi.daobridge.userbookbridge import UserBookBridge
from dbapi.daobridge.usermoviebridge import UserMovieBridge
from dbapi.daobridge.userseriesbridge import UserSeriesBridge


class DBAPI(object):
    def __init__(self):
        self._dao_factory_ = DAOFactory()
        self.book = BookBridge(self._dao_factory_.book_dao(), self._dao_factory_)
        self.movie = MovieBridge(self._dao_factory_.movie_dao(), self._dao_factory_)
        self.series = SeriesBridge(self._dao_factory_.series_dao(), self._dao_factory_)
        self.user = UserBridge(self._dao_factory_.user_dao(), self._dao_factory_)
        self.userbook = UserBookBridge(self._dao_factory_.userbook_dao(), self._dao_factory_)
        self.usermovie = UserMovieBridge(self._dao_factory_.usermovie_dao(), self._dao_factory_)
        self.userseries = UserSeriesBridge(self._dao_factory_.userseries_dao(), self._dao_factory_)
