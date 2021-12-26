import os
import typing
import discord
from discord.ext import tasks

from Database.Games import Section


async def updateVoiceChannel(chs: typing.List[discord.VoiceChannel]):
    chs: typing.List[discord.VoiceChannel] = sorted(chs, key=lambda x: int(x.name.replace("Vocal#", "")))
    lastLenChs: int = len(chs)

    for j in range(1, lastLenChs):
        i = lastLenChs - j
        r: discord.VoiceChannel = chs[i]
        prev: discord.VoiceChannel = chs[i - 1]

        if (len(r.members) == 0):
            if (len(prev.members) == 0):
                await r.delete(reason="Auto vocal channel")
                chs = chs[0:i]
        elif len(prev.members) == 0:
            ch = prev;
            for c in chs:
                if len(c.members) == 0:
                    ch = c
                    break
            for m in r.members:
                await m.move_to(ch, reason="Auto vocal channel")

    if (len(chs) != 0):
        last = chs[len(chs) - 1]
        if len(last.members) != 0:
            await last.guild.create_voice_channel(
                f"Vocal#" + str(int(last.name.replace("Vocal#", "")) + 1), overwrites=None,
                category=last.category,
                reason="Auto vocal channel")


@tasks.loop(seconds=10)
async def vocalCategory(client: discord.Client):
    for g in client.guilds:
        chs = []
        for c in g.channels:
            if c.name.startswith("Vocal#"):
                if c.type.name == 'voice' and c.category is not None and c.category.name == os.getenv(
                        "voiceCategoryName"):
                    chs.append(c)

        await updateVoiceChannel(chs)

    games: typing.List[Section] = Section.findAll()
    for game in games:
        g: discord.Guild = client.get_guild(int(game.guildId))
        chs: typing.List[discord.VoiceChannel] = []
        if g is not None:
            for c in g.channels:
                if c.name.startswith("Vocal#"):
                    if c.type.name == 'voice' and c.category is not None and c.category.id == int(game.categoryId):
                        chs.append(c)

            await updateVoiceChannel(chs)
