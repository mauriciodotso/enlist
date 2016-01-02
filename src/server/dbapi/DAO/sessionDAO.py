import abc


class SessionDAO(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get(self, id):
        pass

    @abc.abstractmethod
    def insert(self, session):
        pass

    @abc.abstractmethod
    def update(self, session):
        pass

    @abc.abstractmethod
    def remove(self, id):
        pass

    @abc.abstractmethod
    def remove_all(self, query):
        pass
