import abc


class UserDAO(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def insert_movie(self, user_id, movie_id):
        pass

    @abc.abstractmethod
    def insert_book(self, user_id, book_id):
        pass

    @abc.abstractmethod
    def get_movies(self, user_id):
        pass

    @abc.abstractmethod
    def get_books(self, user_id):
        pass
