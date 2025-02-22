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
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send("yo")

async def setup(bot):
    await bot.add_cog(Greetings(bot))