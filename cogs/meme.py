import asyncio
from os import replace
import re
import aiohttp
from aiohttp.helpers import current_task
import discord
import wavelink
from essentials.player import WebPlayer
from discord.ext import commands
from essentials.checks import in_same_channel, player_connected, voice_connected
import urllib
import json


class Meme(commands.Cog):
    """Comandos De Meme"""

    def __init__(self, bot):
        self.bot = bot
        self.URL_REG = re.compile(r"https?://(?:www\.)?.+")

    @commands.command(name="meme", aliases=["m"])
    async def meme(self, ctx):
        """Exibe um meme aleatório"""
        memeAPI = urllib.request.urlopen('https://meme-api.herokuapp.com/gimme/DiretoDoZapZap')
        memeData = json.load(memeAPI)

        memeUrl = memeData['url']
        memeName = memeData['title']

        embed = discord.Embed(title=memeName, colour=discord.Colour.purple())
        embed.set_image(url=memeUrl)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Meme(bot))
