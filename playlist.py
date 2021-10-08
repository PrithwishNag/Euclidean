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

    @staticmethod
    async def help(ctx, e):
        await ctx.send(e)

    async def create(self, ctx, playlist, *args):
        author = str(ctx.author)
        if utils.playlistUtils.addPlaylist(author, playlist):
            await ctx.send(author + ": playlist created")
        else:
            await ctx.send(
                author
                + ": error occured while creating playlist or playlist already exists"
            )

    async def select(self, ctx, playlist, *args):
        author = str(ctx.author)
        ob = utils.playlistUtils(author, playlist)
        if ob.exists():
            if author in self.details:
                del self.details[author]
            self.details[author] = ob
            await ctx.send(author + ": has selected playlist, " + playlist)
        else:
            del ob
            await ctx.send(author + ": playlist, " + playlist + " doesn't exist")

    async def show(self, ctx, option, *args):
        author = str(ctx.author)

        async def playlist():
            playlists = utils.playlistUtils.getPlaylists(author)
            msg = author + "'s playlists:\n"
            for i, pl in enumerate(playlists):
                msg += f"{i+1}. {pl[0]}"
            await ctx.send(msg)

        async def song():
            if author in self.details:
                pass
            else:
                await ctx.send(author + ": select a playlist first")

        await locals()[option]()

    @commands.command()
    async def playlist(self, ctx, *args):
        import re

        try:
            pattern = r"-(.*)"
            result = re.search(pattern, args[0])
            inst = result.group(1)
            await getattr(playlist, inst)(self, ctx, args[1], *args[2:])

        except Exception as e:
            await playlist.help(ctx, e)


def setup(client):
    client.add_cog(playlist(client))
