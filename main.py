import discord
from discord.ext import commands
import music, playlist
from database import utils

TOKEN = "ODk0ODA1NTM1MjY0NzM5MzQ5.YVvWmA.8m2QQ_rvN1tq0S7wdG4VEkDjvzI"
prefix = "&"
client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

# cogs = [music, playlist]
# for i, c in enumerate(cogs):
#     c.setup(client)

# Setup
playable = music.setup(client)
playlist.setup(client, playable)

database = "database/euclidean.db"
utils.connection.initiate(database)


@client.command
async def help(ctx):
    docs = f"""Euclidean: Music Bot\n
    Prefix: {prefix}\n"""
    music_docs = {
        "connect": "connect to a voice channel",
        "disconnect": "disconnect from a voice channel",
        "play": "play song from youtube",
        "skip": "skip the current song",
        "pause": "pause the current song",
        "resume": "resume the current song",
        "empty": "empty the queue of songs",
        "show": "show the queue of songs",
    }

    for i, key in enumerate(music_docs):
        docs += f"{i+1}. {key} - {music_docs[key]}\n"
    await ctx.send(docs)


client.run(TOKEN)
