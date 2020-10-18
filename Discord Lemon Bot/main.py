import os
import json
import discord
import keep_alive
from discord.ext import commands

def get_prefix(client, message):
    with open('./jsons/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())
client.remove_command('help')

# Gives a guild a default prefix when the bot joins it

@client.event
async def on_guild_join(guild):
    with open('./jsons/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('./jsons/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('./jsons/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('./jsons/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    
@client.command()
async def changeprefix(ctx, prefix):
    with open('./jsons/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('./jsons/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send(f'Changed guild prefix to: "{prefix}"')

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
    await ctx.author.send('```Current extensions:```')
    for cog in os.listdir('./cogs'):
        await ctx.author.send(f'```{cog}```')

# The mechanic for finding cogs

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# Loop that keeps the bot up and running

keep_alive.keep_alive()

# Starts up the bot

client.run('TOKEN')
