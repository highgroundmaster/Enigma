import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('APL is ready to work.')

@client.event
async def on_member_join(member):
    print(f'Yayy {member} has joined the server')

@client.event
async def on_member_remove(member):
    print(f'Goodbye {member}')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')



client.run('NzYwMDU2NDE2OTQ5MzcwOTA5.X3Gfsg.lGMgtSiIzO_XSSTp-AVV5qe6y_A')
