"""myTableSQL.py."""

__title__: str = "myTableSQL"
__version__: str = "0.3.0"
__author__: str = "Oliver Rudow"
__email__: str = "oliver.rudow@googlemail.com"
__copyright__: str = "Copyright 2024, Brain Center Höfen"

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import dataclasses
import sqlite3
from typing import Any, Optional
from mydatabase import myTableBase
from myauxiliary import myAuxiliary

"""
    SQL PRAGMA TABLE LIST: Tuple Definition
"""
TABLE_LIST_SCHEMA = 0
TABLE_LIST_TABLE_NAME = 1
TABLE_LIST_TABLE_TYPE = 2  # table or view
TABLE_LIST_NUMBER_COLUMNS = 3
TABLE_LIST_FLAG_ROWID = 4
TABLE_LIST_FLAG_STRICT_OPTION = 5

"""
    SQL PRAGMA TABLE INFO: Tuple Definition
"""
TABLE_INFO_NUMBER_COLUMN = 0
TABLE_INFO_NAME_COLUMN = 1
TABLE_INFO_TYPE_COLUMN = 2  # TEXT, INTEGER, BLOB
TABLE_INFO_FLAG_NOT_NULL = 3
TABLE_INFO_DEFAULT_VALUE = 4
TABLE_INFO_FLAG_PRIMARY_KEY = 5


