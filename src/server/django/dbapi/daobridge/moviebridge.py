from dbapi.daobridge.basebridge import BaseBridge


class MovieBridge(BaseBridge):
    def __init__(self, dao, dao_factory):
        super(MovieBridge, self).__init__(dao, dao_factory)