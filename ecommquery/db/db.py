from peewee import *
import sqlite3
import os
from pathlib import Path

db_proxy = Proxy()

class Db(Model):
    class Meta:
        database = db_proxy

    # def __init__(self, conn):
    #     self._conn = conn

    @staticmethod
    def _load_schema(conn):
        # Get the directory where this file is located
        dbpack_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(dbpack_dir, 'schema.sql')
        with open(schema_path, 'r') as schema_file:
            schema_sql = schema_file.read()

        try:
            conn.executescript(schema_sql)
            conn.commit()
        except sqlite3.Error as e:
            error_message = f"SQL error in '{schema_path}': \n{type(e).__name__}: {str(e)}"
            raise Exception(error_message) from e

    @classmethod
    def open(cls, db_path: str = 'data/db/ecommquery.db', recreate: bool = False):
        """
        Open/create database using schema.sql file
        """

        # Check if database exists
        db_exists = Path(db_path).exists()
        # If recreate is True and db exists, remove it

        # Create database and execute schema
        conn = sqlite3.connect(db_path)

        if db_exists == False or recreate == True:
            cls._load_schema(conn)

        db_proxy.initialize(conn)

        #db = cls()
        #return db

    # def close(self):
    #     self._conn.close()

