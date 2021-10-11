import discord
from discord.ext import commands
import youtube_dl
from collections import deque
import asyncio
from database import utils
from tabulate import tabulate


class playlist(commands.Cog):
    def __init__(self, client, playable):
        self.client = client
        self.addExtraCommands()
        self.playable = playable
        self.details = {}

    async def error(self, ctx, e):
        await ctx.send(e)

    async def help(self, ctx, *args):
        head = "Playlist features:\nSyntax: (&playlist|&pl) (-<instruction>) (<arg>)\n"
        headers = ["instruction", "description", "args"]
        playlist_rows = [
            ["-create | -c", "create a playlist", "<playlist name>"],
            ["-delete | -d", "delete a playlist", "<playlist name>"],
            ["-select | -s", "select a playlist", "<playlist name>"],
            ["-show   | -l", "show playlists", '"playlist"'],
        ]

        song_rows = [
            ["-add    | -a", "add song", "<song name>"],
            ["-remove | -r", "remove song", "<index>"],
            ["-show   | -l", "show playlists or songs", '"song"'],
            ["-play   | -p", "play songs in playlist", "-"],
            ["-help   | -h", "open manual", "-"],
        ]
        await ctx.send(
            head
            + "```"
            + tabulate(playlist_rows, headers=headers)
            + "\n\nFollowing commands can be used only after selecting a playlist:\n"
            + tabulate(song_rows, headers=headers)
            + "```"
        )

    def addExtraCommands(self):
        substitute = {
            "create": ["c"],
            "delete": ["d"],
            "select": ["s"],
            "add": ["a"],
            "show": ["l"],
            "play": ["p"],
            "remove": ["r"],
            "help": ["h"],
        }

        for subKey in substitute:
            for subValue in substitute[subKey]:
                setattr(playlist, subValue, getattr(playlist, subKey))

    async def create(self, ctx, inst, playlist, *args):
        author = str(ctx.author)
        import re

        pattern = "([a-zA-Z]\w*)"
        result = re.search(pattern, playlist)
        if result is None:
            raise Exception(
                "Playlist name has to start with an alphabet and can further contain numbers, alphabets and _"
            )
        playlist = result.group(1)

        if utils.playlistUtils.addPlaylist(author, playlist):
            await ctx.send(f"{author}: playlist created")
        else:
            await ctx.send(
                f"{author}: error occured while creating playlist or playlist already exists"
            )

    async def delete(self, ctx, inst, playlist, *args):
        author = str(ctx.author)
        if utils.playlistUtils.delPlaylist(author, playlist):
            await ctx.send(f"{author}: playlist, **{playlist}** deleted")
        else:
            await ctx.send(
                f"{author}: error occured while creating playlist or playlist already exists"
            )

    async def select(self, ctx, inst, playlist, *args):
        author = str(ctx.author)
        ob = utils.playlistUtils(author, playlist)
        if ob.exists_():
            if author in self.details:
                del self.details[author]
            self.details[author] = ob
            await ctx.send(f"{author}: has selected playlist, **{playlist}**")
        else:
            del ob
            await ctx.send(f"{author}: playlist, **{playlist}** doesn't exist")

    async def isPlaylistSelected(self, ctx):
        author = str(ctx.author)
        if author in self.details:
            return True
        await ctx.send(f"{author}: select a playlist first")
        return False

    async def showOptions(self, ctx, inst, option, *args):
        author = str(ctx.author)

        async def playlist():
            playlists = utils.playlistUtils.getPlaylists(author)
            msg = f"{author}'s playlists:\n"
            for i, pl in enumerate(playlists):
                msg += f"{i+1}. {pl[0]}\n"
            await ctx.send(msg)

        async def song(display=1):
            if not await self.isPlaylistSelected(ctx):
                return

            details = self.details[author]
            songs = details.getSongs_()
            if display:
                msg = f"{author}:'s songs in playlist, *{details.playlist}*\n"
                for i, song in enumerate(songs):
                    msg += f"{i+1}. {song['title']} - {song['channel']}\n"
                await ctx.send(msg)
            return songs

        if option in locals():
            return locals()[option]
        else:
            raise Exception(f"It's either *{inst} song* or *{inst} playlist*")

    async def show(self, ctx, inst, *args):
        await (await self.showOptions(ctx, inst, *args))()

    async def add(self, ctx, inst, *args):
        author = str(ctx.author)

        if not await self.isPlaylistSelected(ctx):
            return

        for arg in args:
            song = self.playable.ytsearch(arg)
            if self.details[author].addSong_(song):
                await ctx.send(f"{author}: *{song['title']}* added")
            else:
                await ctx.send(f"{author}: Error: *{song['title']}* not added")

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
                details = self.details[author]
                details.removeSong_(song["id"])
                await ctx.send(
                    f"{author}: *{song['title']}* is removed from playlist, **{details.playlist}**"
                )
        except:
            await ctx.send("Provide correct index for the playlist")

    async def play(self, ctx, inst, *args):
        author = str(ctx.author)

        if not await self.isPlaylistSelected(ctx):
            return

        showOptionsSong = await self.showOptions(ctx, inst, "song")
        songs = await showOptionsSong(0)

        await ctx.send(
            f"Playing {author}'s playlist, **{self.details[author].playlist}**\n"
        )
        for i, song in enumerate(songs):
            await self.playable.playSong(ctx, song["title"])

    @commands.command()
    async def playlist(self, ctx, *args):
        import re

        args = tuple(map(lambda arg: arg.lower(), args))

        try:
            pattern = r"-(.*)"
            result = re.search(pattern, args[0])
            inst = result.group(1)
            await getattr(playlist, inst)(self, ctx, *args)

        except Exception as e:
            await self.error(ctx, e)

    @commands.command()
    async def pl(self, ctx, *args):
        await self.playlist(ctx, *args)


def setup(client, playable):
    client.add_cog(playlist(client, playable))
