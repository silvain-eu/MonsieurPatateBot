import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, SlashCommand
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType

from Commands import ReloadGameCommand
from Database.Games import Game


class GameCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name="addgame", description="ajout d un jeux", options=[
        create_option(
            name="name",
            description="nom du jeux",
            option_type=SlashCommandOptionType.STRING,
            required=True
        ), create_option(
            name="emoticon",
            description="emoticon",
            option_type=SlashCommandOptionType.STRING,
            required=True
        )
    ])
    async def addgame(self, ctx: SlashContext, name: str, emoticon: str):
        if Game.findOneByName(name, ctx.guild.id) is not None:
            print("[AddGame] " + name + " existe déjà.")
            await ctx.send(content=("[AddGame] " + name + " existe déjà."), hidden=True)
            return

        game: Game = Game()
        game.name = name
        game.emoticon = emoticon
        game.memberIdCreate = ctx.author.id
        game.memberUsernameCreate = ctx.author.name

        guild: discord.Guild = ctx.guild
        game.guildId = guild.id

        category: discord.CategoryChannel = await guild.create_category(name)
        game.categoryId = category.id

        role: discord.Role = await guild.create_role(name=name, mentionable=True, hoist=False,
                                                     permissions=discord.Permissions(0))
        game.roleId = role.id

        await category.set_permissions(ctx.guild.default_role, view_channel=False, connect=False, read_messages=False,
                                       send_messages=False, speak=False)
        await category.set_permissions(role, view_channel=True, connect=True, read_messages=True, send_messages=True,
                                       speak=True)

        await guild.create_text_channel("general", category=category, sync_permissions=True)
        await guild.create_voice_channel("Vocal#1", category=category, sync_permissions=True)

        Game.create(game)
        await ctx.send(content=("Ok ! <@&" + str(role.id) + ">"), hidden=True)
        await ReloadGameCommand.reloadChannelAnnounce(guild)

    @cog_ext.cog_slash(name="removegame", description="delete a game", options=[
        create_option(
            name="name",
            description="nom du jeux",
            option_type=SlashCommandOptionType.STRING,
            required=True
        )
    ])
    async def removegame(self, ctx: SlashContext, name: str):

        game: Game = Game.findOneByName(name, ctx.guild.id)
        if game is None:
            print("[RemoveGame] " + name + " n'existe pas.")
            await ctx.send(content=("[RemoveGame] " + name + " n'existe pas."), hidden=True)
            return

        guild: discord.Guild = ctx.guild
        role: discord.Role = guild.get_role(int(game.roleId))
        category: discord.CategoryChannel = discord.utils.get(guild.categories, id=int(game.categoryId))

        if category is not None:
            for c in category.channels:
                await c.delete(reason="Remove game : " + game.name)
            await category.delete(reason="Remove game : " + game.name)

        if role is not None:
            await role.delete(reason="Remove game : " + game.name)

        await ctx.send(content=("Aurevoir ! " + game.name), hidden=True)

        Game.delete(game)
        await ReloadGameCommand.reloadChannelAnnounce(guild)

        return


def setup(bot):
    bot.add_cog(GameCommand(bot))
