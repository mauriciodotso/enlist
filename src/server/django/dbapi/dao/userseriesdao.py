from dbapi.dao.basedao import BaseDAO
from dbapi.model.userseriesdb import UserSeriesDB


class UserSeriesDAO(BaseDAO):
    def __init__(self):
        super(UserSeriesDAO, self).__init__('user_series', UserSeriesDB())
