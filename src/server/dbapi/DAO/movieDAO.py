import abc


class MovieDAO(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get(self, id):
        pass

    @abc.abstractmethod
    def get_all(self, limit=10, offset=0):
        pass

    @abc.abstractmethod
    def insert(self, movie):
        pass

    @abc.abstractmethod
    def update(self, movie):
        pass

    @abc.abstractmethod
    def remove(self, id):
        pass
