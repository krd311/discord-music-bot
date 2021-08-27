import discord
from discord.ext import commands
import music

cogs = [music]
client = commands.Bot(command_prefix=".", intents = discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

print("RUNNING")

client.run("ODgwNjU4NTU1MjA2Nzg3MDcz.YShfMQ.UNRuUqNfqZkZ86W3irtFqpCyI2U")


