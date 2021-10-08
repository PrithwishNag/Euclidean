import discord
from discord.ext import commands
import youtube_dl
from collections import deque
import asyncio
from database import utils


class playlist(commands.Cog):
    def __init__(self, client, playable):
        self.client = client
        self.playable = playable
        self.details = {}

    @staticmethod
    async def help(ctx, e):
        await ctx.send(e)

    async def create(self, ctx, inst, *args):
        playlist = args[0]
        author = str(ctx.author)
        if utils.playlistUtils.addPlaylist(author, playlist):
            await ctx.send(f"{author}: playlist created")
        else:
            await ctx.send(
                f"{author}: error occured while creating playlist or playlist already exists"
            )

    async def select(self, ctx, inst, *args):
        playlist = args[0]
        author = str(ctx.author)
        ob = utils.playlistUtils(author, playlist)
        if ob.exists():
            if author in self.details:
                del self.details[author]
            self.details[author] = ob
            await ctx.send(f"{author}: has selected playlist, {playlist}")
        else:
            del ob
            await ctx.send(f"{author}: playlist, {playlist} doesn't exist")

    async def isPlaylistSelected(self, ctx):
        author = str(ctx.author)
        if author in self.details:
            return True
        await ctx.send(author + ": select a playlist first")
        return False

    async def showOptions(self, ctx, inst, *args):
        option = args[0]
        author = str(ctx.author)

        async def playlist():
            playlists = utils.playlistUtils.getPlaylists(author)
            msg = author + "'s playlists:\n"
            for i, pl in enumerate(playlists):
                msg += f"{i+1}. {pl[0]}"
            await ctx.send(msg)

        async def song(display):
            if not await self.isPlaylistSelected(ctx):
                return

            details = self.details[author]
            songs = details.getSongs()
            if display:
                msg = author + "'s songs in playlist, " + details.playlist + "\n"
                for i, song in enumerate(songs):
                    msg += f"{i+1}. {song[1]} - {song[2]}\n"
                await ctx.send(msg)
            return songs

        return locals()[option]

    async def show(self, ctx, inst, *args):
        await (await self.showOptions(ctx, inst, *args))(1)

    async def add(self, ctx, inst, *args):
        author = str(ctx.author)

        if not await self.isPlaylistSelected(ctx):
            return

        for arg in args:
            song = self.playable.ytsearch(arg)
            if self.details[author].addSongToPlaylist(song):
                await ctx.send(f"{author}: \"{song['title']}\" added")
            else:
                await ctx.send(f"{author}: ERROR: \"{song['title']}\" not added")

    async def remove(self, ctx, inst, *args):
        author = str(ctx.author)

        if not await self.isPlaylistSelected(ctx):
            return

        showOptionsSong = await self.showOptions(ctx, inst, "song")
        if args == ():
            await showOptionsSong(1)
            await ctx.send(
                "Select the index of the song to be deleted\nSyntax: &playlist -delete <index>"
            )
            return
        try:
            songs = await showOptionsSong(0)
            for arg in args:
                idx = int(arg)
                song = songs[idx - 1]
                title = song[1]
                details = self.details[author]
                details.removeSong(song[0])
                await ctx.send(
                    f"{author}: {title} is removed from playlist, {details.playlist}"
                )
        except:
            await ctx.send("Provide integer index")

    @commands.command()
    async def playlist(self, ctx, *args):
        import re

        try:
            pattern = r"-(.*)"
            result = re.search(pattern, args[0])
            inst = result.group(1)
            await getattr(playlist, inst)(self, ctx, *args)

        except Exception as e:
            await playlist.help(ctx, e)


def setup(client, playable):
    client.add_cog(playlist(client, playable))
