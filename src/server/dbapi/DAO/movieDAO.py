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
    def insert(self, meal):
        pass

    @abc.abstractmethod
    def update(self, meal):
        pass

    @abc.abstractmethod
    def remove(self, id):
        pass
