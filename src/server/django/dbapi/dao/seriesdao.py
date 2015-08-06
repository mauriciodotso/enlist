from dbapi.dao.basedao import BaseDAO
from dbapi.model.seriesdb import SeriesDB


class SeriesDAO(BaseDAO):
    def __init__(self):
        super(SeriesDAO, self).__init__('series', SeriesDB())
