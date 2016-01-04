import abc


class UserDAO(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_all_movies(self, limit=10, offset=0):
        pass

    @abc.abstractmethod
    def get_all_books(self, limit=10, offset=0):
        pass
