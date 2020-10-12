import discord
from discord.ext import commands, tasks


class startup(commands.Cog):

    def __init__(self, client):
        self.client = client

    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game('with your feelings'))

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print('!!!!BOT IS READY!!!!')

    #Catches any wrong inputs, and returns either error message.

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please input the correct arguments')
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send('Invalid command, please input a valid command')


def setup(client):
    client.add_cog(startup(client))
