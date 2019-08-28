import os
import re

import typing

# ensure having set env vars
import setup  # noqa

import psycopg2


def with_connection(func):
    def wrapper(*args):
        return func(*args)
    return wrapper


class DB:
    connection = None
    cursor = None
    headers = {}

    def __init__(self, host_name: str = None, db_name: str = None, user_name: str = None, password: str = None):
        self.__host_name = host_name or os.environ.get('DB_HOST')
        self.__db_name = db_name or os.environ.get('DB_NAME')
        self.__username = user_name or os.environ.get('DB_USER')
        self.__password = password or os.environ.get('DB_PW')

    def __connect(self) -> bool:
        self.connection = psycopg2.connect(
            f'host={self.__host_name} dbname={self.__db_name} user={self.__username} password={self.__password}')
        assert isinstance(self.connection, psycopg2.extensions.connection), 'DB not connected'
        return True

    def __disconnect(self):
        self.connection.close()
        assert self.connection.closed, 'DB still connected!'

    def has_headers(self):
        return len(self.headers) > 0

    def __gen_cursor(self):
        self.cursor = self.connection.cursor()

    @staticmethod
    def __escape(query: str) -> str:
        return re.escape(query).replace('\\', '')

    def open_connection(self):
        self.__connect()
        self.__gen_cursor()

    def close_connection(self):
        self.connection.commit()
        self.__disconnect()

    @with_connection
    def __parse_output(self, output: str, table_name: str) -> str:
        if self.has_headers():
            return output
        self.open_connection()
        self.cursor.execute(f'SELECT * FROM information_schema.columns WHERE table_name=\'{table_name}\';')
        try:
            output = self.cursor.fetchall()
        except psycopg2.ProgrammingError:
            output = None
        self.close_connection()
        return output

    def select(self, table_name: str, columns: typing.List, where: typing.List):
        where_cond = ''
        if where:
            where_cond = f'WHERE {" ".join(where)}'
        query = f'SELECT {", ".join(columns)} FROM {table_name} {where_cond}'
        return self.__parse_output(self.execute(query), table_name)

    @with_connection
    def execute(self, query: str):
        self.open_connection()

        self.cursor.execute(self.__escape(query))
        try:
            output = self.cursor.fetchall()
        except psycopg2.ProgrammingError:
            output = None

        self.close_connection()
        return output
