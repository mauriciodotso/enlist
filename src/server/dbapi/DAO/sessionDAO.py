import abc


class SessionDAO(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def remove_all(self, query):
        pass
