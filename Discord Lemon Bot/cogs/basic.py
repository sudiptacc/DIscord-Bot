import discord
from discord.ext import commands
from discord.ext.commands import BucketType


class basic(commands.Cog):

    def __init__(self, client):
        self.client = client

# PING COMMAND

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def ping(self, ctx):
        await ctx.send(f'Pong! | {round(self.client.latency * 1000)}ms')

# HELP COMMAND

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def help(self, ctx, command=None):
        if command == None:
            embed = discord.Embed(title="Help Menu", description="Use the ' . ' prefix when typing the commands",
                                color=0x00b3ff)
            embed.add_field(name="Basic Commands", value="ping, help, about", inline=False)
            embed.add_field(name="Useful/Fun Commands", value="ask (query), eightball (question), roll (*maximum), fact, search (query), coinflip", inline=False)
            embed.add_field(name="Economy Commands", value="guess, blackjack (bet), stats, prestige, prestigeinfo, multiplier, give (person, amount), trivia, daily", inline=False)
            embed.add_field(name="Bot Commands (OWNER ONLY)", value="reload, load, unload, extensions", inline=True)
            await ctx.send(embed=embed)
        elif command.lower() == 'ping':
            await ctx.send('Ping: returns the connection between discord and the bot')
        elif command.lower() == 'about':
            await ctx.send('About: returns information about the bot')
        elif command.lower() == 'ask':
            await ctx.send('Ask: returns an answer to a question')
        elif command.lower() == 'eightball':
            await ctx.send('Eightball: returns a random response to a question')
        elif command.lower() == 'roll':
            await ctx.send('Roll: returns a random dice roll. Input number after to increase maximum')
        elif command.lower() == 'fact':
            await ctx.send('Fact: returns a random fact')
        elif command.lower() == 'search':
            await ctx.send('Search: returns a random gif related to the topic sent')
        elif command.lower() == 'coinflip':
            await ctx.send('Coinflip: returns heads or tails')
        else:
            await ctx.send('Guess: starts the guessing game.')

# ABOUT COMMAND

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def about(self, ctx):
        embed = discord.Embed(title="About this bot", description="information about this bot", color=0x00b3ff)
        embed.add_field(name="Creator", value="binay#8032", inline=False)
        embed.add_field(name="Created", value="10/4/2020", inline=False)
        embed.add_field(name="Purpose", value="idk", inline=False)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(basic(client))