@dataclasses.dataclass(init=False)
class MyTableSQL(myTableBase.MyTableBase):
    """
        Class for providing variables and methods for an application based on SQL DataBase.
        The class is considered to comply with SQLite.

    """
    # the SQL Connection is the Python access to SQL Data Base
    _my_sql_connection: sqlite3.Connection = dataclasses.field(repr=False, default = type(sqlite3.connect))

    # the SQL Cursor is relevant to send and receive SQL Data Base Information
    _my_sql_cursor: sqlite3.Cursor = dataclasses.field(repr=False, default_factory = type(sqlite3.Cursor))

    # SQL Data Base Schema holding the relevant Tables
    _str_sql_schema: str = dataclasses.field(repr=False, default='')

    # SQL Table Names
    _dict_sql_table_names: dict[str, str] = dataclasses.field(repr=False, default=dict[str, str])

    # SQL Given Table Names
    _list_sql_given_tables_names: list[tuple] = dataclasses.field(repr=False, default_factory = list[tuple])

    _int_sql_number_of_tables_in_schema: int = dataclasses.field(repr=False, default=0)

    # Python SQLITE3 settings
    _list_given_sql_table_info: list[tuple] = dataclasses.field(repr=False, default_factory = list[tuple])

    _int_sql_table_row_number: int = dataclasses.field(repr=False, default=0)

    # check Table for completeness
    _bool_sql_data_base_table: bool = dataclasses.field(repr=False, default=False)

    # data frame row index for getting and putting a line
    _int_table_put_row_index: int = dataclasses.field(repr=False, default=0)

    _int_table_get_row_index: int = dataclasses.field(repr=False, default=0)

    def __init__(self,
                 the_sql_connection: sqlite3.Connection,
                 the_sql_cursor: sqlite3.Cursor):
        super().__init__()

        self._my_sql_connection = the_sql_connection

        self._my_sql_cursor = the_sql_cursor

        self._dict_sql_table_names  = {}

        self._list_sql_given_tables_names = []

        self._list_given_sql_table_info = []

    """
        manage SQL Database
    """

    @property
    def get_sql_schema(self) -> str:

        return self._str_sql_schema

    @property
    def get_table_sql_bool(self) -> bool:

        return self._bool_sql_data_base_table

    @property
    def _get_sql_alive(self) -> bool:

        if self._my_sql_connection and self._my_sql_cursor:

            return True

        else:

            return False


    def set_sql_data_base_schema(self, str_schema: str) -> None:

        self._str_sql_schema = str_schema

    def set_sql_dict_table_names(self, dict_sql_table_names: dict[str, str]) -> None:

        self._dict_sql_table_names = dict_sql_table_names

    def get_sql_data_base_table_list(self) -> None:
        """
            this function provides a list of tuples giving information about the tables belonging to the specified
            schema.

            the tuples are organized as follows:
            0. schema
            1. name of table
            2. type of table (table or view)
            3. number of columns
            4. flag indicating a WITHOUT ROWID
            5. flag indicating the STRICT option

            finally, the function evaluates the number of tables belonging to the specified schema.

            the output:
            _listGivenSQLTablesNames
            _intNumberOfTablesInSchema
        """
        if self._my_sql_connection and self._my_sql_cursor:

            self._int_sql_number_of_tables_in_schema = 0

            str_text = f'PRAGMA {self._str_sql_schema}.table_list'

            try:

                self._my_sql_cursor.execute(str_text)

                # table list as tuples
                self._list_sql_given_tables_names = self._my_sql_cursor.fetchall()

            except sqlite3.OperationalError as err:

                print(f'---- Operational Error in {__title__}, {self.get_sql_data_base_table_list.__name__} ----, \n'
                      f'---- the Text {str_text} has caused an Error {err} ! ----')

                exit(1)

            # number of tables in schema
            for num in range(self._list_sql_given_tables_names.__len__()):

                if (self._list_sql_given_tables_names[num][TABLE_LIST_SCHEMA] == self._str_sql_schema and
                        self._list_sql_given_tables_names[num][TABLE_LIST_TABLE_TYPE] == 'table'):

                    self._int_sql_number_of_tables_in_schema += 1

            self._my_sql_connection.commit()

    def get_sql_set_of_tables(self, str_table_name_starts_with: str) -> list[str]:
        list_tables = []

        self.get_sql_data_base_table_list()

        if self._int_sql_number_of_tables_in_schema > 0 and str_table_name_starts_with != '':

            for elem in self._list_sql_given_tables_names:

                str_table_name = elem[1]

                if myAuxiliary.check_date_in_object_name(str_table_name):

                    if str_table_name.startswith(str_table_name_starts_with):

                        list_tables.append(str_table_name)

            list_tables.sort(reverse=True)

        return list_tables

    def clean_preceded_tables(self, str_table_name_starts_with: str) -> None:

        list_tables = self.get_sql_set_of_tables(str_table_name_starts_with)

        while list_tables.__len__() > self._int_number_preceded_tables:

            self.drop_sql_table(list_tables[-1])

            del list_tables[-1]

    def check_sql_data_base_table_exists(self, str_table_name: Optional[str] = None) -> bool:

        if str_table_name is None:

            _str_table_name = self._str_table_name

        else:

            _str_table_name = str_table_name

        if self._list_sql_given_tables_names.__len__() == 0:

            self.get_sql_data_base_table_list()

        bool_result = False

        for num in range(self._list_sql_given_tables_names.__len__()):

            if (self._list_sql_given_tables_names[num][TABLE_LIST_TABLE_NAME] == _str_table_name and
                    self._list_sql_given_tables_names[num][TABLE_LIST_TABLE_TYPE] == 'table'):

                bool_result = True

        return bool_result

    def get_sql_data_base_table_info_list(self, str_table_name: Optional[str] = None) -> None:
        """
            the function provides a list of tuples giving information about the columns of a specified table.

            The tuples are organized as follows:
            0. Number of columns
            1. Name of column
            2. Type of column (TEXT, INTEGER, BLOB, ...)
            3. Flag "notnull"
            4. Default value
            5. Flag PRIMARY KEY

            Output:
            _listGivenSQLTableInfo
        """
        if str_table_name is None:

            str_text = f'PRAGMA table_info("{self._str_table_name}")'

        else:

            str_text = f'PRAGMA table_info("{str_table_name}")'

        if self._my_sql_connection and self._my_sql_cursor:

            try:

                self._my_sql_cursor.execute(str_text)

                self._list_given_sql_table_info = self._my_sql_cursor.fetchall()

                self._my_sql_connection.commit()

            except sqlite3.OperationalError as err:

                print(f'---- Operational Error in {__title__}, {self.get_sql_data_base_table_info_list.__name__} ----, \n'
                      f'---- the Text {str_text} has caused an Error {err} ! ----')

                exit(1)

    def check_sql_data_base_table_is_not_empty(self, str_table_name: Optional[str] = None) -> bool:
        """
            Function checks whatever a given SQL table is empty or not
        """
        if str_table_name is None:

            str_sql_data_base_check_empty_table = (
                f'SELECT exists (SELECT 1 FROM{self._str_table_name})')

        else:

            str_sql_data_base_check_empty_table = (
                f'SELECT exists (SELECT 1 FROM{str_table_name})')

        if self._my_sql_connection and self._my_sql_cursor:

            try:

                response = self._my_sql_cursor.execute(str_sql_data_base_check_empty_table)

                result = response.fetchone()

            except sqlite3.OperationalError as err:

                print(f'---- Operational Error in {__title__}, {self.check_sql_data_base_table_is_not_empty.__name__} ----, \n'
                      f'---- the Text {str_sql_data_base_check_empty_table} has caused an Error {err} ! ----')

                exit(1)

            if result[0] == 0:

                return False

            else:

                return True

        else:

            return False

    def check_sql_data_base_table_column_name(self, str_column: str, str_table_name: Optional[str] = None) -> bool:

        if str_table_name is None:

            self.get_sql_data_base_table_info_list()

        else:

            self.get_sql_data_base_table_info_list(str_table_name)

        bool_result = False

        for num in range(self._list_given_sql_table_info.__len__()):

            if self._list_given_sql_table_info[num][TABLE_INFO_NAME_COLUMN] == str_column:

                bool_result = True

        return bool_result

    def check_sql_data_base_table_all_column_names(self, list_column_names: list[str]) -> bool:

        bool_result = True

        for elem in list_column_names:

            bool_result = bool_result and self.check_sql_data_base_table_column_name(elem)

        return bool_result

    def create_sql_data_base_table(self, str_table_name: Optional[str] = None) -> None:

        if str_table_name is None:

            _str_table_name = self._str_table_name

        else:

            _str_table_name = str_table_name

        # get string for table definitions
        my_list = []

        for elem in self._list_table_column_keys:
            # get tuple
            my_tuple = self._dict_table_settings[elem]

            # joint tuple to string with whitespace
            my_list.append(' '.join(my_tuple))

        # joint list to string with comma separator
        str_table_definition = ', '.join(my_list)

        # create table
        if self._my_sql_connection and self._my_sql_cursor:

            str_text = (f'CREATE TABLE IF NOT EXISTS {self._str_sql_schema}.{_str_table_name}'
                       f'({str_table_definition})')

            try:

                self._my_sql_cursor.execute(str_text)

                self._my_sql_connection.commit()

            except sqlite3.OperationalError as err:

                print(f'---- Operational Error in {__title__}, {self.create_sql_data_base_table.__name__} ----, \n'
                      f'---- the Text {str_text} has caused an Error {err} ! ----')

                exit(1)

    def delete_sql_data_base_rows(self, str_table_name: str, str_column_name: str, str_column_content: str) -> None:

        str_text = f'DELETE from {self._str_sql_schema}.{str_table_name} WHERE {str_column_name} = "{str_column_content}"'

        if self._my_sql_connection and self._my_sql_cursor:

            try:

                self._my_sql_cursor.execute(str_text)

                self._my_sql_connection.commit()

            except sqlite3.OperationalError as err:

                print(f'---- Operational Error in {__title__}, {self.delete_sql_data_base_rows.__name__} ----, \n'
                      f'---- the Text {str_text} has caused an Error {err} ! ----')

                exit(1)

    def drop_sql_table(self, *argv) -> None:
        str_table_name = ''

        if argv.__len__() == 0:

            str_table_name = self._str_table_name

        elif argv.__len__() == 1:

            if isinstance(argv, tuple):

                str_table_name = argv[0]

            elif isinstance(argv, str):

                str_table_name = argv

        str_text = f'DROP TABLE IF EXISTS {str_table_name}'

        if self._get_sql_alive:

            try:

                self._my_sql_cursor.execute(str_text)

            except sqlite3.OperationalError as err:

                print(f'---- Operational Error in {__title__}, {self.drop_sql_table.__name__} ----, \n'
                      f'---- the Text {str_text} has caused an Error {err} ! ----')

                exit(1)

    def update_table_put_row_index(self) -> None:

        str_text = f'SELECT ROWID FROM {self._str_table_name} ORDER BY ROWID DESC LIMIT 1'

        result = 0

        if self._get_sql_alive:

            try:

                self._my_sql_cursor.execute(str_text)

                result = self._my_sql_cursor.fetchone()

                self._my_sql_connection.commit()

            except sqlite3.OperationalError as err:

                print(f'---- Operational Error in {__title__}, {self.update_table_put_row_index.__name__} ----, \n'
                      f'---- the Text {str_text} has caused an Error {err} ! ----')

                exit(1)

        self._int_table_put_row_index = result[0] + 1

    def print_sql_data_base_table_info(self) -> None:

        print(self._list_given_sql_table_info)

    def close_sql_data_base(self) -> None:

        self._my_sql_connection.close()

    """
        work with SQL Database
    """

    def get_column_index_from_sql_pragma_list(self, str_column_name: str) -> int | None:
        if self._list_given_sql_table_info.__len__() == 0:

            self.get_sql_data_base_table_info_list()

        for elem in self._list_given_sql_table_info:

            if str_column_name in elem:

                return elem[TABLE_INFO_NUMBER_COLUMN]

        return None

    def get_table_single_column_from_data_frame(self, str_column_name: str) -> list[Any]:
        my_list: list[str] = []

        str_text = f"SELECT {str_column_name} FROM {self._str_table_name}"

        if self._my_sql_connection and self._my_sql_cursor:

            try:

                self._my_sql_cursor.execute(str_text)

                result = self._my_sql_cursor.fetchall()

            except sqlite3.OperationalError as err:

                print(f'---- Operational Error in {__title__}, '
                      f'{self.get_table_single_column_from_data_frame.__name__} ----, \n'
                      f'---- the Text {str_text} has caused an Error {err} ! ----')

                exit(1)

            for elem in result:
                my_list.append(elem[0])

        return my_list

    def set_table_single_column_into_data_frame(self, str_column_name: str, list_objects: list[Any]) -> None:

        str_sql_data_base_insert = (f'INSERT OR IGNORE INTO {self._str_sql_schema}.{self._str_table_name} '
                                f'({str_column_name}) VALUES (?)')

        if self._my_sql_connection and self._my_sql_cursor:

            if not list_objects.__len__() == 0:

                try:

                    for elem in list_objects:

                        tuple_elem = tuple([elem])

                        self._my_sql_cursor.execute(str_sql_data_base_insert, tuple_elem)

                    self._my_sql_connection.commit()

                except sqlite3.OperationalError as err:

                    print(
                        f'---- Operational Error in {__title__}, '
                        f'{self.set_table_single_column_into_data_frame.__name__} ----, \n'
                        f'---- the Text {str_sql_data_base_insert} has caused an Error {err} ! ----')

                    exit(1)

    def set_table_entire_row(self, str_insert_string: str, tuple_entire_row: tuple[Any, ...]) -> None:
        try:

            if tuple_entire_row.__len__() == 0:

                raise ValueError(f'----- Value Error {__title__}, {self.set_table_entire_row.__name__}, '
                                 f'Data Base {self._str_table_name}: Input Line {tuple_entire_row} to '
                                 f'Data Output is empty -----')

            if tuple_entire_row.__len__() != self._int_table_columns_number:

                raise ValueError(f'----- Value Error {__title__}, {self.set_table_entire_row.__name__},'
                                 f'Data Base {self._str_table_name}: Input Line {tuple_entire_row} '
                                 f'to Data Output is corrupt -----')

            if self._my_sql_connection and self._my_sql_cursor:

                self._my_sql_cursor.execute(str_insert_string, tuple_entire_row)

                # update last rowid of SQL table
                if self._my_sql_cursor.lastrowid is not None:

                    self._int_table_put_row_index = self._my_sql_cursor.lastrowid + 1

                self._my_sql_connection.commit()

        except ValueError as e:

            print(e)

            exit(1)

    def get_table_entire_row(self, int_row_id: int, flag_with_row_id: bool) -> tuple:

        str_offset = str(int_row_id - 1)

        tuple_result = ()

        if flag_with_row_id:

            str_text = (f'SELECT ROWID, * FROM {self._str_sql_schema}.{self._str_table_name} ORDER BY ROWID LIMIT 1 '
                       f'OFFSET {str_offset}')

        else:

            str_text = (f'SELECT * FROM {self._str_sql_schema}.{self._str_table_name} ORDER BY ROWID LIMIT 1 '
                       f'OFFSET {str_offset}')

        if self._my_sql_connection and self._my_sql_cursor:

            try:

                self._my_sql_cursor.execute(str_text)

                tuple_result = self._my_sql_cursor.fetchone()

                self._my_sql_connection.commit()

            except sqlite3.OperationalError as err:

                print(
                    f'---- Operational Error in {__title__}, {self.get_table_entire_row.__name__} ----, \n'
                    f'---- the Text {str_text} has caused an Error {err} ! ----')

                exit(1)

        return tuple_result

    def get_column_names(self) -> list:

        list_dict_keys = []

        for i in range(self._list_given_sql_table_info.__len__()):
            list_dict_keys.append(self._list_given_sql_table_info[i][1])

        return list_dict_keys

    def get_table_all_data(self) -> list:

        list_result = []

        str_text = f'SELECT * FROM {self._str_sql_schema}.{self._str_table_name}'

        if self._get_sql_alive:

            try:

                self._my_sql_cursor.execute(str_text)

                list_result = self._my_sql_cursor.fetchall()

                self._my_sql_connection.commit()

            except sqlite3.OperationalError as err:

                print(
                    f'---- Operational Error in {__title__}, {self.get_table_all_data.__name__} ----, \n'
                    f'---- the Text {str_text} has caused an Error {err} ! ----')

                exit(1)

        return list_result

    def get_table_all_data_as_list_of_dicts(self) -> list:

        list_result = self.get_table_all_data()

        list_dict_keys = self.get_column_names()

        list_dicts = []

        for i in range(list_result.__len__()):
            list_dicts.append(dict(zip(list_dict_keys, list(list_result[i]))))

        return list_dicts

    def get_table_entire_column(self, str_column_name: str) -> list:

        list_result = []

        str_text = f'SELECT {str_column_name} FROM {self._str_sql_schema}.{self._str_table_name}'

        if self._my_sql_connection and self._my_sql_cursor:

            try:

                self._my_sql_cursor.execute(str_text)

                list_result = self._my_sql_cursor.fetchall()

                self._my_sql_connection.commit()

            except sqlite3.OperationalError as err:

                print(
                    f'---- Operational Error in {__title__}, {self.get_table_entire_column.__name__} ----, \n'
                    f'---- the Text {str_text} has caused an Error {err} ! ----')

                exit(1)

        for i in range(list_result.__len__()):

            list_result[i] = list_result[i][0]

        return list_result

    def get_table_number_rows(self, str_table_name: Optional[str] = None) -> int:

        if str_table_name is not None:

            if not str_table_name == '':

                _str_table_name = str_table_name

            else:

                _str_table_name = self._str_table_name

        else:

            _str_table_name = self._str_table_name

        str_text = f'SELECT COUNT(*) FROM {self._str_sql_schema}.{_str_table_name}'

        if self._my_sql_connection and self._my_sql_cursor:

            try:

                self._my_sql_cursor.execute(str_text)

                list_result = self._my_sql_cursor.fetchall()

                self._my_sql_connection.commit()

            except sqlite3.OperationalError as err:

                print(
                    f'---- Operational Error in {__title__}, {self.get_table_number_rows.__name__} ----, \n'
                    f'---- the Text {str_text} has caused an Error {err} ! ----')

                exit(1)

            if list_result.__len__() > 0:

                return list_result[0][0]

            else:

                return 0

        else:

            return 0

    def group_table_column_as_histogram(self, str_column_name: str, bool_order_result_desc: Optional[bool] = None) -> list:

        list_result = []

        if bool_order_result_desc:

            str_text = (f'SELECT {str_column_name}, COUNT(*) AS anzahl FROM '
                        f'{self._str_sql_schema}.{self._str_table_name} GROUP BY '
                        f'{str_column_name} HAVING COUNT(*) > 1 ORDER BY anzahl DESC')


        else:

            str_text = (f'SELECT {str_column_name}, COUNT(*) AS anzahl FROM '
                        f'{self._str_sql_schema}.{self._str_table_name} GROUP BY '
                        f'{str_column_name} HAVING COUNT(*) > 1')

        if self._my_sql_connection and self._my_sql_cursor:

            try:

                self._my_sql_cursor.execute(str_text)

                list_result = self._my_sql_cursor.fetchall()

                self._my_sql_connection.commit()

            except sqlite3.OperationalError as err:

                print(
                    f'---- Operational Error in {__title__}, {self.group_table_column_as_histogram.__name__} ----, \n'
                    f'---- the Text {str_text} has caused an Error {err} ! ----')

                exit(1)

            if list_result.__len__() > 0:

                return list_result

            else:

                return []

        else:

            return []

    def sort_desc_table_acc_column(self, str_column_name: str) -> None:

        str_text = f'SELECT * FROM {self._str_table_name} ORDER BY {str_column_name} DESC'

        if self._get_sql_alive:

            try:

                self._my_sql_cursor.execute(str_text)

                self._my_sql_connection.commit()

            except sqlite3.OperationalError as err:

                print(f'---- Operational Error in {__title__}, {self.sort_desc_table_acc_column.__name__} ----, \n'
                      f'---- the Text {str_text} has caused an Error {err} ! ----')

                exit(1)
