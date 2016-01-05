import abc


class BookDAO(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_all(self, limit=10, offset=0):
        pass

    @abc.abstractmethod
    def get_all_by_title(self, title, limit=10, offset=0):
        pass

    @abc.abstractmethod
    def get_all_by_user(self, user_id, limit=10, offset=0):
        pass
