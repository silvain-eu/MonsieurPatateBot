from abc import ABC, abstractmethod
import sqlite3
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


class Migration(object):
    id: str
    sql: str
    date: str

    def __init__(self, sqlFile: str):
        self.id = sqlFile.replace(".sql", "")
        self.sql = open(os.path.dirname(os.path.abspath(__file__)) + "/Migrations/" + sqlFile, "r").read()
        self.date = None

    def isApply(self):
        return self.date is not None

    def load(self, dbConn: sqlite3.Connection):
        c = dbConn.cursor()
        c.execute("SELECT date from __Migration where id = ?;", (self.id,))
        dbConn.commit()

        res = c.fetchone()
        if res is not None:
            self.date = res[0]

    def apply(self, dbConn: sqlite3.Connection):
        c = dbConn.cursor()
        self.date = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        c.executescript(
            f"INSERT INTO __Migration(id, sql, date) VALUES('{self.id}','{self.sql}','{self.date}');"
            + self.sql)

        print("Application migration " + self.id)

        dbConn.commit()


def connect(db: str = "potatoes.db"):
    dbConn = sqlite3.connect(db)

    c = dbConn.cursor()
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='__Migration';")
    dbConn.commit()

    if c.fetchone()[0] == 0:
        c = dbConn.cursor()
        c.execute("""create table __Migration
            (
                id TEXT
                    constraint __Migration_pk
                        primary key,
                sql text,
                date text
            );
        """)
        dbConn.commit()
        print("Création de la table de migration ")

    loadMigration(dbConn)

    return dbConn


def disconnect(dbConn: sqlite3.Connection):
    dbConn.close()
    # print("Closed database successfully")


def loadMigration(dbConn: sqlite3.Connection):
    migrations = []
    for file in os.listdir(os.path.dirname(os.path.abspath(__file__)) + "/Migrations"):
        if file.endswith(".sql"):
            migration = Migration(file)
            migration.load(dbConn)
            migrations.append(migration)
    migrations = sorted(migrations, key=lambda x: x.id, reverse=False)

    for m in migrations:
        if not m.isApply():
            m.apply(dbConn)
