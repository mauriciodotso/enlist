from dbapi.daobridge.basebridge import BaseBridge


class UserMovieBridge(BaseBridge):
    def __init__(self, dao, dao_factory):
        super(UserMovieBridge, self).__init__(dao, dao_factory)