import discord
from discord.ext import commands
import music

TOKEN = "ODk0ODA1NTM1MjY0NzM5MzQ5.YVvWmA.8m2QQ_rvN1tq0S7wdG4VEkDjvzI"
client = commands.Bot(command_prefix="&", intents=discord.Intents.all())

cogs = [music]
for i, c in enumerate(cogs):
    c.setup(client)


client.run(TOKEN)
