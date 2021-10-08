import discord
from discord.ext import commands
import youtube_dl
from collections import deque
import asyncio
from database import utils


class playlist(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.details = {}

    @commands.command()
    async def playlist(self, ctx, *arg):
        print(ctx.author)
        print(arg)


def setup(client):
    client.add_cog(playlist(client))
