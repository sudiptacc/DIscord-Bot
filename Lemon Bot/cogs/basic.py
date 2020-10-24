'''
Imports from external packages
'''
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
    async def help(self, ctx, help=None):
        if help == None:
            embed = discord.Embed(title="Help Menu", description="Use the ' . ' prefix when typing the commands",
                                color=ctx.author.color)
            embed.add_field(name="Basic Commands", value="*ping, help, about*", inline=False)
            embed.add_field(name="Useful/Fun Commands", value="*ask, eightball, roll, fact, search, poll, membercount, choose, invite, quote, avatar, suggest*", inline=False)
            embed.add_field(name="Economy Commands", value="*daily, stats, give, level, inventory, shop, sell, buy, leaderboard, prestige*", inline=False)
            embed.add_field(name="Game Commands", value="*trivia, guess, blackjack, unscramble, challenge, fish, memory*", inline=True)
            await ctx.send(embed=embed)
        else:
            commands = {
                "ping": "Displays the connection between the bot and the server.",
                "help": "Displays the help menu, shows all commands available.",
                "about": "Displays information about the bot.",
                "ask": "Displays an answer to a question. example: `.ask define trouble`",
                "eightball": "Displays a random response to any prompt. example: `.eightball should I do homework?`",
                "roll": "Displays the result of a dice roll. You can set a maximum. example: `.roll 200`",
                "fact": "Displays a random fact.",
                "search": "Searches a random gif from tenor about the query. example: `.search bananas`",
                "poll": "Displays a poll about a prompt with reactions. example: `.poll this is a test`",
                "membercount": "Displays the number of members in the current server.",
                "choose": "Displays a random choice from a list of options (seperated by commas). example: `.choose fruits, vegetables`",
                "invite": "Displays the invite link for the bot to join other servers.",
                "quote": "Displays a random quote using a random set of words.",
                "avatar": "Displays the avatar of the person, or of another person if specified. example: `.avatar @binay#8032`",
                "suggest": "Suggest or report a feature/bug to the creator of the bot. example: `.suggest this is a test!`",
                "daily": "Gives a $1000 bonus. Can only be used every 24 hours.",
                "stats": "Displays the balance, multiplier, level, and prestige of the player, or a player specified. This command should also be used by people who are just starting out. example: `.stats @binay#8032`",
                "give": "Give the mentioned person a specific amount of money. example: `.give @binay#8032 1000`",
                "level": "Level up. You cannot level up if you are already max level or do not have enough to level up.",
                "inventory": "Displays the inventory of the player or of someone specified. example: `.inventory @binay#8032`",
                "shop": "Displays the items that can be bought and their prices.",
                "sell": "Sell an item from your inventory. The item must be in your inventory. example: `.sell fishing rod`",
                "buy": "Buy an item from the shop. The item gets added to your inventory. example: `.buy fishing rod`",
                "leaderboard": "Displays the leaderboard for the current server. People are ranked based on their balance.",
                "prestige": "Used to prestige. You will need MAX (100) level in order to prestige. Prestiging will reset all of your stats, and add 1 to your base multiplier everytime you prestige.",
                "trivia": "Returns a random question that you can respond to with 'True' or 'False' to earn a prize. The prize IS affected by multipliers.",
                "guess": "Guess a number from 0 to 25, and earn a prize. The prize IS affected by multipliers.",
                "blackjack": "Hit or stand based on the cards you can see. You will need to bet an amount, which you will lose or make back double of. The prize IS NOT affected by multipliers. example: `.blackjack 100`",
                "unscramble": "Unscramble a word that is given to you, and earn a prize. The prize IS affected by multipliers.",
                "challenge": "Challenge a random person to a wager. You/they will either lose the bet, or make double. The prize IS NOT affected by multipliers.",
                "fish": "Catch a fish within 3 seconds of it appearing to win a prize. The prize is affected by your fishing rod, so a better fishing rod will yield better prizes.",
                "memory": "Remember a sequence of words, and type them out (separated by commas) in the order they were shown. The prize IS affected by multipliers."
            }
            embed=discord.Embed(title='Command Help', color = ctx.author.color)
            embed.add_field(name=help.upper(), value=commands[help.lower()], inline=False)
            await ctx.send(embed=embed)
            
        
# ABOUT COMMAND

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def about(self, ctx):
        embed = discord.Embed(title="About this bot", description="information about this bot", color=ctx.author.color)
        embed.add_field(name="Creator", value="binay#8032", inline=False)
        embed.add_field(name="Created", value="10/4/2020", inline=False)
        embed.add_field(name="Purpose", value="idk", inline=False)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(basic(client))
