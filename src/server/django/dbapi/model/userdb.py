from types import TupleType
from dbapi.model.basedb import BaseDB


class UserDB(BaseDB):
    def __init__(self, *args, **kwargs):
        if len(args) is 1 and isinstance(args, TupleType):
            args = args[0]
        elif len(args) is 0:
            args = (0, ) + args
        elif len(args) < 1:
            args = [0, ]

        self.id = args[0]

    def get_tuple(self):
        return self.id,

    def get_tuple_without_id(self):
        return 