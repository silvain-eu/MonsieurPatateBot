from abc import ABC, abstractmethod
import sqlite3
import mysql.connector
import os
from datetime import datetime


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
    dbConn = mysql.connector.connect(
        host=os.getenv("db_host"),
        user=os.getenv("db_username"),
        password=os.getenv("db_password"),
        database=os.getenv("db_database"),
    )

    return dbConn


def disconnect(conn: mysql.connector.MySQLConnection):
    conn.close()
    # print("Closed database successfully")
