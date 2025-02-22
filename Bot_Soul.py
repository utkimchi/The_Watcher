# https://stackoverflow.com/questions/53528168/how-do-i-use-cogs-with-discord-py
import discord
import os
from dotenv import load_dotenv
import cogs.LetterBox_Utils as lu
from discord.ext import commands
from typing import Literal, Optional
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
        print("Bot Up")
        

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

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

@bot.command()
@commands.is_owner()
async def reload(ctx):
    for file in os.listdir(f'./cogs'):
        if file.endswith('.py'):
            print(f"Reloading {file}")
            await bot.reload_extension(f'cogs.{file[:-3]}')
    print(f"Reloaded")

@bot.command()
@commands.is_owner()
async def scoms(ctx):
    for c in bot.commands:
        print(c.name)

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

