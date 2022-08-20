import pandas as pd
import ast
from pprint import pprint

import psycopg2

CONST_PANDAS_DTYPES = {
    "object": "string",
    "int64": "integer",
    "float64": "float",
    "bool": "bool",
    "datetime": "datetime",
    "category": "list",
}


class DbParser:
    columns: dict = {}

    def __init__(self, name: str) -> None:
        self.name = name
        self.columns = {}

    def __cache_db(self):
        # save dataframe as aroow for faster io
        self.__dataframe.to_feather("./data/dataframe.feather")

    def __parse_columns(self):
        # parse column names and thier datatype
        __columns_dict = self.__dataframe.dtypes.apply(lambda x: x.name).to_dict()

        for key in __columns_dict.keys():
            column_name = key
            column_type = __columns_dict[column_name]

            converted_col_type = CONST_PANDAS_DTYPES.get(column_type, "other")

            self.columns.update({column_name: converted_col_type})

    def postgresql(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        db_name: str,
        table_name: str,
    ):
        try:
            conn = psycopg2.connect(
                dbname=db_name, host=host, port=port, user=username, password=password
            )

        except Exception as e:
            print(e)
            return e

        self.__dataframe = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        self.__cache_db()
        self.__parse_columns()


    def csv(self, url: str):
        self.__dataframe = pd.read_csv(url)
        self.__cache_db()
        self.__parse_columns()

    def feather(self, url: str):
        self.__dataframe = pd.read_feather(url)
        self.__cache_db()
        self.__parse_columns()


if __name__ == "__main__":
    parser = DbParser("sample_data")
