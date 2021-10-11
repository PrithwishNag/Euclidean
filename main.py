import discord
from discord.ext import commands
import music, playlist
from database import utils
from dotenv import load_dotenv
import os

prefix = "&"
client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all(), help_command=None)

@client.group(invoke_without_command=True)
async def help(ctx):
    await music.music.help(None, ctx, prefix)
    await playlist.playlist.help(None, ctx)

# Setup
playable = music.setup(client)
playlist.setup(client, playable)

# Database
database = "database/euclidean.db"
utils.connection.initiate(database)

# Environment Token and Run
load_dotenv(".env")
client.run(os.getenv("TOKEN"))