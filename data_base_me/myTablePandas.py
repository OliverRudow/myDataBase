"""myTablePandas.py."""

__title__: str = "myTablePandas"
__version__: str = "1.0"
__author__: str = "Oliver Rudow"
__copyright__: str = "Copyright 2024, Brain Center Höfen"

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import dataclasses
import pandas as pd
from sys import getsizeof
from typing import Optional, Any
from data_base_me import myTableBase
from file_base_me import myFileBase


@dataclasses.dataclass(init=False)
class MyTablePandas(myTableBase.MyTableBase):
    """
        Class for providing variables and methods for an application utilizing Pandas DataFrame.
        The class is considered to be file-based.

    """
    # pandas data frame
    _pd_table_data_frame: pd.DataFrame = dataclasses.field(repr=False, default_factory=type(pd.DataFrame))

    # data frame row index for getting and putting a line
    _int_table_put_row_index: int = dataclasses.field(repr=False, default=0)
    _int_table_get_row_index: int = dataclasses.field(repr=False, default=0)

    # column selection for writing and reading pandas dataframes to file or from file
    _list_table_columns_storage: list[str] = dataclasses.field(repr=False, default=list[str])
    _list_table_columns_read: list[str] = dataclasses.field(repr=False, default=list[str])

    # File Base
    _file_base: myFileBase.MyFileBase = dataclasses.field(repr=False, default=type(myFileBase.MyFileBase))

    def __init__(self):
        super().__init__()

        self._file_base = myFileBase.MyFileBase()

    def set_list_table_columns_storage(self, list_table_columns_storage: list[str]) -> None:
        self._list_table_columns_storage = list_table_columns_storage

    def set_list_table_columns_read(self, list_table_columns_read: list[str]) -> None:
        self._list_table_columns_read = list_table_columns_read

    def reset_table_pandas(self) -> None:
        self._pd_table_data_frame = pd.DataFrame([], columns=list(self._dict_table_columns.values()))

    def write_table_pandas(self) -> None:
        try:

            self._file_base.set_file_name(self._str_table_name, False)

            my_csv_data_file = self._file_base.get_entire_file_name

            with open(my_csv_data_file, 'w'):

                self._pd_table_data_frame.to_csv(my_csv_data_file,
                                                 columns=self._list_table_columns_storage,
                                                 index=True,
                                                 header=True)

        except FileNotFoundError:

            print(f'----- Error: Write Data to CSV File, File {self._str_table_name} not found -----')

    def read_table_pandas(self, str_file_name: Optional[str] = None) -> None:
        try:

            if str_file_name is not None:

                self._file_base.set_file_name(str_file_name, False)

            else:

                self._file_base.set_file_name(self._str_table_name, False)

            my_input_csv_data_file = self._file_base.get_entire_file_name_as_path_obj

            if not my_input_csv_data_file.is_file():

                raise FileNotFoundError

            # check suffix
            if not my_input_csv_data_file.suffix == '.csv':

                raise Exception(f'----- Suffix {my_input_csv_data_file.suffix} incorrect ------')

            # read data
            self._pd_table_data_frame = pd.read_csv(str(my_input_csv_data_file))

        except FileNotFoundError:

            print(f'----- FileNotFoundError: File {self._str_table_name} does not exist -----')
            exit(1)

        except pd.errors.EmptyDataError:

            print(f'----- File empty error: File {self._str_table_name} has no content -----')
            exit(1)

        except pd.errors.ParserError:

            print(f'----- Parse error: File {self._str_table_name} failed -----')
            exit(1)

        except Exception as error:

            print(error)
            exit(1)

    def update_table_put_row_index(self) -> None:
        self._int_table_put_row_index = self._pd_table_data_frame.__len__()

    @property
    def get_size_table_data_frame(self) -> int:
        return getsizeof(self._pd_table_data_frame)

    @property
    def get_table_put_row_index(self) -> int:
        return self._int_table_put_row_index

    @property
    def get_table_get_row_index(self) -> int:
        return self._int_table_get_row_index

    def set_sable_individual_value_row_index_column_index(self,
                                                          int_row_index: int,
                                                          int_column_index: int,
                                                          all_value: Any) -> None:
        try:

            if int_row_index > self._int_table_put_row_index:
                raise ValueError(f'---- ValueError: set Value in Pandas data Frame failed, RoW Index {int_row_index} out'
                                 f'of Range! ----')

            if int_column_index >= self._int_table_columns_number:
                raise ValueError(f'---- ValueError: set Value in Pandas data Frame failed, RoW Index {int_column_index} '
                                 f'out of Range! ----')

            self._pd_table_data_frame.iat[int_row_index, int_column_index] = all_value

        except ValueError as e:
            print(e)
            exit(1)

    def get_table_individual_value_row_index_column_index(self, int_row_index: int, int_column_index: int) -> Any:
        try:
            if int_row_index > self._int_table_put_row_index:
                raise ValueError(f'---- ValueError: set Value in Pandas data Frame failed, RoW Index {int_row_index} out'
                                 f'of Range! ----')

            if int_column_index >= self._int_table_columns_number:
                raise ValueError(f'---- ValueError: set Value in Pandas data Frame failed, RoW Index {int_column_index} '
                                 f'out of Range! ----')

            return self._pd_table_data_frame.iat[int_row_index, int_column_index]

        except ValueError as e:
            print(e)
            exit(1)

    def get_table_single_column_from_data_frame(self, list_column_name: list[str]) -> list[Any]:
        try:
            if list_column_name.__len__() != 1:
                raise ValueError(f'---- ValueError: getting a column from  Pandas data Frame failed, List Column'
                                 f'Names {list_column_name} exceeds dimension 1! ---- ')

            if list_column_name[0] not in self._list_table_columns_read:
                raise pd.errors.InvalidColumnName(f'----PandasColumnError: {list_column_name} is not a '
                                                  f'DataFrame Column -----!')

            return list(self._pd_table_data_frame[list_column_name[0]])

        except pd.errors.InvalidColumnName as e:
            print(e)
            exit(1)

    def set_table_entire_row(self, list_entire_row: list[Any]) -> None:
        try:

            if list_entire_row.__len__() == 0:

                raise ValueError(f'----- Value Error in Data Base URL-Filer: Input Line {list_entire_row} to '
                                 f'Data Output is empty -----')

            if list_entire_row.__len__() != self._int_table_columns_number:

                raise ValueError(f'----- Value Error in Data Base URL-Filer: Input Line {list_entire_row} '
                                 f'to Data Output is Corrupt -----')

            self.update_table_put_row_index()

            # insert result in pandas table
            self._pd_table_data_frame.loc[self._int_table_put_row_index] = list_entire_row

        except ValueError as e:
            print(e)
            exit(1)

    def get_table_as_dict(self) -> list:

        return self._pd_table_data_frame.to_dict('records')


if __name__ == "__main__":
    myTable = MyTablePandas()
    myTable.set_table_name('Oliver')
    myTable.set_dict_table_settings({'firstColumn': ('Weight', 'INTEGER', 'PRIMARY_KEY')})
    print(myTable)
    print(f' Number of Columns: {myTable.get_table_number_columns}')
    print(f' Table Name: {myTable.get_table_name}')
    print(f' Index of Column: {myTable.get_column_index_from_list(('', 'firstColumn', '', str))}')

