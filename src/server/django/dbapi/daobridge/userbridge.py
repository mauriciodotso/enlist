from dbapi.daobridge.basebridge import BaseBridge


class UserBridge(BaseBridge):
    def __init__(self, dao, dao_factory):
        super(UserBridge, self).__init__(dao, dao_factory)