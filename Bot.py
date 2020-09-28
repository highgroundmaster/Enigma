import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot is ready.')

client.run('NzYwMDU2NDE2OTQ5MzcwOTA5.X3Gfsg.lGMgtSiIzO_XSSTp-AVV5qe6y_A')
