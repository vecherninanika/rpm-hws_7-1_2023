"""File with database managing tools."""

import psycopg2
from dotenv import load_dotenv
from os import getenv
from config import *
from views import list_to_view

load_dotenv()
PG_DBNAME = getenv('PG_DBNAME')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')
PG_HOST = getenv('PG_HOST')


def is_num(value: any) -> bool:
    return isinstance(value, (int, float))


class InvalidQuery(Exception):
    """Error class for server."""

    def __init__(self, msg: str) -> None:
        self.msg = msg

    def __str__(self) -> str:
        classname = self.__class__.__name__
        return f'\n {classname} Error: {self.msg}\n'


class DbHandler:
    """Class which sends queries to database."""

    db_connection = psycopg2.connect(
    dbname=PG_DBNAME,
    host=PG_HOST,
    port=PG_PORT,
    user=PG_USER,
    password=PG_PASSWORD
    )
    db_cursor = db_connection.cursor()

    @classmethod
    def get_data(cls, req_conds: dict = None) -> dict:
        cls.db_cursor.execute(DbHandler.query_request(SELECTOR, req_conds) if req_conds else SELECTOR)
        examples = cls.db_cursor.fetchall()
        examples = [example[1:] for example in examples]  # чтобы на сайт не выводит id
        return {
            'names': list_to_view(examples),
            'count': len(examples)
        }

    @classmethod
    def is_valid_token(cls, username: str, req_token: str) -> bool:

        cls.db_cursor.execute(GET_TOKEN.format(username=username))
        db_token = cls.db_cursor.fetchone()
        if db_token:
            return db_token[0] == req_token
        return False

    @staticmethod
    def compose_insert(insert_data: dict) -> str:
        keys = tuple(insert_data.keys())
        for key in keys:
            if key == 'name' and str(insert_data[key]).isdigit():
                raise InvalidQuery('Name should not be a number!')
            if key == 'age' and not str(insert_data[key]).isdigit():
                raise InvalidQuery('Age should be a number!')
            if key == 'age' and insert_data[key] < 0:
                raise InvalidQuery('Age should be more than zero!')
        values = [insert_data[val_key] for val_key in keys]
        attrs = ', '.join(keys)
        values = ', '.join([str(val) if is_num(val) else f"'{val}'" for val in values])
        return INSERT.format(keys=attrs, values=values)

    @classmethod
    def update(cls, data: dict, where: dict) -> bool:
        to_join = []
        for data_key in data.keys():
            if data_key == 'name' and str(data[data_key]).isdigit():
                raise InvalidQuery('Name should not be a number')
            if data_key == 'age' and not str(data[data_key]).isdigit():
                raise InvalidQuery('Age should be a number!')
            if is_num(data[data_key]):
                to_join.append(f"{data_key}={data_key}")
            else:
                to_join.append(f"{data_key}='{data[data_key]}'")
        req = ', '.join(to_join)
        try:
            cls.db_cursor.execute(cls.query_request(UPDATE.format(request=req), where))
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @classmethod
    def insert(cls, examples_data: dict) -> bool:
        try:
            cls.db_cursor.execute(cls.compose_insert(examples_data))
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @classmethod
    def delete(cls, req_conds: dict) -> bool:
        try:
            cls.db_cursor.execute(cls.query_request(DELETE, req_conds))
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @staticmethod
    def query_request(request: str, req_conds: dict) -> str:
        conditions = []
        for attr, value in req_conds.items():
            to_add = f'{attr}={value}' if isinstance(value, (int, float)) else f"{attr}='{value}'"
            conditions.append(to_add)
        return '{0} WHERE {1}'.format(request, ' AND '.join(conditions))
