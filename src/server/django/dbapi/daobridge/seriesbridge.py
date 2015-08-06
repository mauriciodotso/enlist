from dbapi.daobridge.basebridge import BaseBridge


class SeriesBridge(BaseBridge):
    def __init__(self, dao, dao_factory):
        super(SeriesBridge, self).__init__(dao, dao_factory)