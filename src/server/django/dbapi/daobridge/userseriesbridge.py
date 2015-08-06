from dbapi.daobridge.basebridge import BaseBridge


class UserSeriesBridge(BaseBridge):
    def __init__(self, dao, dao_factory):
        super(UserSeriesBridge, self).__init__(dao, dao_factory)