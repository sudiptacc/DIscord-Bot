import random
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
    @commands.cooldown(1, 30, BucketType.user)
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
    @commands.cooldown(1, 30, BucketType.user)
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
    @commands.cooldown(1, 30, BucketType.user)
    async def blackjack(self, ctx, bet):
        hits = 0
        dealer_deck = [random.randint(1, 10) for card in range(0, 3)]
        player_deck = [random.randint(1, 10) for card in range(0, 3)]
        dealer_msg = await ctx.send(f'Dealer hand: `{dealer_deck[0]}, ?, ?`')
        player_msg = await ctx.send(f'Your hand: `{player_deck[0]}, {player_deck[1]}, ?`')

        while True:
            await ctx.send('Hit or stand?')
            dealer_deck_string = ", ".join(str(card) for card in dealer_deck)
            player_deck_string = ", ".join(str(card) for card in player_deck)
            response = await self.client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
            if response.content.lower() == 'hit':
                hits += 1
                player_deck.append(random.randint(1, 10))
                await player_msg.edit(content=f'Your hand: `{player_deck[0]}, {player_deck[1]}, ?{", ?" * hits}`')
            elif response.content.lower() == 'stand':
                if sum(dealer_deck) < sum(player_deck) and sum(player_deck) <= 21:
                    await ctx.send(f'You won ${round(bet * 2 * econ.get_multiplier(ctx.author.id), 2)}! Your hand: {sum(player_deck)} Dealer hand: {sum(dealer_deck)}')
                    await dealer_msg.edit(content=f'Dealer hand: `{dealer_deck_string}`')
                    await player_msg.edit(content=f'Player Hand: `{player_deck_string}`')
                    econ.deposit(ctx.author.id, bet * 2 * econ.get_multiplier(ctx.author.id))
                    break
                elif sum(dealer_deck) > sum(player_deck) and sum(dealer_deck) <= 21:
                    await ctx.send(f'You lost! Your hand: {sum(player_deck)} Dealer hand: {sum(dealer_deck)}')
                    await dealer_msg.edit(content=f'Dealer hand: `{dealer_deck_string}`')
                    await player_msg.edit(content=f'Player Hand: `{player_deck_string}`')
                    econ.withdraw(ctx.author.id, bet)
                    break  
                elif sum(dealer_deck) < sum(player_deck) and sum(player_deck) > 21:
                    await ctx.send(f'You lost! Your hand: {sum(player_deck)} Dealer hand: {sum(dealer_deck)}')
                    await dealer_msg.edit(content=f'Dealer hand: `{dealer_deck_string}`')
                    await player_msg.edit(content=f'Player Hand: `{player_deck_string}`')
                    econ.withdraw(ctx.author.id, bet)
                    break
                elif sum(dealer_deck) > sum(player_deck) and sum(dealer_deck) > 21:
                    await ctx.send(f'You won ${round(bet * 2 * econ.get_multiplier(ctx.author.id), 2)}! Your hand: {sum(player_deck)} Dealer hand: {sum(dealer_deck)}')
                    await dealer_msg.edit(content=f'Dealer hand: `{dealer_deck_string}`')
                    await player_msg.edit(content=f'Player Hand: `{player_deck_string}`')
                    econ.deposit(ctx.author.id, bet * 2 * econ.get_multiplier(ctx.author.id))
                    break
                else:
                    await ctx.send(f'You tied, so you get your money back! Your hand: {sum(player_deck)} Dealer hand: {sum(dealer_deck)}')
                    await dealer_msg.edit(content=f'Dealer hand: `{dealer_deck_string}`')
                    await player_msg.edit(content=f'Player Hand: `{player_deck_string}`')
                    break
       
                     
            
def setup(client):
    client.add_cog(game(client))
            