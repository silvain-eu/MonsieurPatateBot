import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

from Database.RoleAllowSection import RoleAllowSection
from Utils import VoiceChannel
from Commands import ReloadGameCommand
from Database.GuildSettings import GuildSettings
from Database.Games import Section
from Database.DatabseManager import connect, disconnect
from Utils.AnnounceGameChannel import autoCreateSectionAnnounceChannel, on_announce_game_message

load_dotenv()
TOKEN = os.getenv('token')

intents = discord.Intents().default()
intents.members = True
intents.reactions = True

client = commands.Bot(command_prefix="!", intent=intents, help_command=None)
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True, override_type=True,
                     application_id=os.getenv("clientId"))


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    await slash.sync_all_commands(delete_from_unused_guilds=False)
    disconnect(connect())
    VoiceChannel.vocalCategory.start(client)
    await client.change_presence(activity=discord.Game(name="faire des frites", type=discord.ActivityType.playing))
    await ReloadGameCommand.reloadAllChannelAnnounce(client)
    await autoCreateSectionAnnounceChannel(client)


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    announce: GuildSettings = GuildSettings.findOne(payload.guild_id)
    if announce is None or announce.SectionMessageId is None or payload.message_id != int(announce.SectionMessageId):
        return

    guild: discord.Guild = client.get_guild(payload.guild_id)
    user: discord.Member = await guild.fetch_member(payload.user_id)

    if user.bot:
        return

    game: Section = Section.findOneByGuildEmoticon(announce.GuildId, payload.emoji._as_reaction())
    channel: discord.TextChannel = guild.get_channel(payload.channel_id)
    msg: discord.Message = await channel.fetch_message(int(announce.SectionMessageId))

    if game is None:
        await msg.remove_reaction(payload.emoji, user)
        return

    role: discord.Role = guild.get_role(int(game.roleId))
    if game.visibility == "RESTRICT":
        listRole = []
        for r in user.roles:
            listRole.append(str(r.id))
        if RoleAllowSection.findOneByGameRolesList(game.id, listRole) is None:
            await msg.remove_reaction(payload.emoji, user)
            return

    await user.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    announce: GuildSettings = GuildSettings.findOne(payload.guild_id)
    if announce is None or payload.message_id != int(announce.SectionMessageId):
        return

    guild: discord.Guild = client.get_guild(payload.guild_id)
    user: discord.Member = await guild.fetch_member(payload.user_id)

    if user.bot:
        return

    game: Section = Section.findOneByGuildEmoticon(announce.GuildId, payload.emoji._as_reaction())

    role: discord.Role = guild.get_role(int(game.roleId))
    await user.remove_roles(role)


@client.event
async def on_message(message: discord.Message):
    await on_announce_game_message(message)


client.load_extension("Commands.GameCommand")
client.load_extension("Commands.ReloadGameCommand")
client.load_extension("Commands.AnnounceMessageCommand")
client.run(TOKEN)
