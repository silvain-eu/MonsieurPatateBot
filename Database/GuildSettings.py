import Database.DatabseManager


class GuildSettings(Database.DatabseManager.DataBaseObject):
    GuildId: str
    AnnounceChannelId: str
    SectionMessageId: str = None

    @staticmethod
    def create(announceChannel):
        dbConn = Database.DatabseManager.connect();
        c = dbConn.cursor()
        c.execute(
            "INSERT INTO guild_settings(GuildId,announce_channel_id, section_message_id) values (?,?,?);"
            , (announceChannel.GuildId, announceChannel.AnnounceChannelId, announceChannel.SectionMessageId,))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def update(announceChannel):
        dbConn = Database.DatabseManager.connect();
        c = dbConn.cursor()
        c.execute(
            "update guild_settings Set announce_channel_id = %s, section_message_id = %s where GuildId =%s"
            , (announceChannel.AnnounceChannelId, announceChannel.SectionMessageId, announceChannel.GuildId,))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def delete(announceChannel):
        pass

    @staticmethod
    def findAll():
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select GuildId,announce_channel_id,section_message_id from guild_settings;")

        rows = c.fetchall()
        res = []
        for row in rows:
            res.append(GuildSettings.serialize(row))
        Database.DatabseManager.disconnect(dbConn)
        return res

    @staticmethod
    def findOne(guild: int):
        dbConn = Database.DatabseManager.connect();
        c = dbConn.cursor()
        c.execute(
            "select GuildId,announce_channel_id,section_message_id from guild_settings where GuildId = %s limit 1;",
            (str(guild),))

        res = c.fetchone()
        if res is None:
            return None
        Database.DatabseManager.disconnect(dbConn)
        return GuildSettings.serialize(res)

    @staticmethod
    def serialize(data):
        res = GuildSettings()
        res.GuildId = data[0]
        res.AnnounceChannelId = data[1]
        res.SectionMessageId = data[2]

        return res
