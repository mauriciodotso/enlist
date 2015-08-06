# coding=utf-8
import mysql.connector
import os
import re
from dbapi.dao import db_config

__author__ = 'nakayama'


def execute_query(query, data, connection):
    cursor = connection.cursor()
    cursor.execute(query, data)

    return cursor


def get_query(query, data):
        connection = mysql.connector.connect(**db_config)

        cursor = execute_query(query, data, connection)

        result_list = []

        for result in cursor:
            result_list.append(result)

        cursor.close()
        connection.close()

        return result_list


def setup_parameters(is_update):
    query = ("SHOW TABLES")

    table_list = get_query(query, ())

    dbapi_string_header = "from dbapi.dao.daofactory import DAOFactory\n"
    dbapi_string = "class DBAPI(object):\n"
    dbapi_string += "    def __init__(self):\n"
    dbapi_string += "        self._dao_factory_ = DAOFactory()\n"

    dao_string_header = ""
    dao_string = "class DAOFactory(object):\n"
    dao_string += "    def __init__(self):\n"
    dao_string_body = ""

    for table in table_list:
        table_title = str(table[0]).title()
        table_title = re.sub('_', '', table_title)
        table_name = table[0]
        table = re.sub('_', '', str(table[0]))

        query = ("SELECT `COLUMN_NAME` " +
            " FROM `INFORMATION_SCHEMA`.`COLUMNS` " +
            " WHERE `TABLE_SCHEMA` = %s " +
            " AND `TABLE_NAME` = %s ")

        column_list = (get_query(query, (db_config['database'], table_name)))
        column_tuple = ()
        column_len = len(column_list)
        args = ""
        args_index = 0
        args_array = "["

        for column in column_list:
            if not str(column[0]) == 'id':
                column_tuple += ("self." + str(column[0]), )
            args += "        self." + str(column[0]) + " = args[" + str(args_index) + "]\n"
            args_index += 1
            args_array += "0, "

        args_array += "]"
        column_tuple_id = ('self.id',) + column_tuple

        if not (("auth" in table or "django" in table) or (os.path.isfile("../../dbapi/model/" + table + "db.py"))) or not is_update:
            dao_file = open("../../dbapi/dao/" + table + "dao.py", 'w+')

            string = "from dbapi.dao.basedao import BaseDAO\n"
            string += "from dbapi.model." + table + "db import " + table_title + "DB\n\n\n"
            string += "class " + table_title + "DAO(BaseDAO):\n"
            string += "    def __init__(self):\n"
            string += "        super(" + table_title + "DAO, self).__init__('" + table_name + "', " + table_title + "DB())\n"

            dao_file.write(string)
            dao_file.close()

            bridge_file = open("../../dbapi/daobridge/" + table + "bridge.py", 'w+')

            string = "from dbapi.daobridge.basebridge import BaseBridge\n\n\n"
            string += "class " + table_title + "Bridge(BaseBridge):\n"
            string += "    def __init__(self, dao, dao_factory):\n"
            string += "        super(" + table_title + "Bridge, self).__init__(dao, dao_factory)"

            bridge_file.write(string)
            bridge_file.close()

        if not ("auth" in table or "django" in table):
            model_file = open("../../dbapi/model/" + table + "db.py", 'w+')

            string = "from types import TupleType\n"
            string += "from dbapi.model.basedb import BaseDB\n\n\n"
            string += "class " + table_title + "DB(BaseDB):\n"
            string += "    def __init__(self, *args, **kwargs):\n"
            string += "        if len(args) is 1 and isinstance(args, TupleType):\n"
            string += "            args = args[0]\n"
            string += "        elif len(args) is " + str((column_len - 1)) + ":\n"
            string += "            args = (0, ) + args\n"
            string += "        elif len(args) < " + str(column_len) + ":\n"
            string += "            args = " + args_array + "\n\n"
            string += args + "\n"
            string += "    def get_tuple(self):\n"
            string += "        return " + re.sub('\)', '', re.sub('\(', '', re.sub("'", "", str(column_tuple_id)))) + "\n\n"
            string += "    def get_tuple_without_id(self):\n"
            string += "        return " + re.sub('\)', '', re.sub('\(', '', re.sub("'", "", str(column_tuple))))

            model_file.write(string)
            model_file.close()

            dbapi_string_header += "from dbapi.daobridge." + table + "bridge import " + table_title + "Bridge\n"
            dbapi_string += "        self." + table + " = " + table_title + "Bridge(self._dao_factory_." + table + "_dao(), self._dao_factory_)\n"

            dao_string_header += "from dbapi.dao." + table + "dao import " + table_title + "DAO\n"
            dao_string += "        self._" + table + "_dao_ = None\n"
            dao_string_body += "    def " + table + "_dao(self):\n"
            dao_string_body += "        if not self._" + table + "_dao_:\n"
            dao_string_body += "            self._" + table + "_dao_ = " + table_title + "DAO()\n"
            dao_string_body += "\n"
            dao_string_body += "        return self._" + table + "_dao_\n\n"

    dao_string_header += "\n\n"
    dbapi_string_header += "\n\n"

    dao_string += "\n"

    dbapi_file = open("../../dbapi/api.py", 'w+')
    dbapi_file.write(dbapi_string_header)
    dbapi_file.write(dbapi_string)
    dbapi_file.close()

    dao_file = open("../../dbapi/dao/daofactory.py", 'w+')
    dao_file.write(dao_string_header)
    dao_file.write(dao_string)
    dao_file.write(dao_string_body)
    dao_file.close()


    #ToDo: Deletar arquivos de tabelas que não existem mais