import os
import sys

import discord
import typing

from discord.ext import commands
from discord_slash import cog_ext, SlashCommandOptionType, SlashContext
from discord_slash.utils.manage_commands import create_option

from Database.AnnounceChannel import AnnounceChannel
from Database.Games import Game


async def reloadChannelAnnounce(g: discord.Guild, clear: bool = False):
    announceChannel: AnnounceChannel = AnnounceChannel.findOne(g.id)
    if announceChannel is not None:
        channel: discord.TextChannel = g.get_channel(int(announceChannel.AnnounceChannelId))

        msg: discord.Message = None
        if clear:
            await channel.purge(limit=sys.maxsize)
        else:
            try:
                msg = await channel.fetch_message(int(announceChannel.GameMessageId))
            except:
                msg = None

        embed = discord.Embed(title="Accès aux sections",
                              description="Cliquez sur les mentions pour être à ajouter au groupe de la section.",
                              color=discord.Color.dark_gold())
        # embed.set_author(name="Monsieur Patate",
        #                  icon_url="https://cdn.discordapp.com/avatars/876096685892325376/8b81d5f2d0970e9cc521dcf99978dc48.png?size=128")

        games: typing.List[Game] = Game.findByGuild(g.id)
        list = ''
        for game in games:
            list += game.emoticon + " : " + game.name + "\n"

        if list != '':
            embed.add_field(name="List des sections :", value=list, inline=False)

        if msg is not None:
            await msg.edit(embed=embed)
        else:
            msg = await channel.send(embed=embed)

        for r in msg.reactions:
            game: Game = Game.findOneByGuildEmoticon(g.id, r.emoji)
            if game is None:
                async for user in r.users():
                    if os.getenv("clientId") == str(user.id):
                        await msg.remove_reaction(r.emoji, user)

        for game in games:
            await msg.add_reaction(game.emoticon)

        announceChannel.GameMessageId = msg.id
        AnnounceChannel.update(announceChannel)


async def reloadAllChannelAnnounce(client: discord.Client):
    guilds: typing.List[discord.Guild] = client.guilds

    for g in guilds:
        await reloadChannelAnnounce(g)


class ReloadGameCommand(commands.Cog):
    bot: discord.Client

    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name="setannouncechannel", description="on fixe le channel d annonce", options=[
        create_option(
            name="channel",
            description="channel de l'annonce",
            option_type=SlashCommandOptionType.CHANNEL,
            required=False
        ),
    ])
    async def setannouncechannel(self, ctx: SlashContext,
                                 channel: typing.Union[discord.VoiceChannel, discord.TextChannel] = None):

        if channel is not None:
            if channel.type != discord.ChannelType.text:
                await ctx.send("Pas un channel texte", hidden=True)
        else:
            channel = ctx.channel

        announce: AnnounceChannel = AnnounceChannel.findOne(ctx.guild.id)

        if announce is None:
            announce = AnnounceChannel()
            announce.GuildId = ctx.guild_id
            announce.AnnounceChannelId = channel.id
            AnnounceChannel.create(announce)
        else:
            if announce.AnnounceChannelId != channel.id:
                try:
                    lastChannel: discord.TextChannel = ctx.guild.get_channel(int(announce.AnnounceChannelId))
                    msg: discord.Message = await lastChannel.fetch_message(int(announce.GameMessageId))
                    await msg.delete()
                except:
                    ...
                announce.GameMessageId = None

            announce.AnnounceChannelId = channel.id
            AnnounceChannel.update(announce)

        perm: discord.PermissionOverwrite = discord.PermissionOverwrite(manage_channels=True, view_channel=True,
                                                                        read_messages=True,
                                                                        send_messages=True)
        await channel.set_permissions(self.bot.user, overwrite=perm)

        perm = discord.PermissionOverwrite(manage_channels=False, view_channel=True,
                                           read_messages=True,
                                           send_messages=False, read_message_history=True)
        await channel.set_permissions(ctx.guild.default_role, overwrite=perm)

        await reloadChannelAnnounce(ctx.guild, True)
        await ctx.send("Fait ! Nouveau channel d'annonce !!", hidden=True)

    @cog_ext.cog_slash(name="reloadannouncechannel", description="on recharge le channel d annonce", options=[
        create_option(
            name="clear",
            description="vide le channel",
            option_type=SlashCommandOptionType.BOOLEAN,
            required=False
        ),
    ])
    async def reloadannouncechannel(self, ctx: SlashContext, clear: bool = False):
        await reloadChannelAnnounce(ctx.guild, clear)
        await ctx.send(content=("Reloaded !!"), hidden=True)


def setup(bot):
    bot.add_cog(ReloadGameCommand(bot))
