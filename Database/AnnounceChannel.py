import Database.DatabseManager


class AnnounceChannel(Database.DatabseManager.DataBaseObject):
    GuildId: str
    AnnounceChannelId: str
    GameMessageId: str = None

    @staticmethod
    def create(announceChannel):
        dbConn = Database.DatabseManager.connect();
        c = dbConn.cursor()
        c.execute(
            "INSERT INTO AnnounceChannel(GuidId,AnnounceChannelId, GameMessageId) values (?,?,?);"
            , (announceChannel.GuildId, announceChannel.AnnounceChannelId, announceChannel.GameMessageId,))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def update(announceChannel):
        dbConn = Database.DatabseManager.connect();
        c = dbConn.cursor()
        c.execute(
            "update AnnounceChannel Set AnnounceChannelId = ?, GameMessageId = ? where GuidId =?"
            , (announceChannel.AnnounceChannelId, announceChannel.GameMessageId, announceChannel.GuildId,))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def delete(announceChannel):
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "delete from AnnounceChannel where GuidId = ?;"
            , (announceChannel.GuildId,))
        dbConn.commit()
        Database.DatabseManager.disconnect(dbConn)

    @staticmethod
    def findAll():
        dbConn = Database.DatabseManager.connect()
        c = dbConn.cursor()
        c.execute(
            "select GuidId,AnnounceChannelId,GameMessageId from AnnounceChannel;")
        dbConn.commit()

        rows = c.fetchall()
        res = []
        for row in rows:
            res.append(AnnounceChannel.serialize(row))
        Database.DatabseManager.disconnect(dbConn)
        return res

    @staticmethod
    def findOne(guild: int):
        dbConn = Database.DatabseManager.connect();
        c = dbConn.cursor()
        c.execute(
            "select GuidId,AnnounceChannelId,GameMessageId from AnnounceChannel where GuidId = ? limit 1;",
            (str(guild),))
        dbConn.commit()

        res = c.fetchone()
        if res is None:
            return None
        Database.DatabseManager.disconnect(dbConn)
        return AnnounceChannel.serialize(res)

    @staticmethod
    def serialize(data):
        res = AnnounceChannel()
        res.GuildId = data[0]
        res.AnnounceChannelId = data[1]
        res.GameMessageId = data[2]

        return res
