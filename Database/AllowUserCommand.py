import sqlite3

import typing

import Database.DatabseManager
from datetime import datetime


class AllowUserCommand(Database.DatabseManager.DataBaseObject):
    MemberId: str

    @staticmethod
    def create(game):
        dbConn = Database.DatabseManager.connect();
        c = dbConn.cursor()
        c.execute(
            "INSERT INTO AllowUserCommand(MemberId) values (?);"
            , (game.MemberId,))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def delete(game):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "delete from AllowUserCommand where MemberId = ?;"
            , (game.MemberId,))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def findAll():
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select MemberId from AllowUserCommand;", )
        dbConn.commit()

        rows = c.fetchall()
        res = []
        for row in rows:
            res.append(AllowUserCommand.serialize(row))
        Database.DatabseManager.disconnect(dbConn)
        return res

    @staticmethod
    def findByUser(userId: str):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select MemberId from AllowUserCommand where MemberId = ?;",
            (userId,))
        dbConn.commit()

        res = c.fetchone()
        if res is None:
            return None
        Database.DatabseManager.disconnect(dbConn)
        return AllowUserCommand.serialize(res)

    @staticmethod
    def accessDeniedUser(userId: str) -> bool:
        return AllowUserCommand.findByUser(userId) is  None

    @staticmethod
    def serialize(data):
        res = AllowUserCommand()
        res.MemberId = data[0]

        return res
