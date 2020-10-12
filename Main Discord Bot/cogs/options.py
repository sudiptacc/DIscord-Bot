import os
import discord
import random
import tenorpy
import asyncio
import wolframalpha
from discord.ext import tasks, commands

tenor = tenorpy.Tenor()

class options(commands.Cog):

    def __init__(self, client):
        self.client = client
    
#ASK COMMAND (Takes the prompt, and sends it to the Wolfram API. Sends the answer to the channel.)

    @commands.command()
    async def ask(self, ctx, *, question):
        client = wolframalpha.Client('4KG5LE-J9QU6LY2JR')
        res = client.query(question)
        answer = next(res.results).text
        embed = discord.Embed(title="Answer", description="Answer to the question", color=0x00b3ff)
        embed.add_field(name="Q:", value=question, inline=False)
        embed.add_field(name="A:", value=answer, inline=True)
        await ctx.send(embed=embed)

#EIGHTBALL COMMAND (Takes a question, and returns a random response from the 8ball file.)

    @commands.command()
    async def eightball(self, ctx, *, question):
        with open('C:/Users/toyo7/Desktop/Main Discord Bot/bot_resources/8ball.txt', 'r') as eightball_lines:
            eightball_lines_list = [line.strip('\n') for line in eightball_lines]
        embed=discord.Embed(title="8 Ball ", color=0x00b3ff)
        embed.add_field(name="Question:", value=question, inline=False)
        embed.add_field(name="Answer", value=random.choice(eightball_lines_list), inline=True)
        await ctx.send(embed=embed)
     
#ROLL COMMAND (Returns a random dice roll. Has default maximum of 6, but can be changed if written after)
     
    @commands.command()
    async def roll(self, ctx, maximum=6):
        try:
            maximum = int(maximum)
        except ValueError:
            await ctx.send('Please enter a number for the maximum.')
            
        if maximum < 1:
            await ctx.send('Please enter a maximum number higher than 1.')
        else:
            await ctx.send(f'You rolled a {random.randint(1, maximum)}!')
           
#COINFLIP COMMAND (Returns heads or tails) 

    @commands.command()
    async def coinflip(self, ctx):
        flip = random.randint(1, 2)
        if flip == 1:
            await ctx.send('You flipped heads.')
        else:
            await ctx.send('You flipped tails.')
            
#FACT COMMAND (Returns a random fact from the facts file.)
            
    @commands.command()
    async def fact(self, ctx):
        with open('C:/Users/toyo7/Desktop/Main Discord Bot/bot_resources/facts.txt', 'r') as facts_file:
            facts = facts_file.readlines()
        await ctx.send(random.choice(facts))
        
#SEARCH COMMAND (searches a gif from tenor api, and returns it)

    @commands.command()
    async def search(self, ctx, choice):
        await ctx.send(tenor.random(str(choice)))

#GUESSING GAME (guessing game)

    @commands.command()
    async def guess(self, ctx):
        secret_number = random.randint(1, 50)
        guesses = 0
        await ctx.send('I\'m thinking of a number... you have 5 tries to guess it!')
        
        while guesses < 5:
            response = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
            if int(response.content) < secret_number:
                guesses += 1
                await ctx.send(f'Nope! The number is bigger. You have {5 - guesses} guesses remaining.')
            elif int(response.content) > secret_number:
                guesses += 1
                await ctx.send(f'Nope! The number is smaller. You have {5 - guesses} guesses remaining.')
            else:
                await ctx.send(f'Correct! You guessed the number {secret_number} in {guesses} guesses!')
        if guesses == 5:
            await ctx.send(f'You failed! The correct number was {secret_number}!')
            
#MISC COMMANDS (other stuff)

    @commands.command()
    async def amanda(self, ctx):
        amanda_id = '<@529490561137115157>'
        await ctx.send(amanda_id + 'you have been summoned')
        await ctx.send(tenor.random('jungkook'))
        await ctx.send(tenor.random('han jisung'))
        
    @commands.command()
    async def ananna(self, ctx):
        ananna_id = '<@529154044179120131>'
        await ctx.send(ananna_id + ', you have been summoned')
        await ctx.send(tenor.random('jungkook'))
        
    @commands.command()
    async def hans(self, ctx):
        hans_id = '<@306937268768210944>'
        image = random.choice(['daniel.jpg', 'dieter.jpg', 'nol.jpg'])
        await ctx.send(hans_id + ', you have been summoned')
        await ctx.send(file=discord.File(f'C:/Users/toyo7/Desktop/Main Discord Bot/bot_resources/{image}'))


def setup(client):
    client.add_cog(options(client))

