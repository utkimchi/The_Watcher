# https://stackoverflow.com/questions/53528168/how-do-i-use-cogs-with-discord-py
import discord
import os
from dotenv import load_dotenv
import cogs.LetterBox_Utils as lu
from discord.ext import commands
from discord import app_commands
import asyncio

class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(intents=discord.Intents.all(), command_prefix='!')

    async def setup_hook(self):
        for file in os.listdir(f'./cogs'):
            if file.endswith('.py'):
                print(file)
                await self.load_extension(f'cogs.{file[:-3]}')
        synced = await self.tree.sync()
        print(f"Synced {len(synced)}command(s).")
        


load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
disc_id = os.getenv("DISC_ID")
bot = MyBot()

@bot.tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    await interaction.response.defer()
    if interaction.user.id == int(disc_id):
        print("Syncing")
        await bot.tree.sync()
        await interaction.followup.send('Command tree synced.')
    else:
        await interaction.followup.send('You must be the owner to use this command!')

@bot.event
async def main():
    async with bot:
        await bot.start(bot_token, reconnect=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print("Script Ending") # Error handling
        raise(error)





# @bot.tree.command(name="addmovie",description='Adds a movie to the Kinosphere')
# async def addmovie(ctx, movie_title: str):
#     """Adds movie to List"""
#     message = lu.addMovie(movie_title)
#     await ctx.send(message)


# @bot.tree.command()
# async def add(ctx, left: int, right: int):
#     """Adds two numbers together."""
#     await ctx.send(left + right)


# @bot.tree.command()
# async def roll(ctx, dice: str):
#     """Rolls a dice in NdN format."""
#     try:
#         rolls, limit = map(int, dice.split('d'))
#     except Exception:
#         await ctx.send('Format has to be in NdN!')
#         return

#     result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
#     await ctx.send(result)


# @bot.tree.command(name="choose",description='For when you wanna settle the score some other way')
# async def choose(ctx, choices):
#     """Chooses between multiple choices."""
#     await ctx.send(random.choice(choices))


# @bot.tree.command()
# async def repeat(ctx, times: int, content: str):
#     """Repeats a message multiple times."""
#     for i in range(times):
#         await ctx.send(content)


# @bot.tree.command()
# async def joined(ctx, member: discord.Member):
#     """Says when a member joined."""
#     await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

# @bot.group()
# async def cool(ctx):
#     """Says if a user is cool.

#     In reality this just checks if a subcommand is being invoked.
#     """
#     if ctx.invoked_subcommand is None:
#         await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


# @cool.command(name='bot')
# async def _bot(ctx):
#     """Is the bot cool?"""
#     await ctx.send('Yes, the bot is cool.')
