import random
import asyncio
import discord
import economy_utils as econ
from discord.ext import commands
from discord.ext.commands import BucketType
from pytrivia import Type, Trivia

class game(commands.Cog):

    def __init__(self, client):
        self.client = client

# TRIVIA GAME 

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def trivia(self, ctx):
        prize = random.randint(150, 300)
        my_api = Trivia(True)
        data = my_api.request(1, type_= Type.True_False)
        question = data['results'][0]['question']
        difficulty = data['results'][0]['difficulty']
        category = data['results'][0]['category']
        correct_answer = data['results'][0]['correct_answer']

        embed=discord.Embed(title="Trivia", color=ctx.author.color)
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="Difficulty", value=difficulty.title(), inline=True)
        embed.add_field(name="Category", value=category, inline=True)
        await ctx.send(embed=embed)

        answer = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=20.0)

        if answer.content == None:
            await ctx.send(f'You timed out! The correct answer was `{correct_answer}`')
        elif answer.content.title() == correct_answer:
            await ctx.send(f'You were right! You have won `${prize * econ.get_multiplier(ctx.author.id)}!`')
            econ.deposit(ctx.author.id, prize * econ.get_multiplier(ctx.author.id))
        else:
            await ctx.send(f'You were wrong! The correct answer was `{correct_answer}`!')



# GUESSING GAME 

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def guess(self, ctx):
        secret_number = random.randint(1, 25)
        guesses = 0
        prize = random.randint(100, 250)
        await ctx.send('I\'m thinking of a number... you have 5 tries to guess it!')
        
        while guesses < 5:
            response = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10.0)
            if response == None:
                await ctx.send(f'You timed out! the secret number was {secret_number}')
            elif int(response.content) < secret_number:
                guesses += 1
                await ctx.send(f'Nope! The number is bigger. You have {5 - guesses} guesses remaining.')
            elif int(response.content) > secret_number:
                guesses += 1
                await ctx.send(f'Nope! The number is smaller. You have {5 - guesses} guesses remaining.')
            else:
                await ctx.send(f'Correct! You guessed the number {secret_number} in {guesses} guesses! You earned ${round(prize * econ.get_multiplier(ctx.author.id), 2)}')
                econ.deposit(ctx.author.id, (prize * econ.get_multiplier(ctx.author.id)))
        if guesses == 5:
            await ctx.send(f'You failed! The correct number was {secret_number}!')

# BLACKJACK GAME

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def blackjack(self, ctx, bet: int):
        if bet > econ.get_balance(ctx.author.id):
            await ctx.send('You can\'t bet that! you\'re broke lmao')
            return
        elif bet > 500000:
            await ctx.send('That\'s too much! It is over the maximum amount you can bet. (`$500000`)')
            return
        hits = 0
        prize = bet * 2         
        dealer_deck = [random.randint(1, 10) for card in range(0, 3)]
        player_deck = [random.randint(1, 7) for card in range(0, 3)]
        dealer_msg = await ctx.send(f'Dealer hand: `{dealer_deck[0]}, ?, ?`')
        player_msg = await ctx.send(f'Your hand: `{player_deck[0]}, {player_deck[1]}, ?`')

        while True:
            await ctx.send('Hit or stand?')
            dealer_deck_string = ", ".join(str(card) for card in dealer_deck)
            player_deck_string = ", ".join(str(card) for card in player_deck)
            response = await self.client.wait_for('message', check=lambda message: message.author.id == ctx.author.id, timeout=20.0)
            if response.content.lower() == 'hit':
                hits += 1
                player_deck.append(random.randint(1, 10))
                await player_msg.edit(content=f'Your hand: `{player_deck[0]}, {player_deck[1]}, ?{", ?" * hits}`')
            elif response.content.lower() == 'stand':
                if sum(dealer_deck) < sum(player_deck):
                    if sum(player_deck) <= 21:
                        await ctx.send(f'You won `${prize}`! Your hand: `{sum(player_deck)}` Dealer hand: `{sum(dealer_deck)}`')
                        await dealer_msg.edit(content=f'Dealer hand: `{dealer_deck_string}`')
                        await player_msg.edit(content=f'Player Hand: `{player_deck_string}`')
                        econ.deposit(ctx.author.id, prize)
                        break
                    else:
                        await ctx.send(f'You lost! Your hand: `{sum(player_deck)}` Dealer hand: `{sum(dealer_deck)}`')
                        await dealer_msg.edit(content=f'Dealer hand: `{dealer_deck_string}`')
                        await player_msg.edit(content=f'Player Hand: `{player_deck_string}`')
                        econ.withdraw(ctx.author.id, bet)
                        break
                elif sum(dealer_deck) > sum(player_deck):
                    if sum(dealer_deck) <= 21:
                        await ctx.send(f'You lost! Your hand: `{sum(player_deck)}` Dealer hand: `{sum(dealer_deck)}`')
                        await dealer_msg.edit(content=f'Dealer hand: `{dealer_deck_string}`')
                        await player_msg.edit(content=f'Player Hand: `{player_deck_string}`')
                        econ.withdraw(ctx.author.id, bet)
                        break
                    else:
                        await ctx.send(f'You won `${prize}`! Your hand: `{sum(player_deck)}` Dealer hand: `{sum(dealer_deck)}`')
                        await dealer_msg.edit(content=f'Dealer hand: `{dealer_deck_string}`')
                        await player_msg.edit(content=f'Player Hand: `{player_deck_string}`')
                        econ.deposit(ctx.author.id, prize)
                        break
                else:
                    await ctx.send(f'You tied, so you get your money back! Your hand: {sum(player_deck)} Dealer hand: {sum(dealer_deck)}')
                    await dealer_msg.edit(content=f'Dealer hand: `{dealer_deck_string}`')
                    await player_msg.edit(content=f'Player Hand: `{player_deck_string}`')
                    break       

