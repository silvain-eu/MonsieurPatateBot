import traceback
from abc import ABC, abstractmethod
import sqlite3
import mysql.connector
import os
from datetime import datetime

from LoggerSetup import logger


class DataBaseObject(ABC):

    @staticmethod
    @abstractmethod
    def create():
        ...

    @staticmethod
    @abstractmethod
    def findAll():
        ...

    @staticmethod
    @abstractmethod
    def serialize(data):
        ...


def connect(db: str = "Data/potatoes.db"):
    try:
        dbConn = mysql.connector.connect(
            host=os.getenv("db_host"),
            user=os.getenv("db_username"),
            password=os.getenv("db_password"),
            database=os.getenv("db_database"),
        )
    except Exception as ex:
        logger.critical(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))
        raise ex

    return dbConn


def disconnect(conn: mysql.connector.MySQLConnection):
    conn.close()
    # print("Closed database successfully")
