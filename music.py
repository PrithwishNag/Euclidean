import discord
from discord.ext import commands
import youtube_dl
import time


class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.vc = None
        self.is_paused = 0
        self.OPTIONS = {
            "FFMPEG": {
                "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                "options": "-b:a 48k -vn",
            },
            "YDL": {"format": "worstaudio", "noplaylist": "True"},
        }
        self.ydl = youtube_dl.YoutubeDL(self.OPTIONS["YDL"])

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
        return 1

    @commands.command()
    async def disconnect(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("Not connected to be disconected u noob!")
            return
        await ctx.voice_client.disconnect()

    # @commands.command()
    # async def search(self, ctx, *args):
    #     search = " ".join(args)
    #     with youtube_dl.YoutubeDL(self.OPTIONS["YDL"]) as ydl:
    #         songs = ydl.extract_info(f"ytsearch:{search}", download=False)["entries"]
    #         print(len(songs))
    #         for i, s in enumerate(songs):
    #             info = s
    #             print(info)
    #             await ctx.send(f"{i}. \"{info['track']}\", \"{info['artist']}\"")
    #     pass

    # def play_next():

    @commands.command()
    async def play(self, ctx, *args):
        if ctx.voice_client is None and not await self.connect(ctx):
            return

        search = " ".join(args)

        # ctx.voice_client.stop()

        self.vc = ctx.voice_client

        info = self.ydl.extract_info(f"ytsearch:{search}", download=False)["entries"][0]
        print("INFO: ", info)
        url = info["formats"][0]["url"]
        source = await discord.FFmpegOpusAudio.from_probe(
            executable="C:/ffmpeg/bin/ffmpeg.exe",
            source=url,
            **self.OPTIONS["FFMPEG"],
        )
        self.vc.play(source, after=lambda x: print("done: ", x))
        await ctx.send(f"Playing \"{info['title']}\", \"{info['artist']}\"")

    @commands.command()
    async def pause(self, ctx):
        if self.vc is not None and self.vc.is_playing:
            self.vc.pause()
            self.is_paused = 1
            await ctx.send("Paused")

    @commands.command()
    async def resume(self, ctx):
        print(self.vc)
        print(self.vc.is_playing)
        if self.vc is not None and self.is_paused:
            self.vc.resume()
            self.is_paused = 0
            await ctx.send("Resumed")

    @commands.command()
    async def skip(self, ctx):
        if self.vc is not None and self.vc.is_playing:
            self.vc.stop()
            await ctx.send("Skipped")


def setup(client):
    client.add_cog(music(client))
