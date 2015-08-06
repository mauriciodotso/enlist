from types import TupleType
from dbapi.model.basedb import BaseDB


class SeriesDB(BaseDB):
    def __init__(self, *args, **kwargs):
        if len(args) is 1 and isinstance(args, TupleType):
            args = args[0]
        elif len(args) is 3:
            args = (0, ) + args
        elif len(args) < 4:
            args = [0, 0, 0, 0, ]

        self.id = args[0]
        self.title = args[1]
        self.year = args[2]
        self.img = args[3]

    def get_tuple(self):
        return self.id, self.title, self.year, self.img

    def get_tuple_without_id(self):
        return self.title, self.year, self.img