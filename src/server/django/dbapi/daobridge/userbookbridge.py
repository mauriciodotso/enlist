from dbapi.daobridge.basebridge import BaseBridge


class UserBookBridge(BaseBridge):
    def __init__(self, dao, dao_factory):
        super(UserBookBridge, self).__init__(dao, dao_factory)