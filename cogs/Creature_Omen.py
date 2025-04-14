from time import sleep as zzz
import random
import os
from os.path import join
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import typing
import discord
from discord.app_commands import Choice
from discord.ext import commands
from utils import LinkSelect,SelectView
import pandas as pd


class creatureOmen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bp = Path(__file__).parent
        self.species_path= join(bp, "Data/Species.csv")
        self.omen_path = join(bp, "Data/Omens.csv")
        self.species_options = pd.read_csv(self.species_path)
        self.omen_options = pd.read_csv(self.omen_path)

    @commands.command()
    async def omen(self, ctx):
        genus = ''
        species = ''
        for i in range(1,4):
            genus = genus + (self.species_options.at[random.randint(0,9),f"Genus{i}"])
        for i in range(1,4):
            species = species + (self.species_options.loc[random.randint(0,9),f"Species{i}"])

        omen1 = self.omen_options.loc[random.randint(0,9),f"Omen{1}"]
        omen2 = self.omen_options.loc[random.randint(0,9),f"Omen{2}"]
        omen3 = self.omen_options.loc[random.randint(0,9),f"Omen{3}"]
        omen4 = self.omen_options.loc[random.randint(0,9),f"Omen{4}"]

        final_message = f"The {genus} {species} states: If {omen1} then {omen2}! Hurry! You must {omen3}! If you do not {omen3}, {omen4} things will occur!"
        await ctx.send(final_message)


async def setup(bot):
    await bot.add_cog(creatureOmen(bot))
