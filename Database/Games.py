import sqlite3

import typing

import uuid
import Database.DatabseManager
from datetime import datetime


class Section(Database.DatabseManager.DataBaseObject):
    id: str
    name: str
    guildId: str
    categoryId: str
    roleId: str
    dateCreate: str
    memberIdCreate: str
    memberUsernameCreate: str
    emoticon: str
    visibility: str = "SHOW"
    AnnounceChannelId: str = None

    @staticmethod
    def create(game):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        game.dateCreate = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        game.id = str(uuid.uuid4())
        c.execute(
            "INSERT INTO section(id, name, server_id, category_id, role_id, date, creator_id, creator_name,emoji,visibility,announce_channel_id)"
            " values (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            , (game.id, game.name, game.guildId, game.categoryId, game.roleId, game.dateCreate, game.memberIdCreate,
               game.memberUsernameCreate, game.emoticon, game.visibility, game.AnnounceChannelId,))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def delete(game):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "delete from section where id = %s;"
            , (game.id,))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def findAll():
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select id, name, gs.GuildId, category_id, role_id, date, creator_id, creator_name, emoji,visibility, section.announce_channel_id from section"
            " inner join guild_settings gs on section.server_id = gs.GuildId;")

        rows = c.fetchall()
        res = []
        for row in rows:
            res.append(Section.serialize(row))
        Database.DatabseManager.disconnect(dbConn)
        return res

    @staticmethod
    def findOneByGuildAndCategory(guildId: str, CategoryId: str):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select id, name, gs.GuildId, category_id, role_id, date,creator_id, creator_name, emoji,visibility,section.announce_channel_id  from section "
            "inner join guild_settings gs on section.server_id = gs.GuildId "
            "where gs.GuildId = %s and category_id = %s;",
            (guildId, CategoryId,))

        res = c.fetchone()
        if res is None:
            return None
        Database.DatabseManager.disconnect(dbConn)
        return Section.serialize(res)

    @staticmethod
    def findByGuild(guildId: str):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select id, name, gs.GuildId, category_id, role_id, date,creator_id, creator_name, emoji,visibility,section.announce_channel_id  from section "
            "inner join guild_settings gs on section.server_id = gs.GuildId "
            "where gs.GuildId = %s and (visibility like 'SHOW' or visibility like 'RESTRICT');",
            (guildId,))

        rows = c.fetchall()
        res = []
        for row in rows:
            res.append(Section.serialize(row))
        Database.DatabseManager.disconnect(dbConn)
        return res

    @staticmethod
    def findOneByGuildEmoticon(guildId: str, emoticon: str):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select id, name, gs.GuildId, category_id, role_id, date, creator_id, creator_name, emoji,visibility,section.announce_channel_id from section "
            "inner join guild_settings gs on section.server_id = gs.GuildId"
            " where guildId = %s and emoji = %s limit 1;",
            (guildId, emoticon,))

        res = c.fetchone()
        if res is None:
            return None
        Database.DatabseManager.disconnect(dbConn)
        return Section.serialize(res)

    @staticmethod
    def findOneByName(name: str, guild: int):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select id, name, gs.GuildId, category_id, role_id, date, creator_id, creator_name, emoji, visibility,section.announce_channel_id from section"
            " inner join guild_settings gs on section.server_id = gs.GuildId "
            "where name like %s and guildId = %s limit 1;",
            (name, str(guild),))

        res = c.fetchone()
        if res is None:
            return None
        Database.DatabseManager.disconnect(dbConn)
        return Section.serialize(res)

    @staticmethod
    def update(game):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "update section Set name = %s, category_id = %s, role_id = %s, date = %s, creator_id = %s, "
            "creator_name = %s,emoji = %s,section.visibility = %s, announce_channel_id = %s"
            " where id = %s;"
            , (game.name, game.categoryId, game.roleId, game.dateCreate, game.memberIdCreate,
               game.memberUsernameCreate, game.emoticon, game.visibility, game.AnnounceChannelId, game.id,))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def serialize(data):
        res = Section()
        res.id = data[0]
        res.name = data[1]
        res.guildId = data[2]
        res.categoryId = data[3]
        res.roleId = data[4]
        res.dateCreate = data[5]
        res.memberIdCreate = data[6]
        res.memberUsernameCreate = data[7]
        res.emoticon = data[8].decode("utf-8")
        res.visibility = data[9]
        res.AnnounceChannelId = data[10]

        return res
