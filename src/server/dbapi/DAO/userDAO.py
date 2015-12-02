import abc


class UserDAO(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get(self, id):
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
