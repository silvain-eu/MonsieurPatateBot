import asyncio
import datetime
import io

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

from Database.PlanningScreen import PlanningScreen
from LoggerSetup import logger


class GameCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name="planning",
                       description="Recevoir un screen de l'ADE", options=[
            create_option(
                name="week",
                description="nombre de semaine en plus par rapport à aujourd'hui",
                option_type=SlashCommandOptionType.INTEGER,
                required=False
            ),
        ])
    async def planning(self, ctx: SlashContext, week: int = 0):
        date = (datetime.datetime.now() + datetime.timedelta(weeks=week)).isocalendar()
        year = date[0]
        week = date[1]
        screen = PlanningScreen.findOne(week, year)
        if screen is None:
            logger.WARN("[Planning] Erreur : pas de screen pour " + str(week) + " " + str(year) + ".")
            await ctx.send(content=("[Planning] pas de screen pour " + str(week) + " " + str(year) + "."), hidden=True)
            return

        with io.BytesIO(screen.file) as image_binary:
            image_binary.read()
            image_binary.seek(0)

            try:
                newMessage = await ctx.author.send(
                    file=discord.File(image_binary, filename="ADE-" + str(week) + "_" + str(year) + ".png"))
                await ctx.send(content="Envoyé par message privé.", hidden=True)
                logger.WARN("[Planning] Screen pour " + ctx.author.name + " du " + str(week) + "_" + str(year) + ".")

                dm = ctx.author.dm_channel
                if (dm is None):
                    dm = await ctx.author.create_dm()
                info = await ctx.bot.application_info()
                async for message in dm.history(limit=20):
                    if message.author.id == info.id and message.id != newMessage.id:
                        await message.delete()
                        await asyncio.sleep(0.5)
            except discord.errors.Forbidden:
                await ctx.send(content="[Erreur] Assuré vous d'avoir activé vos MP depuis un serveur.", hidden=True)


def setup(bot):
    bot.add_cog(GameCommand(bot))
