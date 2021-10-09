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
        self.lock = asyncio.Lock()

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

    def reset(self):
        self.vc = None
        self.is_paused = False
        del self.song_queue
        self.song_queue = deque()

    @commands.command()
    async def disconnect(self, ctx):
        print("DC")
        if ctx.voice_client is None:
            await ctx.send("Not connected to be disconected u noob!")
            return
        self.reset()
        await ctx.voice_client.disconnect()

    async def play_next(self, ctx):
        if not self.song_queue:
            if self.vc is not None:
                await self.disconnect(ctx)
            return

        print(self.song_queue)

        song = self.song_queue[0]
        self.song_queue.popleft()

        await ctx.send(f"Playing \"{song['title']}\" - {song['channel']}")
        self.vc.play(
            song["source"],
            after=lambda err: asyncio.run_coroutine_threadsafe(
                self.play_next(ctx), self.client.loop
            ),
        )

    def ytsearch(self, search):
        song = {}
        info = self.ydl.extract_info(f"ytsearch:{search}", download=False)["entries"][0]
        song["url"] = info["formats"][0]["url"]
        song["title"] = info["title"]
        song["channel"] = info["channel"]
        return song

    async def playSong(self, ctx, song):
        if ctx.voice_client is None and not await self.connect(ctx):
            return

        print(song)

        source = await discord.FFmpegOpusAudio.from_probe(
            executable="C:/ffmpeg/bin/ffmpeg.exe",
            source=song["url"],
            **self.OPTIONS["FFMPEG"],
        )
        song = {"source": source, "title": song["title"], "channel": song["channel"]}
        self.song_queue.append(song)

        async with self.lock:
            if not self.vc.is_playing() and not self.is_paused:
                print("play next!!!!!!!!!")
                await self.play_next(ctx)
            else:
                await ctx.send(
                    f"Added to queue \"{song['title']}\" - {song['channel']}"
                )

    @commands.command()
    async def play(self, ctx, *args):
        search = " ".join(args)
        song = self.ytsearch(search)
        await self.playSong(ctx, song)

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
