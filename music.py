import discord
from discord.ext import commands
import youtube_dl
from collections import deque
import asyncio


class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.vc = None
        self.is_paused = False
        self.OPTIONS = {
            "FFMPEG": {
                "before_options": "-reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 2",
                "options": "-map 0:a:0 -b:a 96k -vn",
            },
            "YDL": {"format": "bestaudio", "noplaylist": "True"},
        }
        self.ydl = youtube_dl.YoutubeDL(self.OPTIONS["YDL"])
        self.search_queue = deque()
        self.lock = asyncio.Lock()

    async def help(self, ctx, prefix):
        title = f"""Euclidean Music"""
        desc = """Prefix: %s
        Syntax: &<instruction> <args>
        Instructions:
        ```""" % (prefix,)
        docs = ["connect       connect to a voice channel",
                "disconnect    disconnect from a voice channel",
                "play          play song from youtube",
                "skip          skip the current song",
                "pause         pause the current song",
                "resume        resume the current song",
                "empty         empty the queue of songs",
                "show          show the queue of songs",]
        for d in docs:
            desc += d+"\n"
        desc += "```"
        embed = discord.Embed(title=title, description=desc)
        await ctx.send(embed=embed)

    @commands.command()
    async def connect(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Please join a voice channel.")
            return 0
        vc = ctx.author.voice.channel
        if ctx.voice_client is None:
            await vc.connect()
        else:
            await ctx.voice_client.move_to(vc)
        self.vc = ctx.voice_client
        return 1

    def reset(self):
        self.vc = None
        self.is_paused = False
        del self.search_queue
        self.search_queue = deque()

    @commands.command()
    async def disconnect(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("Not connected to be disconected.")
            return
        self.reset()
        await ctx.voice_client.disconnect()

    def ytsearch(self, search):
        song = {}
        info = self.ydl.extract_info(f"ytsearch:{search}", download=False)["entries"][0]
        song["url"] = info["formats"][0]["url"]
        song["title"] = info["title"]
        song["channel"] = info["channel"]
        return song

    async def play_next(self, ctx):
        if not self.search_queue:
            if self.vc is not None:
                await self.disconnect(ctx)
            return

        search = self.search_queue[0]
        self.search_queue.popleft()

        song = self.ytsearch(search)
        source = await discord.FFmpegOpusAudio.from_probe(
            # executable="C:/ffmpeg/bin/ffmpeg.exe",
            source=song["url"],
            **self.OPTIONS["FFMPEG"],
        )

        await ctx.send(f"Playing \"{song['title']}\" - {song['channel']}")
        self.vc.play(
            source,
            after=lambda err: asyncio.run_coroutine_threadsafe(
                self.play_next(ctx), self.client.loop
            ),
        )

    async def playSong(self, ctx, search):
        if ctx.voice_client is None and not await self.connect(ctx):
            return

        self.search_queue.append(search)

        async with self.lock:
            if not self.vc.is_playing() and not self.is_paused:
                await self.play_next(ctx)
            else:
                await ctx.send(f'Added to queue *{search}*')

    @commands.command()
    async def play(self, ctx, *args):
        # Process Search
        search = (" ".join(args)).lower()
        # Play
        await self.playSong(ctx, search)

    @commands.command()
    async def p(self, ctx, *args):
        await self.play(ctx, *args)

    @commands.command()
    async def pause(self, ctx):
        if self.vc is not None and self.vc.is_playing():
            self.vc.pause()
            self.is_paused = True
            await ctx.send("Paused")
        else:
            await ctx.send("Play something first.")

    @commands.command()
    async def resume(self, ctx):
        if self.vc is not None and self.is_paused:
            self.vc.resume()
            self.is_paused = False
            await ctx.send("Resumed")
        else:
            await ctx.send("Aready playing a queue.")

    @commands.command()
    async def skip(self, ctx):
        if self.vc is not None and (self.vc.is_playing() or self.is_paused):
            self.vc.stop()
            self.is_paused = False
            await ctx.send("Skipped")
        else:
            await ctx.send("Play something first.")

    @commands.command()
    async def empty(self, ctx):
        self.search_queue = []
        await ctx.send("Queue emptied")

    @commands.command()
    async def show(self, ctx):
        if not self.search_queue:
            await ctx.send("Queue is empty")
            return
        await ctx.send("Queue:\n")
        message = ""
        for i, search in enumerate(self.search_queue):
            message += f'{i+1}. "{search}"\n'
        await ctx.send(message)


def setup(client):
    playable = music(client)
    client.add_cog(playable)
    return playable
