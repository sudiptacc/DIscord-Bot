import discord
from discord.ext import commands


class basic(commands.Cog):

    def __init__(self, client):
        self.client = client

#PING COMMAND

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! | {round(self.client.latency * 1000)}ms')

#HELP COMMAND

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Help Menu", description="Use the ' $ ' prefix when typing the commands",
                              color=0x00b3ff)
        embed.add_field(name="Basic Commands", value="ping, help, about", inline=False)
        embed.add_field(name="Useful/Fun Commands", value="ask, eightball, roll, fact, search, coinflip", inline=False)
        embed.add_field(name="Bot Commands (OWNER ONLY)", value="reload, load, unload, extensions", inline=True)
        await ctx.send(embed=embed)

#ABOUT COMMAND

    @commands.command()
    async def about(self, ctx):
        embed = discord.Embed(title="About this bot", description="information about this bot", color=0x00b3ff)
        embed.add_field(name="Creator", value="binay#8032", inline=False)
        embed.add_field(name="Created", value="10/4/2020", inline=False)
        embed.add_field(name="Purpose", value="idk", inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(basic(client))
