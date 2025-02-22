from discord.ext import commands
from discord import app_commands, Interaction

class MyCog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @app_commands.command(name='test_command')
    async def test_command_method(self, ctx: Interaction, param1: str = None, param2: str = None):
        if param1 is None:
            param1 = ctx.channel_id  # set default value
        if param2 is None:
            await ctx.send(f'param2 missing!')
            return
        await ctx.send(f'Called with parameters param1: "{param1}" and param2: "{param2}"')


async def setup(client):
    await client.add_cog(MyCog(client))