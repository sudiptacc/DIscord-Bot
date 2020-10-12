import os
import discord
from discord.ext import commands, tasks


client = commands.Bot(command_prefix= '.', intents=discord.Intents.all())
client.remove_command('help')

# All of the cog loading and unloading commands, checks if the author is an owner. Also includes a command that lists all cogs, and outputs it to the guild

def bot_owner(ctx):
    return ctx.author.id == 385929138256740354
    
@client.command()
@commands.check(bot_owner)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send('extension loaded')

@client.command()
@commands.check(bot_owner)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send('extension unloaded')

@client.command()
@commands.check(bot_owner)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send('extension reloaded')
    
@client.command()
@commands.check(bot_owner)
async def extensions(ctx):
    await ctx.send('```Current extensions:```')
    for cog in os.listdir('./cogs'):
        await ctx.send(f'```{cog}```')

#The mechanic for finding cogs

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#Starts up the bot

client.run('TOKEN')
