import abc


class BookDAO(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_all(self, limit=10, offset=0):
        pass

    @abc.abstractmethod
    def get_all_by_title(self, limit=10, offset=0):
        pass
