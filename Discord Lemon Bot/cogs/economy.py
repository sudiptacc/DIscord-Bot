import json
import discord
import datetime
import economy_utils as econ
from discord.ext import commands
from discord.ext.commands import BucketType

class economy(commands.Cog):

    def __init__(self, client):
        self.client = client

# DAILY COMMAND

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def daily(self, ctx):
        with open('./jsons/playerdates.json', 'r') as f:
            playerdates = json.load(f)
        if str(ctx.author.id) not in playerdates:
            playerdates[str(ctx.author.id)] = datetime.datetime.now().isoformat()
            with open('./jsons/playerdates.json', 'w') as f:
                json.dump(playerdates, f, indent=4)

            embed=discord.Embed(title="Daily Bonus!", description="Collected your daily bonuse!", color=ctx.author.color)
            embed.set_author(name=ctx.author.id)
            embed.set_thumbnail(url="https://assets.stickpng.com/images/580b585b2edbce24c47b288d.png")
            embed.add_field(name="You have collected `$1000`!", value='yay!', inline=False)
            await ctx.send(embed=embed)
            econ.deposit(ctx.author.id, 1000)
        else:
            time_from_playerdates = datetime.datetime.fromisoformat(playerdates[str(ctx.author.id)])
            time_difference = datetime.datetime.now() - time_from_playerdates

            if time_difference.days >= 1:
                embed=discord.Embed(title="Daily Bonus!", description="Collected your daily bonuse!", color=ctx.author.color)
                embed.set_author(name=ctx.author.id)
                embed.set_thumbnail(url="https://assets.stickpng.com/images/580b585b2edbce24c47b288d.png")
                embed.add_field(name="You have collected `$1000`!", inline=False)
                await ctx.send(embed=embed)
                econ.deposit(ctx.author.id, 1000)

                playerdates[str(ctx.author.id)] = datetime.datetime.now().isoformat()
                with open('./jsons/playerdates.json', 'w') as f:
                    json.dump(playerdates, f, indent=4)
            else:
                await ctx.send('Your daily bonus is not ready yet!')


# STATS + OPEN ACCOUNT

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def stats(self, ctx, user: discord.User=None):
        if user == None:
            with open('./jsons/playerstats.json', 'r') as f:
                playerstats = json.load(f)

            if str(ctx.author.id) not in playerstats:
                playerstats[str(ctx.author.id)] = {}
                playerstats[str(ctx.author.id)]['balance'] = 100
                playerstats[str(ctx.author.id)]['multiplier'] = 1
                playerstats[str(ctx.author.id)]['prestige'] = 0
                with open('./jsons/playerstats.json', 'w') as f:
                    json.dump(playerstats, f, indent=4)

            embed=discord.Embed(title=f"Stats of {ctx.author.name}", color=ctx.author.color)
            embed.add_field(name="Balance", value=f'`${round(econ.get_balance(ctx.author.id), 2)}`', inline=True)
            embed.add_field(name="Multiplier", value=f'`{econ.get_multiplier(ctx.author.id)}x`', inline=True)
            embed.add_field(name="Prestige", value=f'`{econ.get_prestige(ctx.author.id)}`', inline=True)
            await ctx.send(embed=embed)
        else:
            with open('./jsons/playerstats.json', 'r') as f:
                playerstats = json.load(f)

            if str(user.id) not in playerstats:
                playerstats[str(user.id)] = {}
                playerstats[str(user.id)]['balance'] = 100
                playerstats[str(user.id)]['multiplier'] = 1
                playerstats[str(user.id)]['prestige'] = 0
                with open('./jsons/playerstats.json', 'w') as f:
                    json.dump(playerstats, f, indent=4)

            embed=discord.Embed(title=f"Stats of {user.name}", color=0x00b3ff)
            embed.add_field(name="Balance", value=f'`${round(econ.get_balance(user.id), 2)}`', inline=True)
            embed.add_field(name="Multiplier", value=f'`{econ.get_multiplier(user.id)}x`', inline=True)
            embed.add_field(name="Prestige", value=f'`{econ.get_prestige(user.id)}`', inline=True)
            await ctx.send(embed=embed)

# TRADING BETWEEN PLAYERS

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def give(self, ctx, receiver: discord.User, amount):
        if float(amount.strip('$')) < 0:
            await ctx.send('Hey! You can\'t steal money!')
        else:
            try:
                amount = round(float(amount.strip('$')), 2)
                econ.withdraw(ctx.author.id, amount)
                econ.deposit(receiver.id, amount)
                await ctx.send(f'You gave {receiver.mention} `${amount}`!')
            except ValueError:
                await ctx.send('Please enter a valid amount!')

# PRESTIGE & MULTIPLIER

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def prestigeinfo(self, ctx):
        await ctx.send(f'You are currently on prestige level `{econ.get_prestige(ctx.author.id)}`!')
    
    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def prestige(self, ctx):
        await ctx.send(f'Are you sure you want to prestige? It will cost you `${round((5 * econ.get_prestige(ctx.author.id)**3)/5)}` Type "yes" to confirm.')
        confirmation = await self.client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
        if confirmation.content.lower() == 'yes':
            if econ.prestige_can_happen(ctx.author.id):
                econ.prestige_action(ctx.author.id)
                await ctx.send(f'You have prestiged! You are now prestige level `{econ.get_prestige(ctx.author.id)}`!')
            else:
                await ctx.send('You cannot prestige. You are either already max prestige, or cannot afford it.')
        else:
            await ctx.send('Prestige cancelled!')
        

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def multiplier(self, ctx):
        await ctx.send(f'Your current multiplier is `{econ.get_multiplier(ctx.author.id)}x`!')

def setup(client):
    client.add_cog(economy(client))