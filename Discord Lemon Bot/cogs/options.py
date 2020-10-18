import discord
import random
import tenorpy
import wolframalpha
from discord.ext import commands
from discord.ext.commands import BucketType

tenor = tenorpy.Tenor()

class options(commands.Cog):

    def __init__(self, client):
        self.client = client
    
# ASK COMMAND (Takes the prompt, and sends it to the Wolfram API. Sends the answer to the channel.)

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def ask(self, ctx, *, question):
        client = wolframalpha.Client('4KG5LE-J9QU6LY2JR')
        res = client.query(question)
        answer = next(res.results).text
        embed = discord.Embed(title="Answer", description="Answer to the question", color=ctx.author.color)
        embed.add_field(name="Q:", value=question, inline=False)
        embed.add_field(name="A:", value=answer, inline=True)
        await ctx.send(embed=embed)

# EIGHTBALL COMMAND (Takes a question, and returns a random response from the 8ball file.)

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def eightball(self, ctx, *, question):
        with open('./bot_resources/8ball.txt', 'r') as eightball_lines:
            eightball_lines_list = [line.strip('\n') for line in eightball_lines]
        embed=discord.Embed(title="8 Ball ", color=0x00b3ff)
        embed.add_field(name="Question:", value=question, inline=False)
        embed.add_field(name="Answer", value=random.choice(eightball_lines_list), inline=True)
        await ctx.send(embed=embed)
     
# ROLL COMMAND (Returns a random dice roll. Has default maximum of 6, but can be changed if written after)
     
    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def roll(self, ctx, maximum=6):
        try:
            maximum = int(maximum)
        except ValueError:
            await ctx.send('Please enter a number for the maximum.')
            
        if maximum < 1:
            await ctx.send('Please enter a maximum number higher than 1.')
        else:
            await ctx.send(f'You rolled a {random.randint(1, maximum)}!')
           
# COINFLIP COMMAND (Returns heads or tails) 

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def coinflip(self, ctx):
        flip = random.randint(1, 2)
        if flip == 1:
            await ctx.send('You flipped heads.')
        else:
            await ctx.send('You flipped tails.')
            
# FACT COMMAND (Returns a random fact from the facts file.)
            
    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def fact(self, ctx):
        with open('./bot_resources/facts.txt', 'r') as facts_file:
            facts = facts_file.readlines()
        await ctx.send(random.choice(facts))
        
# SEARCH COMMAND (searches a gif from tenor api, and returns it)

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def search(self, ctx, choice):
        await ctx.send(tenor.random(str(choice)))

# POLL COMMAND (Creates a poll)

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def poll(self, ctx, *, message):
        await ctx.message.delete()
        embed=discord.Embed(color=ctx.author.color)
        embed.add_field(name="Poll:", value=message, inline=True)
        embed.set_footer(text=ctx.author.name)
        bot_message = await ctx.send(embed=embed)
        await bot_message.add_reaction('👍')
        await bot_message.add_reaction('👎')

# MEMBERCOUNT COMMAND (Returns the number of members in the guild)

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def membercount(self, ctx):
        count = len(ctx.guild.members)
        await ctx.send(f'{ctx.guild.name} currently has {count} members.')

# CHOOSE COMMAND (Duh)

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def choose(self, ctx, *, choices):
        choices_list = choices.split(',')
        await ctx.send(random.choice(choices_list))

# INVITE COMMAND (Sends invite link for the bot)

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def invite(self, ctx):
        await ctx.send('You can invite me to servers using: https://discord.com/api/oauth2/authorize?client_id=750193712088350790&permissions=523328&scope=bot')

# MISC COMMANDS (other stuff)

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def amanda(self, ctx):
        amanda_id = '<@529490561137115157>'
        await ctx.send(amanda_id + ', you have been summoned')
        await ctx.send(tenor.random('jungkook'))
        await ctx.send(tenor.random('han jisung'))
        
    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def ananna(self, ctx):
        ananna_id = '<@529154044179120131>'
        await ctx.send(ananna_id + ', you have been summoned')
        await ctx.send(tenor.random('jungkook'))
        await ctx.send(tenor.random('felix'))
        
    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def hans(self, ctx):
        hans_id = '<@306937268768210944>'
        image = random.choice(['daniel', 'dieter', 'nol', 'nol2', 'nol3', 'dieter2'])
        await ctx.send(hans_id + ', you have been summoned')
        await ctx.send(file=discord.File(f'./bot_resources/{image}.jpg'))
        image = random.choice(['daniel', 'dieter', 'nol', 'nol2', 'nol3', 'dieter2'])
        await ctx.send(file=discord.File(f'./bot_resources/{image}.jpg'))


def setup(client):
    client.add_cog(options(client))

