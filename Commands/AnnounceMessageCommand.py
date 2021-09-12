import discord
from discord import Guild
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

from Commands import ReloadGameCommand
from Database.AllowUserCommand import AllowUserCommand
from Database.Games import Game
from Utils.AnnounceGameChannel import on_announce_game_message


class AnnounceMessageCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="announcemsg", description="Annoncer le message", options=[
        create_option(
            name="msg",
            description="Message d'annonce",
            option_type=SlashCommandOptionType.STRING,
            required=True
        ),
    ])
    async def announcemsg(self, ctx: SlashContext, msg: str):

        if AllowUserCommand.accessDeniedUser(ctx.author_id):
            await ctx.send(content=("ERROR : Non autorisé !!!"), hidden=True)
            return

        channel: discord.TextChannel = ctx.channel
        try:
            message: discord.Message = await channel.fetch_message(int(msg))
        except:
            await ctx.send(content=("ERROR : Message non trouvé !!!"), hidden=True)
            return

        game: Game = Game.findOneByGuildAndCategory(ctx.guild_id, channel.category_id)
        if game is None:
            await ctx.send(content=("ERROR : Aucune section pour ce message !!!"), hidden=True)
            return
        await on_announce_game_message(message, False)
        await ctx.send(content=("Ok !!!"), hidden=True)
        return


def setup(bot):
    bot.add_cog(AnnounceMessageCommand(bot))
