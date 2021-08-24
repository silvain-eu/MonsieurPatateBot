import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

from Utils import VoiceChannel
from Commands import ReloadGameCommand
from Database.AnnounceChannel import AnnounceChannel
from Database.Games import Game
from Database.DatabseManager import connect,disconnect

load_dotenv()
TOKEN = os.getenv('token')

intents = discord.Intents().default()
intents.members = True
intents.reactions = True

client = commands.Bot(command_prefix="!", intent=intents, help_command=None)
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True, override_type=True,
                     application_id=876096685892325376)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    # await slash.sync_all_commands(delete_from_unused_guilds=False)
    disconnect(connect())
    VoiceChannel.vocalCategory.start(client)
    await client.change_presence(activity=discord.Game(name="faire de frites", type=discord.ActivityType.playing))
    await ReloadGameCommand.reloadAllChannelAnnounce(client)


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    announce: AnnounceChannel = AnnounceChannel.findOne(payload.guild_id)
    if announce is None or announce.GameMessageId is None or payload.message_id != int(announce.GameMessageId):
        return

    guild: discord.Guild = client.get_guild(payload.guild_id)
    user: discord.Member = await guild.fetch_member(payload.user_id)

    if user.bot:
        return

    game: Game = Game.findOneByGuildEmoticon(announce.GuildId, payload.emoji._as_reaction())
    channel: discord.TextChannel = guild.get_channel(payload.channel_id)
    msg: discord.Message = await channel.fetch_message(int(announce.GameMessageId))

    if game is None:
        await msg.remove_reaction(payload.emoji, user)
        return

    role: discord.Role = guild.get_role(int(game.roleId))
    await user.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    announce: AnnounceChannel = AnnounceChannel.findOne(payload.guild_id)
    if announce is None or payload.message_id != int(announce.GameMessageId):
        return

    guild: discord.Guild = client.get_guild(payload.guild_id)
    user: discord.Member = await guild.fetch_member(payload.user_id)

    if user.bot:
        return

    game: Game = Game.findOneByGuildEmoticon(announce.GuildId, payload.emoji._as_reaction())

    role: discord.Role = guild.get_role(int(game.roleId))
    await user.remove_roles(role)


client.load_extension("Commands.GameCommand")
client.load_extension("Commands.ReloadGameCommand")
client.run(TOKEN)
