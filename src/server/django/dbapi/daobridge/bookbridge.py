from dbapi.daobridge.basebridge import BaseBridge


class BookBridge(BaseBridge):
    def __init__(self, dao, dao_factory):
        super(BookBridge, self).__init__(dao, dao_factory)