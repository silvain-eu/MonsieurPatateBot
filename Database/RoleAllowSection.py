import sqlite3

import typing

import Database.DatabseManager
from datetime import datetime


class RoleAllowSection(Database.DatabseManager.DataBaseObject):
    GameId: int
    RoleId: str

    @staticmethod
    def create(game):
        dbConn = Database.DatabseManager.connect();
        c = dbConn.cursor()
        c.execute(
            "INSERT INTO role_allow_section(SectionId, role_id) values (%s,%s);"
            , (game.GameId, game.RoleId))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def delete(game):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "delete from role_allow_section where SectionId = %s and role_id = %s;"
            , (game.GameId, game.RoleId,))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def findAll():
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select SectionId, role_id from role_allow_section;", )

        rows = c.fetchall()
        res = []
        for row in rows:
            res.append(RoleAllowSection.serialize(row))
        Database.DatabseManager.disconnect(dbConn)
        return res

    @staticmethod
    def findByGame(gameId: int):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select SectionId, role_id from role_allow_section where SectionId = %s;",
            (gameId,))

        rows = c.fetchall()
        res = []
        for row in rows:
            res.append(RoleAllowSection.serialize(row))
        Database.DatabseManager.disconnect(dbConn)
        return res

    @staticmethod
    def findOneByGameRole(GameId: int, RoleId: str):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select SectionId, role_id from role_allow_section where SectionId = %s and role_id = %s;",
            (GameId, RoleId,))

        res = c.fetchone()
        if res is None:
            return None
        Database.DatabseManager.disconnect(dbConn)
        return RoleAllowSection.serialize(res)

    @staticmethod
    def findOneByGameRolesList(GameId: int, RoleId: typing.List[str]):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select SectionId, role_id from role_allow_section "
            " where SectionId = %s and role_id in ('" + "','".join(
                RoleId) + "');",
            (GameId,))

        res = c.fetchone()
        if res is None:
            return None
        Database.DatabseManager.disconnect(dbConn)
        return RoleAllowSection.serialize(res)

    @staticmethod
    def serialize(data):
        res = RoleAllowSection()
        res.GameId = data[0]
        res.RoleId = data[1]

        return res
