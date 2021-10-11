import discord
from discord.ext import commands
import music, playlist
from database import utils
from dotenv import load_dotenv
import os

prefix = "&"
client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

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


load_dotenv(".env")
client.run(os.getenv("TOKEN"))
