"""mySQLDataBaseDefinitions.py."""

__title__: str = "mySQLDataBaseDefinitions"
__version__: str = "0.1.0"
__author__: str = "Oliver Rudow"
__copyright__: str = "Copyright 2024, Brain Center Höfen"


LIST_DATA_CONTAINER_SECTIONS: list[str] = ['DATA_CONTAINER.SQL_FLAGS',
                                           'DATA_CONTAINER.SQL_DATA_BASE',
                                           'DATA_CONTAINER.SQL_CONNECTION',
                                           'DATA_CONTAINER.SQL_TABLE_PROPERTIES',
                                           'DATA_CONTAINER.FILE_MANAGEMENT']

TUPLE_DATA_CONTAINER_SQL_FLAG_DATA_BASE = ('DATA_CONTAINER.SQL_FLAGS',
                                           'flag_sql_data_base',
                                           True,
                                           bool)

TUPLE_DATA_CONTAINER_SQL_FLAG_ADD_DATE_2_TABLE = ('DATA_CONTAINER.SQL_FLAGS',
                                                  'flag_sql_add_date_2_table',
                                                   True,
                                                   bool)

TUPLE_DATA_CONTAINER_SQL_DATA_BASE_NAME = ('DATA_CONTAINER.SQL_DATA_BASE',
                                           'sql_data_base_filename',
                                           'default.db',
                                           str)

TUPLE_DATA_CONTAINER_SQL_DATA_BASE_SCHEMA = ('DATA_CONTAINER.SQL_DATA_BASE',
                                             'sql_data_base_schema',
                                             'main',
                                             str)

TUPLE_DATA_CONTAINER_SQL_CONNECTION_TIMEOUT = ('DATA_CONTAINER.SQL_CONNECTION',
                                               'timeout',
                                               5.0,
                                               float)

TUPLE_DATA_CONTAINER_SQL_CONNECTION_URI = ('DATA_CONTAINER.SQL_CONNECTION',
                                           'uri',
                                           True,
                                           bool)


TUPLE_DATA_CONTAINER_SQL_TABLE_NUM_ALLOWED_MINUS_ONE = ('DATA_CONTAINER.SQL_TABLE_PROPERTIES',
                                                        'sql_table_num_allowed_minus_one',
                                                        3,
                                                        int)


TUPLE_DATA_CONTAINER_FILE_MANAGEMENT_NUMBER_PRECEDED_DATA = ('DATA_CONTAINER.FILE_MANAGEMENT',
                                                             'number_preceded_data',
                                                             3,
                                                             int)


LIST_DATA_CONTAINER_OPTIONS: list[tuple] = [TUPLE_DATA_CONTAINER_SQL_FLAG_DATA_BASE,
                                            TUPLE_DATA_CONTAINER_SQL_FLAG_ADD_DATE_2_TABLE,
                                            TUPLE_DATA_CONTAINER_SQL_DATA_BASE_NAME,
                                            TUPLE_DATA_CONTAINER_SQL_DATA_BASE_SCHEMA,
                                            TUPLE_DATA_CONTAINER_SQL_CONNECTION_TIMEOUT,
                                            TUPLE_DATA_CONTAINER_SQL_CONNECTION_URI,
                                            TUPLE_DATA_CONTAINER_SQL_TABLE_NUM_ALLOWED_MINUS_ONE,
                                            TUPLE_DATA_CONTAINER_FILE_MANAGEMENT_NUMBER_PRECEDED_DATA]