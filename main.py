import os
import discord
from discord.ext import commands
from database import utils
from dotenv import load_dotenv
import music, playlist
from server import server

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
server()
client.run(os.getenv("TOKEN"))