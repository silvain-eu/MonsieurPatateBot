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
            "INSERT INTO allow_user_command(member_id) values (%s);"
            , (game.MemberId,))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def delete(game):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "delete from allow_user_command where member_id = %s;"
            , (game.MemberId,))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def findAll():
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select member_id from allow_user_command;", )

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
            "select member_id from allow_user_command where member_id = %s;",
            (userId,))

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
