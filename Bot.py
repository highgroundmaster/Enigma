import discord
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

client.run('NzYwMDU2NDE2OTQ5MzcwOTA5.X3Gfsg.lGMgtSiIzO_XSSTp-AVV5qe6y_A')
