import json
import discord
import random
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
        with open('./jsons/playerstats.json', 'r') as f:
            playerstats = json.load(f)
        with open('./jsons/playerdates.json', 'r') as f:
            playerdates = json.load(f)
        if str(ctx.author.id) not in playerdates:
            playerdates[str(ctx.author.id)] = datetime.datetime.now().isoformat()

            embed=discord.Embed(title="Daily Bonus!", description="Collected your daily bonuse!", color=ctx.author.color)
            embed.set_author(name=ctx.author.id)
            embed.set_thumbnail(url="https://assets.stickpng.com/images/580b585b2edbce24c47b288d.png")
            embed.add_field(name="You have collected `$1000`!", value='yay!', inline=False)
            await ctx.send(embed=embed)
            playerstats[str(ctx.author.id)]['balance'] += 1000
        else:
            time_from_playerdates = datetime.datetime.fromisoformat(playerdates[str(ctx.author.id)])
            time_difference = datetime.datetime.now() - time_from_playerdates
            print(time_difference)

            if time_difference.days >= 1:
                embed=discord.Embed(title="Daily Bonus!", description="Collected your daily bonuse!", color=ctx.author.color)
                embed.set_author(name=ctx.author.name)
                embed.set_thumbnail(url="https://assets.stickpng.com/images/580b585b2edbce24c47b288d.png")
                embed.add_field(name="You have collected `$1000`!", value='yay!', inline=False)
                await ctx.send(embed=embed)
                playerstats[str(ctx.author.id)]['balance'] += 1000
                playerdates[str(ctx.author.id)] = datetime.datetime.now().isoformat()
            else:
                await ctx.send('Your daily bonus is not ready yet!')

        with open('./jsons/playerdates.json', 'w') as f:
            json.dump(playerdates, f, indent=4)
        with open('./jsons/playerstats.json', 'w') as f:
            json.dump(playerstats, f, indent=4)

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
                playerstats[str(user.id)]['inventory'] = []
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
                if econ.get_balance(ctx.author.id) <= amount:
                    await ctx.send('You are broke! You can\'t send money lmao')
                else:
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
    async def prestige(self, ctx, amount=None):
        if amount == None:
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
        elif amount.lower() == 'max':
            while True:
                await ctx.send(f'Are you sure you want to prestige to the highest level you can? Type "yes" to confirm.')
                confirmation = await self.client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
                if confirmation.content.lower() == 'yes':
                    while True:
                        if econ.prestige_can_happen(ctx.author.id):
                            econ.prestige_action(ctx.author.id)
                        else:
                            await ctx.send(f'You are done prestiging! You have reached prestige `{econ.get_prestige(ctx.author.id)}`!')
                            return
                else:
                    await ctx.send('Prestige cancelled')
        else:
            await ctx.send('Please enter a valid argument.')
            

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def multiplier(self, ctx):
        await ctx.send(f'Your current multiplier is `{econ.get_multiplier(ctx.author.id)}x`!')

# STEAL

    @commands.command()
    @commands.cooldown(1, 3600, BucketType.user)
    async def steal(self, ctx, user: discord.User):
        amount = random.randint(250, 5000)
        chance = random.randint(1, 10)
        extra_chance = random.randint(1, 1000)
        if extra_chance == 1000:
            amount = 100000
        if amount > econ.get_balance(ctx.author.id) or amount > econ.get_balance(user.id):
            await ctx.send('Either you are the other person do not have enough to pay for fines, or enough to be robbed of.')
        elif chance == 5:
            await ctx.send(f'You have stolen `${amount}` from {user.mention}!')
            econ.withdraw(user.id, amount)
            econ.deposit(ctx.author.id, amount)
            return
        else:
            await ctx.send(f'You were caught! You are required to pay `${amount}` for compensation.')
            econ.withdraw(ctx.author.id, amount)
            econ.deposit(user.id, amount)
            return

# INVENTORY TODO

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def inventory(self, ctx):
        with open('./jsons/playerstats.json', 'r') as f:
            playerstats = json.load(f)
        embed=discord.Embed(title=f"Inventory of {ctx.author.name}", color=ctx.author.color)
        print(playerstats[str(ctx.author.id)]['inventory'])
        inventory_list = ', '.join(playerstats[str(ctx.author.id)]['inventory'])
        embed.add_field(name="Items", value=f'`{inventory_list}`', inline=True)
        await ctx.send(embed=embed)

# # SHOP, BUYING, SELLING, AND OTHER TODO

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def shop(self, ctx):
        embed=discord.Embed(title="Shop", description="Buy your items here!")
        embed.set_author(name=ctx.author.name)
        embed.set_thumbnail(url="https://i.pinimg.com/originals/70/40/5f/70405f68ba3a416658543134010b9ee5.png")
        embed.add_field(name="Boosters", value="TO BE ADDED\nTO BE ADDED\nTO BE ADDED", inline=False)
        embed.add_field(name="Items", value="Normal Fishing Rod: `$1000`\nChallenging Rod: `$50000`\nRod of Champions: `$250000`\n Rod of Legends: `$1000000`\nShredder: `$2500000` ", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def buy(self, ctx, *, item):

        products = {
            "normal fishing rod": 1000,
            "fishing rod": 1000,
            "challenging rod": 50000,
            "rod of champions": 250000,
            "rod of legends": 1000000,
            "shredder": 2500000
                    }

        with open('./jsons/playerstats.json', 'r') as f:
            playerstats = json.load(f)

        if item.lower() in products:
            if products[item.lower()] > econ.get_balance(ctx.author.id):
                await ctx.send('You cannot buy that, you are broke lmao')
                return
            await ctx.send(f'Bought a `{item}` for `${products[item.lower()]}`!')
            amount = products[item.lower()]
            print(amount)
            playerstats[str(ctx.author.id)]['balance'] -= amount
            playerstats[str(ctx.author.id)]['inventory'].append(item.lower())
            with open('./jsons/playerstats.json', 'w') as f:
                json.dump(playerstats, f, indent=4)
        else:
            await ctx.send(f'{item} not found in the shop!')

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def sell(self, ctx, *, item):

        products = {
            "normal fishing rod": 1000,
            "fishing rod": 1000,
            "challenging rod": 50000,
            "rod of champions": 250000,
            "rod of legends": 1000000,
            "shredder": 2500000
                    }

        with open('./jsons/playerstats.json', 'r') as f:
            playerstats = json.load(f)

        if item.lower() in products:
            if item.lower() not in playerstats[str(ctx.author.id)]['inventory']:
                await ctx.send('You do not have this in your inventory! Shoo!')
                return
            else:
                await ctx.send(f'Sold a `{item}` for `${products[item.lower()]}`!')
                amount = products[item.lower()]
                print(amount)
                playerstats[str(ctx.author.id)]['balance'] += amount
                playerstats[str(ctx.author.id)]['inventory'].remove(item.lower())
                with open('./jsons/playerstats.json', 'w') as f:
                    json.dump(playerstats, f, indent=4)
                
        else:
            await ctx.send(f'{item} could not be sold!')


def setup(client):
    client.add_cog(economy(client))