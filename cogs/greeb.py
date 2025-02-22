from discord.ext import commands
import discord
from time import sleep as s

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')

    @discord.app_commands.command(name="hello")
    @discord.app_commands.choices(option=[
    discord.app_commands.Choice(name="Kinosphere", value="kinosphere"),
    discord.app_commands.Choice(name="Triple C", value="ccc-ppp")
    ])
    async def hello(self, interaction: discord.Interaction, option: discord.app_commands.Choice[str]):
        await interaction.response.defer()
        msg = f"choice = {option.name}"
        await interaction.followup.send(msg)

async def setup(bot):
    await bot.add_cog(Greetings(bot))