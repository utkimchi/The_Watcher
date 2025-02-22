# https://stackoverflow.com/questions/53528168/how-do-i-use-cogs-with-discord-py
import discord
import os
from dotenv import load_dotenv
import cogs.LetterBox_Utils as lu
from discord.ext import commands
from discord import app_commands
import asyncio
import logging
import logging.handlers

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
        

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

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

