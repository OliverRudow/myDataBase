"""myTableBase.py."""

__title__: str = "myTableBase"
__version__: str = "0.3.0"
__author__: str = "Oliver Rudow"
__email__: str = "oliver.rudow@googlemail.com"
__copyright__: str = "Copyright 2024, Brain Center Höfen"

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import dataclasses
from enum import Enum
from myauxiliary import myAuxiliary
from mytuple import myTuple

COLUMN_NAME = 0


@dataclasses.dataclass(init=False)
class MyTableBase:
    """
        Class for providing basic variables and methods.

        _indexTuple is an Enum defining the configuration of the tuple elements as defined in myTuple

        _strTableName is either a filename or a SQL database table name

        _dictTableSettings store a tuple that provides information of the column name and SQL database related info.
        The length of the tuple is at least 1

        _dictTableColumns store the column names of the table, the dict is needed to get access to the column names.
        The dict is derived from the _dictTableSettings

        _listTableColumnKeys provide the dict-keys of the above dicts, the list is needed to get access to the column
        index, the list is derived from _dictTableColumns

        _intNumberTableColumns provides the number of columns stored within the table

    """
    _index_tuple: myTuple.MyTuple = dataclasses.field(repr=False)

    _int_number_tuple_elements: int = dataclasses.field(repr=False, default=0)

    _str_table_name: str = dataclasses.field(repr=True, default='')

    _dict_table_settings: dict[str, tuple] = dataclasses.field(repr=False, default=dict[str, tuple])

    _dict_table_columns: dict[str, str] = dataclasses.field(repr=False, default=dict[str, str])

    _enum_table_columns_index: Enum = dataclasses.field(repr=False, default_factory=type(Enum))

    _list_table_column_keys: list[str] = dataclasses.field(repr=False, default=list[str])

    _int_table_columns_number: int = dataclasses.field(repr=False, default=0)

    # add date to table name
    _flag_add_date_2_file_name: bool = dataclasses.field(repr=False, default=False)

    # handling of preceded tables
    _flag_clean_preceded_tables: bool = dataclasses.field(repr=False, default=True)

    _int_number_preceded_tables: int = dataclasses.field(repr=False, default=0)

    def __init__(self):

        self._index_tuple = myTuple.MyTuple

        self._int_number_tuple_elements = len(myTuple.MyTuple)

        self._str_table_name = 'default'

    def set_table_name(self, str_table_name) -> None:
        try:

            if str_table_name == '':

                raise ValueError

            self. _str_table_name = str_table_name

        except ValueError:

            print(f'---- ValueError in {__title__}, {self.set_table_name.__name__}: '
                  f'init of table failed, table name is a empty string -----')

            exit(1)

    def set_flag_add_date_2_table_name(self, bool_add_date: bool) -> None:

        self._flag_add_date_2_file_name = bool_add_date

    def set_flag_clean_preceded_tables(self, bool_clean_tables: bool) -> None:

        self._flag_clean_preceded_tables = bool_clean_tables

    def set_number_preceded_tables(self, int_number_preceded_tables: int) -> None:

        self._int_number_preceded_tables = int_number_preceded_tables

    def set_dict_table_settings(self, dict_table_settings: dict[str, tuple]) -> None:
        try:

            if dict_table_settings.__len__() == 0:

                raise ValueError

            self._dict_table_settings = dict_table_settings

            self._derive_dict_table_columns()

            self._derive_dict_table_column_keys()

            self._derive_dict_table_columns_number()

            # generate enum for getting column index
            self._enum_table_columns_index = Enum('_enum_table_columns_index', self._list_table_column_keys, start=0)

        except ValueError:

            print(f'---- ValueError in {__title__}, {self.set_dict_table_settings.__name__}: '
                  f'init of table {self._str_table_name} failed, dictTableSettings is empty -----')

            exit(1)

    def _derive_dict_table_columns(self) -> None:
        self._dict_table_columns = {}

        for elem in self._dict_table_settings.keys():
            # get tuple
            the_tuple = self._dict_table_settings[elem]
            # the column name is almost the first element
            self._dict_table_columns[elem] = the_tuple[COLUMN_NAME]

    def _derive_dict_table_column_keys(self) -> None:

        self._list_table_column_keys = list(self._dict_table_settings.keys())

    def _derive_dict_table_columns_number(self) -> None:

        self._int_table_columns_number = self._list_table_column_keys.__len__()

    @property
    def get_table_name(self) -> str:

        return self._str_table_name

    @property
    def get_table_number_columns(self) -> int:

        return self._int_table_columns_number

    def get_column_name_from_dict(self, tuple_column_setting: tuple) -> str:
        try:

            if tuple_column_setting.__len__() != self._int_number_tuple_elements:

                raise ValueError(f'---- ValueError in {__title__}, {self.get_column_name_from_dict.__name__}:'
                                 f' the input tuple {tuple_column_setting} is corrupt!-----')

            if self._dict_table_columns.__len__() == 0:

                raise ValueError(f'---- ValueError in {__title__}, {self.get_column_name_from_dict.__name__}: '
                                 f'the dictTableColumns is empty, '
                                 f'can not apply tuple {tuple_column_setting}! ----')

            return self._dict_table_columns[tuple_column_setting[self._index_tuple.OPTION_NAME]]

        except ValueError as e:

            print(e)

            exit(1)

    def get_column_index_from_list(self, tuple_column_setting: tuple) -> int:
        try:

            if tuple_column_setting.__len__() != self._int_number_tuple_elements:

                raise ValueError

            return self._list_table_column_keys.index(tuple_column_setting[self._index_tuple.OPTION_NAME])

        except ValueError:

            print(f'---- ValueError in {__title__}, {self.get_column_index_from_list.__name__}: '
                  f'the input tuple {tuple_column_setting} is corrupt!-----')

            exit(1)


if __name__ == "__main__":
    myTable = MyTableBase()
    myTable.set_table_name('../System/Oliver.ini')
    myTable.set_dict_table_settings({'firstColumn': ('Weight', 'INTEGER', 'PRIMARY_KEY')})
    myTable.set_table_name(myAuxiliary.add_date_2_object_name(myTable.get_table_name, 'leading'))
    print(myTable)
    print(f' Number of Columns: {myTable.get_table_number_columns}')
    print(f' Table Name: {myTable.get_table_name}')
    print(f' Index of Column: {myTable.get_column_index_from_list(('', 'firstColumn', '', str))}')

