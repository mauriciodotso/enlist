from types import TupleType
from dbapi.model.basedb import BaseDB


class UserMovieDB(BaseDB):
    def __init__(self, *args, **kwargs):
        if len(args) is 1 and isinstance(args, TupleType):
            args = args[0]
        elif len(args) is 3:
            args = (0, ) + args
        elif len(args) < 4:
            args = [0, 0, 0, 0, ]

        self.id = args[0]
        self.iduser = args[1]
        self.idmovie = args[2]
        self.status = args[3]

    def get_tuple(self):
        return self.id, self.iduser, self.idmovie, self.status

    def get_tuple_without_id(self):
        return self.iduser, self.idmovie, self.status