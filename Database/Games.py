import sqlite3

import typing

import Database.DatabseManager
from datetime import datetime


class Game(Database.DatabseManager.DataBaseObject):
    id: int
    name: str
    guildId: str
    categoryId: str
    roleId: str
    dateCreate: str
    memberIdCreate: str
    memberUsernameCreate: str
    emoticon: str
    restricted: bool = False
    show: bool = True

    @staticmethod
    def create(game):
        dbConn = Database.DatabseManager.connect();
        c = dbConn.cursor()
        game.dateCreate = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        c.execute(
            "INSERT INTO Game(name, guildId, categoryId, roleId, dateCreate, memberIdCreate, memberUsernameCreate,emoticon,restricted, show) values (?,?,?,?,?,?,?,?,?,?);"
            , (game.name, game.guildId, game.categoryId, game.roleId, game.dateCreate, game.memberIdCreate,
               game.memberUsernameCreate, game.emoticon, game.restricted, game.show))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def delete(game):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "delete from Game where id = ?;"
            , (game.id,))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def findAll():
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select id, name, guildId, categoryId, roleId, dateCreate, memberIdCreate, memberUsernameCreate, emoticon, restricted, show from Game;")
        dbConn.commit()

        rows = c.fetchall()
        res = []
        for row in rows:
            res.append(Game.serialize(row))
        Database.DatabseManager.disconnect(dbConn)
        return res

    @staticmethod
    def findByGuild(guildId: str):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select id, name, guildId, categoryId, roleId, dateCreate, memberIdCreate, memberUsernameCreate, emoticon,restricted,show from Game where guildId = ? and show = 1;",
            (guildId,))
        dbConn.commit()

        rows = c.fetchall()
        res = []
        for row in rows:
            res.append(Game.serialize(row))
        Database.DatabseManager.disconnect(dbConn)
        return res

    @staticmethod
    def findOneByGuildEmoticon(guildId: str, emoticon: str):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select id, name, guildId, categoryId, roleId, dateCreate, memberIdCreate, memberUsernameCreate, emoticon,restricted,show from Game where guildId = ? and emoticon = ? limit 1;",
            (guildId, emoticon,))
        dbConn.commit()

        res = c.fetchone()
        if res is None:
            return None
        Database.DatabseManager.disconnect(dbConn)
        return Game.serialize(res)

    @staticmethod
    def findOneByName(name: str, guild: int):
        dbConn = Database.DatabseManager.connect();
        c = dbConn.cursor()
        c.execute(
            "select id, name, guildId, categoryId, roleId, dateCreate, memberIdCreate, memberUsernameCreate, emoticon,restricted,show from Game where name like ? and guildId = ? limit 1;",
            (name, str(guild),))
        dbConn.commit()

        res = c.fetchone()
        if res is None:
            return None
        Database.DatabseManager.disconnect(dbConn)
        return Game.serialize(res)

    @staticmethod
    def serialize(data):
        res = Game()
        res.id = data[0]
        res.name = data[1]
        res.guildId = data[2]
        res.categoryId = data[3]
        res.roleId = data[4]
        res.dateCreate = data[5]
        res.memberIdCreate = data[6]
        res.memberUsernameCreate = data[7]
        res.emoticon = data[8]
        res.restricted = data[9] == 1
        res.show = data[10] == 1

        return res
