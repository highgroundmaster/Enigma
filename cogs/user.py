import discord
import random
from discord.ext import commands

class User(commands.Cog):

    def __init__(self, client):
        self.client = client


    #commands

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')


    @commands.command()
    async def tellme(self, ctx, *, question):
        responses=['Absolutely',
                   'Answer Unclear Ask Later',
                   'Cannot Foretell Now',
                   'Yes of course'
                   'Chances do not seem Good',
                   'Ask me if I care'
                   'Very doubtful'
                   'The chances of the Sun rising from the West is more',
                   'Reply hazy, try again later',
                   'Now that is a tricky one',
                   'Nope!',
                   'I will pray for you']

        await ctx.send(f'Question: {question}\n Answer: {random.choice(responses)}')


    @commands.command()
    async def greet(self, ctx):
        greetings=['A fresh start will put you on your way.',
                    'A golden egg of opportunity falls into your lap this month.',
                    'A good time to finish up old tasks.',
                    'A lifetime of happiness lies ahead of you.',
                    'A pleasant surprise is waiting for you.',
                    'Accept something that you cannot change, and you will feel better.',
                    'Change is happening in your life, so go with the flow!',
                    'Distance yourself from the vain.',
                    'Expect much of yourself and little of others.'
                    ]

        await ctx.send(f'Hello there! \n I would like to say that: {random.choice(greetings)}')


    @commands.command()
    async def random_tag(self, ctx):
        tags=['Killer Miller : David Miller',
                'Hitman : Rohit Sharma',
                'Thala : MS Dhoni',
                'Mr.360 : AB Deviliers',
                'The Run Machine : Virat Kohli',
                'Gabbar : Shikhar Dhawan',
                'Warner you are warned : David Warner'
                'Russell Muscle : Andre Russell']

        await ctx.send(f' {random.choice(tags)}')



def setup(client):
    client.add_cog(User(client))
