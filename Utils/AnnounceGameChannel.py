import typing

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashCommandOptionType, SlashContext
from discord_slash.utils.manage_commands import create_option

from Database.Games import Game


async def autoCreateSectionAnnounceChannel(client: discord.Client):
    games: typing.List[Game] = Game.findAll()
    for game in games:
        g: discord.Guild = client.get_guild(int(game.guildId))

        if g is not None:
            ch = None
            if game.AnnounceChannelId is not None:
                ch = g.get_channel(int(game.AnnounceChannelId))

            if ch is None:
                for c in g.channels:
                    if c.category_id is not None and c.category_id == int(game.categoryId) and "annonce" in c.name:
                        ch = c

                if ch is None:
                    ch: discord.TextChannel = await g.create_text_channel("📢annonce",
                                                                          category=discord.utils.get(g.categories,
                                                                                                     id=int(
                                                                                                         game.categoryId)),
                                                                          position=0,
                                                                          sync_permissions=True)

                game.AnnounceChannelId = ch.id
                Game.update(game)


async def on_announce_game_message(message: discord.Message, onlyAnnounceChannel: bool = True):
    if message.author.bot:
        if message.type == discord.MessageType.pins_add:
            game: Game = Game.findOneByGuildAndCategory(message.guild.id, message.channel.category_id)
            if game is not None:
                await message.delete()
        return
    ch: discord.TextChannel = message.channel
    game: Game = Game.findOneByGuildAndCategory(message.guild.id, ch.category_id)
    if game is not None:
        if onlyAnnounceChannel:
            if game.AnnounceChannelId is None and ch.name.contains("annonce"):
                game.AnnounceChannelId = str(ch.id)
                Game.update(game)
            if game.AnnounceChannelId is None or game.AnnounceChannelId != str(ch.id):
                return
        else:
            ch = None
            if game.AnnounceChannelId is not None:
                ch = message.guild.get_channel(int(game.AnnounceChannelId))

            if ch is None:
                for c in message.guild.channels:
                    if c.category_id is not None and c.category_id == int(game.categoryId) and "annonce" in c.name:
                        ch = c

                if ch is None:
                    ch: discord.TextChannel = await message.guild.create_text_channel("📢annonce",
                                                                                      category=discord.utils.get(
                                                                                          message.guild.categories,
                                                                                          id=int(
                                                                                              game.categoryId)),
                                                                                      position=0,
                                                                                      sync_permissions=True)

        member: discord.Member = await message.guild.fetch_member(message.author.id)

        embed = discord.Embed(title="Annonce",
                              description=message.content,
                              color=member.top_role.color)

        embed.set_author(name=member.display_name,
                         icon_url=member.avatar_url)

        mention = ''
        for m in message.mentions:
            mention = mention + m.mention
        for m in message.role_mentions:
            mention = mention + m.mention

        await ch.send(embed=embed, content=mention, )
        if len(message.attachments) > 0:
            await ch.send(files=[await f.to_file() for f in message.attachments])

        if game.AnnounceChannelId == str(message.channel.id):
            await message.delete()
        else:
            await message.pin()