# UNSCRAMBLE GAME

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def unscramble(self, ctx):
        tries = 0
        prize = random.randint(150, 300) * econ.get_multiplier(ctx.author.id)
        with open('./bot_resources/words.txt', 'r') as f:
            words = f.readlines()
            words = [word.strip('\n') for word in words]
            word_original = random.choice(words)
            if "'" in word_original:
                word_original = random.choice(words)
            word = list(word_original)
            random.shuffle(word)
            scrambled = ''.join(word)

        await ctx.send(f'Unscramble this: `{scrambled}` You have 5 tries.')
        while tries < 5:
            response = await self.client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
            if response.content.lower() == word_original:
                await ctx.send(f'You got it! The word was `{word_original}`! You have won `${prize}`')
                econ.deposit(ctx.author.id, prize)
                return
            else:
                tries += 1
                await ctx.send(f'Nope! You have {5 - tries} more tries left.')
        if tries >= 5:
            await ctx.send(f'Nope! The word was {word_original}')

# CHALLENGE GAME

    @commands.command()
    @commands.cooldown(1, 20, BucketType.user)
    async def challenge(self, ctx, challenged: discord.User, bet: int):
        if econ.get_balance(ctx.author.id) < bet or econ.get_balance(challenged.id) < bet:
            await ctx.send('Either you or the challenged person do not have enough.')
        else:
            prize = bet * 2
            await ctx.send(f'{challenged.mention} do you wish to go with this coinflip?')
            response = await self.client.wait_for('message', check=lambda message: message.author.id == challenged.id, timeout=30.0)
            if response.content.lower() == 'yes':
                flip = random.randint(1, 2)
                if flip == 1:
                    await ctx.send(f'{ctx.author.mention} has won the coinflip against {challenged.mention}, and won `${bet * 2}`!')
                    econ.withdraw(challenged.id, bet)
                    econ.deposit(ctx.author.id, prize)
                    return
                else:
                    await ctx.send(f'{ctx.author.mention} has lost the coinflip against {challenged.mention}!')
                    econ.withdraw(ctx.author.id, bet)
                    econ.deposit(challenged.id, prize)
                    return
            else:
                await ctx.send('Coinflip cancelled!')
                return

# FISHING GAME (TODO)
# Have to buy a normal fishing rod: $1000 (goes in inventory)
# Regular multiplier does not stack on fishing
# $250 - $4999 (80%) 5000-10000 (20%) reward
# You can fish up a different rods from fishing (10% - 2.5x) (5% 4x) (1.25% 5x) (0.75% 10x)
# 60s cooldown
# (?) React to edited message within 5 seconds to catch. 

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def fish(self, ctx):
        if 'fishing rod' in econ.get_inventory(ctx.author.id) or 'normal fishing rod' in econ.get_inventory(ctx.author.id):
            if 'shredder' in econ.get_inventory(ctx.author.id):
                multiplier = 100
            elif 'rod of legends' in econ.get_inventory(ctx.author.id):
                multiplier = 50   
            elif 'rod of champions' in econ.get_inventory(ctx.author.id):
                multiplier = 10
            elif 'challenging rod' in econ.get_inventory(ctx.author.id):
                multiplier = 5
            else:
                multiplier = 1
            prize = 0
            cash_percentage = random.randint(1, 100)
            if cash_percentage < 81:
                prize = random.randint(250, 4999) * multiplier
            else:
                prize = random.randint(5000, 10000) * multiplier
            bot_msg = await ctx.send(':ocean::ocean::ocean::ocean::ocean::ocean:      (Type \'catch\' to catch the fish!)')
            await asyncio.sleep(random.randint(1, 10))
            await bot_msg.edit(content=':ocean::fish::ocean::fish::ocean::ocean:     (Type \'catch\' to catch to fish!)')
            try:
                await self.client.wait_for('message', check=lambda message: message.author.id == ctx.author.id, timeout=3.0)    
            except asyncio.TimeoutError:
                await ctx.send('You didn\'t catch the fish in time!')
            else:
                await ctx.send(f'You have caught a fish that is worth `${prize}`!')
                econ.deposit(ctx.author.id, prize)
                return
        else:
            await ctx.send('You do not have a fishing rod! Please buy a fishing rod from the shop. If you have sold one, make sure not to sell it as you will need it.')


def setup(client):
    client.add_cog(game(client))
            