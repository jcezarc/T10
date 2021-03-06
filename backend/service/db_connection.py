import os
from util.db.sql_table import SqlTable
# from util.db.mongo_table import MongoTable


# ----------------------------------------------
T10_USER = os.environ.get(
    'T10_USER',
    ''
)
T10_PASSWORD = os.environ.get(
    'T10_PASSWORD',
    ''
)
T10_HOST = os.environ.get(
    'T10_HOST',
    'localhost'
)
T10_DATA_BASE = os.environ.get(
    'T10_DATA_BASE',
    'T10_JulioCascalles'
)
# ----------------------------------------------


def get_table(schema):
    return SqlTable(schema, {
                "dialect": "postgresql",
                "driver": "psycopg2",
                "username": T10_USER,
                "password": T10_PASSWORD,
                "host": T10_HOST,
                "port": 5432,
                "database": T10_DATA_BASE
            })