'''
Imports from internal packages
'''
import random
'''
Imports from external packages
'''
import discord
import tenorpy
import wolframalpha
from discord.ext import commands
from discord.ext.commands import BucketType

tenor = tenorpy.Tenor()

class commands(commands.Cog):

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
        with open('./bot_resources/texts/8ball.txt', 'r') as eightball_lines:
            eightball_lines_list = [line.strip('\n') for line in eightball_lines]
        embed=discord.Embed(title="8 Ball ", color=ctx.author.color)
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
            
# FACT COMMAND (Returns a random fact from the facts file.)
            
    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def fact(self, ctx):
        with open('./bot_resources/texts/facts.txt', 'r') as facts_file:
            facts = facts_file.readlines()
            embed=discord.Embed(title="Fact", color=ctx.author.color)
        embed.add_field(name="A random fact...", value=random.choice(facts), inline=False)
        await ctx.send(embed=embed)
        
# SEARCH COMMAND (searches a gif from tenor api, and returns it)

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def search(self, ctx, choice):
        embed=discord.Embed(title="Search", color=ctx.author.color)
        embed.add_field(name="A random gif...", value=f"Result for {choice}", inline=False)
        embed.set_image(url=tenor.random(str(choice)))
        await ctx.send(embed=embed)

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
        count = 0
        for member in ctx.guild.members:
            if not member.bot:
                count += 1
        embed=discord.Embed(title="Members", color=ctx.author.color)
        embed.add_field(name=f"{ctx.guild.name} currently has...", value=f"{count} members!", inline=False)
        await ctx.send(embed=embed)

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
        embed=discord.Embed(title="Invite", color=ctx.author.color)
        embed.add_field(name="You can invite me other servers using:", value="https://discord.com/api/oauth2/authorize?client_id=750193712088350790&permissions=523328&scope=bot", inline=False)
        await ctx.send(embed=embed)

# RANDOM QUOTE COMMAND (Returns a random string of words)

    @commands.command() 
    @commands.cooldown(1, 1, BucketType.user)
    async def quote(self, ctx):
        length = range(0, (random.randint(1, 10)))
        with open('./bot_resources/texts/words.txt') as f:
            words = f.readlines()
            words = [word.strip('\n') for word in words]
            quote_words = [random.choice(words) for _ in length]
            quote = ' '.join(quote_words)
        embed=discord.Embed(title="Quote", color=ctx.author.color)
        embed.add_field(name="Inspirational quote...", value=f"*{quote}*", inline=False)
        embed.set_footer(text="~ Lemon Bot")

        await ctx.send(embed=embed)

# AVATAR COMMAND (Returns an enlargened image of the author)

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def avatar(self, ctx, user: discord.User = None):
        if user == None:
            embed=discord.Embed(title="Avatar", color=ctx.author.color)
            embed.set_author(name=ctx.author.name)
            embed.set_image(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Avatar")
            embed.set_author(name=user.name)
            embed.set_image(url=user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def suggest(self, ctx, *, bug: str):
        with open('./bot_resources/texts/bugs.txt', 'r') as f:
            lines = f.readlines()
        lines.append(f'{bug}\n')
        with open('./bot_resources/texts/bugs.txt', 'w') as f:
            f.writelines(lines)
        await ctx.send('Received your suggestion/report! Thank you!')


# MISC COMMANDS (other stuff)

    def bot_owner(ctx):
        return ctx.author.id == 385929138256740354

    @commands.command()
    @commands.check(bot_owner)
    @commands.cooldown(1, 1, BucketType.user)
    async def say(self, ctx):
        while True:
            message = input('> ')
            if message.lower() == 'stop':
                break
            await ctx.send(message)
            


def setup(client):
    client.add_cog(commands(client))

