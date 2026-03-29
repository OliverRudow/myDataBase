"""mySQLDataBase.py."""

__title__: str = "mySQLDataBase"
__version__: str = "1.0"
__author__: str = "Oliver Rudow"
__copyright__: str = "Copyright 2024, Brain Center Höfen"

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import dataclasses
import sqlite3
from data_base_me import myTableSQL
from file_base_me import myFileBase

STR_SQL_DATA_DIR_NAME: str = '../Data'
STR_SQL_DATA_BASE_NAME: str = 'test.db'

@dataclasses.dataclass(init=False)
class MySQLDataBase:
    """
        Class for providing variables and methods for an application using SQL DataBase.
        The class is considered to comply with SQLite.
    """

    # SQL Data Base as per Ini File
    _str_sql_data_base_name: str = dataclasses.field(repr=False, default='')

    # the SQL Connection is the Python access to SQL Data Base
    _my_sql_connection: sqlite3.Connection = dataclasses.field(repr=False, default=type(sqlite3.connect))

    # the SQL Cursor is relevant to send and receive SQL Data Base Information
    _my_sql_cursor: sqlite3.Cursor = dataclasses.field(repr=False, default=type(sqlite3.Cursor))

    # Python SQLITE3 settings
    _float_sql_connection_timeout: float = dataclasses.field(repr=False, default=5.0)

    _bool_sql_connection_uri: bool = dataclasses.field(repr=False, default=True)

    # File Base
    _file_base: myFileBase.MyFileBase = dataclasses.field(repr=False, default=type(myFileBase.MyFileBase))

    def __init__(self):
        super().__init__()

        self._file_base = myFileBase.MyFileBase()

    """
        SQL Data Base Function
    """
    def set_sql_data_base_name(self, str_file_name: str) -> None:
        try:

            if str_file_name == '':

                raise ValueError

            else:

                self._file_base.set_file_name(str_file_name, False)

                self._str_sql_data_base_name = self._file_base.get_entire_file_name

                print(self._str_sql_data_base_name)

        except ValueError:

            print(f'---- ValueError in {__title__}, {self.set_sql_data_base_name.__name__}: '
                  f'init of table failed, table name is a empty string -----')

            exit(1)

    def set_sql_connection_timeout(self, float_timeout: float) -> None:
        self._float_sql_connection_timeout = float_timeout

    def set_sql_connection_uri(self, bool_uri: bool) -> None:
        self._bool_sql_connection_uri = bool_uri

    def open_sql_data_base(self) -> None:
        try:
            # open database
            self._my_sql_connection = sqlite3.connect(database=self._str_sql_data_base_name,
                                                      timeout=self._float_sql_connection_timeout,
                                                      uri=self._bool_sql_connection_uri)
            # create cursor
            self._my_sql_cursor = self._my_sql_connection.cursor()

        except sqlite3.OperationalError as e:

            print(f"Error in {__title__}, {self.open_sql_data_base.__name__}:, {e}")

    def get_sql_data_base_name(self) -> str:
        return self._str_sql_data_base_name

    def get_connection(self) -> sqlite3.Connection:
        return self._my_sql_connection

    def get_cursor(self) -> sqlite3.Cursor:
        return self._my_sql_cursor

    def close_sql_data_base(self) -> None:
        if self._my_sql_connection:

            self._my_sql_connection.close()

    def drop_sql_table(self, str_table) -> None:
        if self._my_sql_connection and self._my_sql_cursor:

            self._my_sql_cursor.execute(f'DROP TABLE IF EXISTS {str_table}')


if __name__ == "__main__":
    my_data = MySQLDataBase()
    my_data.set_sql_data_base_name(STR_SQL_DATA_BASE_NAME)
    my_data.open_sql_data_base()
    my_table_sql = myTableSQL.MyTableSQL(my_data.get_connection(), my_data.get_cursor())
    my_table_sql.set_sql_data_base_schema('main')
    my_table_sql.set_table_name('oliver')
    my_table_sql.get_sql_data_base_table_info_list()
    my_table_sql.print_sql_data_base_table_info()
    my_data.close_sql_data_base()
