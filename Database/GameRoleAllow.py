import sqlite3

import typing

import Database.DatabseManager
from datetime import datetime


class GameRoleAllow(Database.DatabseManager.DataBaseObject):
    GameId: int
    RoleId: str

    @staticmethod
    def create(game):
        dbConn = Database.DatabseManager.connect();
        c = dbConn.cursor()
        c.execute(
            "INSERT INTO GameRoleAllow(GameId, RoleId) values (?,?);"
            , (game.GameId, game.RoleId))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def delete(game):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "delete from GameRoleAllow where GameId = ? and RoleId = ?;"
            , (game.GameId, game.RoleId,))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def findAll():
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select GameId, RoleId from GameRoleAllow;", )
        dbConn.commit()

        rows = c.fetchall()
        res = []
        for row in rows:
            res.append(GameRoleAllow.serialize(row))
        Database.DatabseManager.disconnect(dbConn)
        return res

    @staticmethod
    def findByGame(gameId: int):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select GameId, RoleId from GameRoleAllow where GameId = ?;",
            (gameId,))
        dbConn.commit()

        rows = c.fetchall()
        res = []
        for row in rows:
            res.append(GameRoleAllow.serialize(row))
        Database.DatabseManager.disconnect(dbConn)
        return res

    @staticmethod
    def findOneByGameRole(GameId: int, RoleId: str):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select GameId, RoleId from GameRoleAllow where GameId = ? and RoleId = ?;",
            (GameId, RoleId,))
        dbConn.commit()

        res = c.fetchone()
        if res is None:
            return None
        Database.DatabseManager.disconnect(dbConn)
        return GameRoleAllow.serialize(res)

    @staticmethod
    def findOneByGameRolesList(GameId: int, RoleId: typing.List[str]):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select GameId, RoleId from GameRoleAllow where GameId = ? and RoleId in ('" + "','".join(RoleId) + "');",
            (GameId,))
        dbConn.commit()

        res = c.fetchone()
        if res is None:
            return None
        Database.DatabseManager.disconnect(dbConn)
        return GameRoleAllow.serialize(res)

    @staticmethod
    def serialize(data):
        res = GameRoleAllow()
        res.GameId = data[0]
        res.RoleId = data[1]

        return res
