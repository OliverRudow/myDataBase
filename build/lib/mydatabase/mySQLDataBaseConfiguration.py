"""mySQLDataBaseConfiguration.py."""

__title__: str = "mySQLDataBaseConfiguration"
__version__: str = "0.1.0"
__author__: str = "Oliver Rudow"
__email__: str = "oliver.rudow@googlemail.com"
__copyright__: str = "Copyright 2025, Brain Center Höfen"

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import dataclasses
import configparser
from typing import Optional
from myconfig import myConfigBase
from mydatabase import mySQLDataBaseDefinitions

CONFIG_FILENAME: str = '../System/Init/config.ini'
REFERENCE_CONFIG_FILENAME: str = '../System/reference-config.ini'


@dataclasses.dataclass()
class MyConfigError(Exception):
    """Base class for other exceptions"""
    pass


@dataclasses.dataclass(init=False)
class MyConfigUrlValidationError(MyConfigError):
    """Raised when Url validation is False"""
    pass


@dataclasses.dataclass(init=False)
class MySQLDataBaseConfiguration(myConfigBase.MyConfigBase):
    """
        Class for reading the Scrapper Config.ini.
    """
    # flags
    def __init__(self, cfg_configuration: Optional[configparser.ConfigParser] = None,
                 cfg_reference: Optional[configparser.ConfigParser] = None):

        super().__init__(None)

        if cfg_reference is None:

            self.read_reference_config_file(REFERENCE_CONFIG_FILENAME)

        else:

            self._cfg_reference = cfg_reference

        if cfg_configuration is None:

            self._str_config_file_name = CONFIG_FILENAME

            self.load_config()

        else:

            self._cfg_configuration = cfg_configuration

        self._list_required_sections = self._cfg_reference.sections()

    def __repr__(self) -> str | None:

        if self._cfg_configuration:

            return self.get_config_as_json

        else:

            return None

    """
        Functions related to SQL Data Container
    """

    @property
    def get_int_data_container_clean_number_preceded_data(self) -> int:

        try:

            self._get_tuple(mySQLDataBaseDefinitions.TUPLE_DATA_CONTAINER_FILE_MANAGEMENT_NUMBER_PRECEDED_DATA)

            if self._cfg_configuration.get(self._str_section_name, self._str_option_name):

                return self._cfg_configuration.getint(self._str_section_name, self._str_option_name)

            else:

                raise ValueError

        except configparser.NoSectionError:

            print(f'----- NoSectionError in {__title__}, '
                  f'{self.get_int_data_container_clean_number_preceded_data.__name__}:'
                  f' Section {self._str_section_name} is not in Config-File')

            return bool(self._any_option_content)

        except configparser.NoOptionError:

            print(f'----- NoOptionError in {__title__}, '
                  f'{self.get_int_data_container_clean_number_preceded_data.__name__}:'
                  f' Option {self._str_option_name} is not in Config-File')

            return bool(self._any_option_content)

        except ValueError:

            print(f'----- ValueError in {__title__}, '
                  f'{self.get_int_data_container_clean_number_preceded_data.__name__}:'
                  f' Section {self._str_section_name} is corrupt, bool required')

            return bool(self._any_option_content)

    @property
    def get_flag_data_container_sql_data_base(self) -> bool:

        try:

            self._get_tuple(mySQLDataBaseDefinitions.TUPLE_DATA_CONTAINER_SQL_FLAG_DATA_BASE)

            if myConfigBase.is_bool(self._cfg_configuration.getboolean(self._str_section_name, self._str_option_name)):

                return bool(self._cfg_configuration.getboolean(self._str_section_name, self._str_option_name))

            else:

                raise ValueError

        except configparser.NoSectionError:

            print(f'----- NoSectionError in {__title__}, '
                  f'{self.get_flag_data_container_sql_data_base.__name__}:'
                  f' Section {self._str_section_name} is not in Config-File')

            return bool(self._any_option_content)

        except configparser.NoOptionError:

            print(f'----- NoOptionError in {__title__}, '
                  f'{self.get_flag_data_container_sql_data_base.__name__}:'
                  f' Option {self._str_option_name} is not in Config-File')

            return bool(self._any_option_content)

        except ValueError:

            print(f'----- ValueError in {__title__}, '
                  f'{self.get_flag_data_container_sql_data_base.__name__}:'
                  f' Section {self._str_section_name} is corrupt, bool required')

            return bool(self._any_option_content)

    def set_flag_data_container_sql_data_base(self, str_flag: str) -> None:

        try:

            self._get_tuple(mySQLDataBaseDefinitions.TUPLE_DATA_CONTAINER_SQL_FLAG_DATA_BASE)

            if str_flag not in list(myConfigBase.BOOLEAN_STATES.keys()):

                raise ValueError

            self._cfg_configuration.set(self._str_section_name, self._str_option_name, str_flag)

        except ValueError:

            print(f'----- ValueError in {__title__}, '
                  f'{self.set_flag_data_container_sql_data_base.__name__}:'
                  f' the boolean state {str_flag} is not defined')

        except configparser.NoSectionError:

            print(f'----- NoSectionError in {__title__}, '
                  f'{self.set_flag_data_container_sql_data_base.__name__}:'
                  f' Section {self._str_section_name} is not in Config-File')

        except configparser.NoOptionError:

            print(f'----- NoOptionError in {__title__}, '
                  f'{self.set_flag_data_container_sql_data_base.__name__}:'
                  f' Option {self._str_option_name} is not in Config-File')

    @property
    def get_data_container_sql_data_base_file_name(self) -> str:

        try:

            self._get_tuple(mySQLDataBaseDefinitions.TUPLE_DATA_CONTAINER_SQL_DATA_BASE_NAME)

            if self._cfg_configuration.get(self._str_section_name, self._str_option_name):

                return self._cfg_configuration.get(self._str_section_name, self._str_option_name)

            else:

                raise ValueError

        except configparser.NoSectionError:

            print(f'----- NoSectionError in {__title__}, '
                  f'{self.get_data_container_sql_data_base_file_name.__name__}:'
                  f' Section {self._str_section_name} is not in Config-File')

            return self._any_option_content

        except configparser.NoOptionError:

            print(f'----- NoOptionError in {__title__}, '
                  f'{self.get_data_container_sql_data_base_file_name.__name__}:'
                  f' Option {self._str_option_name} is not in Config-File')

            return self._any_option_content

        except ValueError:

            print(f'----- ValueError in {__title__}, '
                  f'{self.get_data_container_sql_data_base_file_name.__name__}:'
                  f' Section {self._str_section_name} is corrupt, str required')

            return self._any_option_content

    @property
    def get_data_container_sql_data_base_schema(self) -> str:

        try:

            self._get_tuple(mySQLDataBaseDefinitions.TUPLE_DATA_CONTAINER_SQL_DATA_BASE_SCHEMA)

            if self._cfg_configuration.get(self._str_section_name, self._str_option_name):

                return self._cfg_configuration.get(self._str_section_name, self._str_option_name)

            else:

                raise ValueError

        except configparser.NoSectionError:

            print(f'----- NoSectionError in {__title__}, '
                  f'{self.get_data_container_sql_data_base_schema.__name__}:'
                  f' Section {self._str_section_name} is not in Config-File')

            return self._any_option_content

        except configparser.NoOptionError:

            print(f'----- NoOptionError in {__title__}, '
                  f'{self.get_data_container_sql_data_base_schema.__name__}:'
                  f' Option {self._str_option_name} is not in Config-File')

            return self._any_option_content

        except ValueError:

            print(f'----- ValueError in {__title__}, '
                  f'{self.get_data_container_sql_data_base_schema.__name__}:'
                  f' Section {self._str_section_name} is corrupt, str required')

            return self._any_option_content

    @property
    def get_data_container_sql_data_base_connection_timeout(self) -> float:

        try:

            self._get_tuple(mySQLDataBaseDefinitions.TUPLE_DATA_CONTAINER_SQL_CONNECTION_TIMEOUT)

            if float(self._cfg_configuration.getfloat(self._str_section_name, self._str_option_name)):

                return float(self._cfg_configuration.getfloat(self._str_section_name, self._str_option_name))

            else:

                raise ValueError

        except configparser.NoSectionError:

            print(f'----- NoSectionError in {__title__}, '
                  f'{self.get_data_container_sql_data_base_connection_timeout.__name__}:'
                  f' Section {self._str_section_name} is not in Config-File')

            return float(self._any_option_content)

        except configparser.NoOptionError:

            print(f'----- NoOptionError in {__title__}, '
                  f'{self.get_data_container_sql_data_base_connection_timeout.__name__}:'
                  f' Option {self._str_option_name} is not in Config-File')

            return float(self._any_option_content)

        except ValueError:

            print(f'----- ValueError in {__title__}, '
                  f'{self.get_data_container_sql_data_base_connection_timeout.__name__}:'
                  f' Section {self._str_section_name} is corrupt, float required')

            return float(self._any_option_content)

    @property
    def get_data_container_sql_data_base_connection_uri(self) -> bool:

        try:

            self._get_tuple(mySQLDataBaseDefinitions.TUPLE_DATA_CONTAINER_SQL_CONNECTION_URI)

            if myConfigBase.is_bool(self._cfg_configuration.getboolean(self._str_section_name, self._str_option_name)):

                return bool(self._cfg_configuration.getboolean(self._str_section_name, self._str_option_name))

            else:

                raise ValueError

        except configparser.NoSectionError:

            print(f'----- NoSectionError in {__title__}, '
                  f'{self.get_data_container_sql_data_base_connection_uri.__name__}:'
                  f' Section {self._str_section_name} is not in Config-File')

            return bool(self._any_option_content)

        except configparser.NoOptionError:

            print(f'----- NoOptionError in {__title__}, '
                  f'{self.get_data_container_sql_data_base_connection_uri.__name__}:'
                  f' Option {self._str_option_name} is not in Config-File')

            return bool(self._any_option_content)

        except ValueError:

            print(f'----- ValueError in {__title__}, '
                  f'{self.get_data_container_sql_data_base_connection_uri.__name__}:'
                  f' Section {self._str_section_name} is corrupt, bool required')

            return bool(self._any_option_content)

    @property
    def get_data_container_sql_properties_num_allowed_minus_one(self) -> int:

        try:

            self._get_tuple(mySQLDataBaseDefinitions.TUPLE_DATA_CONTAINER_SQL_TABLE_NUM_ALLOWED_MINUS_ONE)

            if self._cfg_configuration.get(self._str_section_name, self._str_option_name):

                return self._cfg_configuration.getint(self._str_section_name, self._str_option_name)

            else:

                raise ValueError

        except configparser.NoSectionError:

            print(f'----- NoSectionError in {__title__}, '
                  f'{self.get_data_container_sql_properties_num_allowed_minus_one.__name__}:'
                  f' Section {self._str_section_name} is not in Config-File')

            return int(self._any_option_content)

        except configparser.NoOptionError:

            print(f'----- NoOptionError in {__title__}, '
                  f'{self.get_data_container_sql_properties_num_allowed_minus_one.__name__}:'
                  f' Option {self._str_option_name} is not in Config-File')

            return int(self._any_option_content)

        except ValueError:

            print(f'----- ValueError in {__title__}, '
                  f'{self.get_data_container_sql_properties_num_allowed_minus_one.__name__}:'
                  f' Section {self._str_section_name} is corrupt, float required')

            return int(self._any_option_content)

    @property
    def get_data_container_number_preceded_data(self) -> int:

        try:

            self._get_tuple(mySQLDataBaseDefinitions.TUPLE_DATA_CONTAINER_FILE_MANAGEMENT_NUMBER_PRECEDED_DATA)

            if self._cfg_configuration.get(self._str_section_name, self._str_option_name):

                return int(self._cfg_configuration.getint(self._str_section_name, self._str_option_name))

            else:

                raise ValueError

        except configparser.NoSectionError:

            print(f'----- NoSectionError in {__title__}, '
                  f'{self.get_data_container_number_preceded_data.__name__}:'
                  f' Section {self._str_section_name} is not in Config-File')

            return int(self._any_option_content)

        except configparser.NoOptionError:

            print(f'----- NoOptionError in {__title__}, '
                  f'{self.get_data_container_number_preceded_data.__name__}:'
                  f' Option {self._str_option_name} is not in Config-File')

            return int(self._any_option_content)

        except ValueError:

            print(f'----- ValueError in {__title__}, '
                  f'{self.get_data_container_number_preceded_data.__name__}:'
                  f' Section {self._str_section_name} is corrupt, int required')

            return int(self._any_option_content)


if __name__ == "__main__":
    my_sql_data_base_config = MySQLDataBaseConfiguration()
    print(my_sql_data_base_config)


