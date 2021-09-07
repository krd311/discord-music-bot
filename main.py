import discord
import music
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv('.env')

cogs = [music]
client = commands.Bot(command_prefix=".", intents = discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

print("RUNNING")

client.run(os.getenv('BOT_TOKEN'))


