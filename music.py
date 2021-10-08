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
                "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                "options": "-b:a 48k -vn",
            },
            "YDL": {"format": "worstaudio", "noplaylist": "True"},
        }
        self.ydl = youtube_dl.YoutubeDL(self.OPTIONS["YDL"])
        self.song_queue = deque()

    @commands.command()
    async def connect(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Voice channel join kar re hajjam!")
            return 0
        vc = ctx.author.voice.channel
        if ctx.voice_client is None:
            await vc.connect()
        else:
            await ctx.voice_client.move_to(vc)
        self.vc = ctx.voice_client
        return 1

    @commands.command()
    async def disconnect(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("Not connected to be disconected u noob!")
            return
        await ctx.voice_client.disconnect()

    async def play_next(self, ctx):
        if self.song_queue == []:
            return

        song = self.song_queue[0]
        self.song_queue.popleft()

        await ctx.send(f"Playing \"{song['title']}\" - {song['channel']}")
        self.vc.play(
            song["source"],
            after=lambda err: asyncio.run_coroutine_threadsafe(
                self.play_next(ctx), self.client.loop
            ),
        )

    @commands.command()
    async def play(self, ctx, *args):
        if ctx.voice_client is None and not await self.connect(ctx):
            return

        search = " ".join(args)
        info = self.ydl.extract_info(f"ytsearch:{search}", download=False)["entries"][0]
        url = info["formats"][0]["url"]
        source = await discord.FFmpegOpusAudio.from_probe(
            executable="C:/ffmpeg/bin/ffmpeg.exe",
            source=url,
            **self.OPTIONS["FFMPEG"],
        )
        song = {"source": source, "title": info["title"], "channel": info["channel"]}
        self.song_queue.append(song)

        if not self.vc.is_playing() and not self.is_paused:
            await self.play_next(ctx)
        else:
            await ctx.send(f"Added to queue \"{song['title']}\" - {song['channel']}")

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
            await ctx.send(
                "Play something noob!"
            )  # Queue is empty (Nothing is playing)

    @commands.command()
    async def resume(self, ctx):
        if self.vc is not None and self.is_paused:
            self.vc.resume()
            self.is_paused = False
            await ctx.send("Resumed")
        else:
            await ctx.send("Aready playing, you blind?")

    @commands.command()
    async def skip(self, ctx):
        if self.vc is not None and (self.vc.is_playing() or self.is_paused):
            self.vc.stop()
            self.is_paused = False
            await ctx.send("Skipped")
        else:
            await ctx.send(
                "Play something noob!"
            )  # Queue is empty (Nothing is playing)

    @commands.command()
    async def empty(self, ctx):
        self.song_queue = []
        await ctx.send("Queue emptied")

    @commands.command()
    async def show(self, ctx):
        if self.song_queue == []:
            await ctx.send("Queue is empty")
            return
        await ctx.send("Queue:\n")
        message = ""
        for i, song in enumerate(self.song_queue):
            message += f"{i+1}. \"{song['title']}\" - {song['channel']}\n"
        await ctx.send(message)


def setup(client):
    playable = music(client)
    client.add_cog(playable)
    return playable
