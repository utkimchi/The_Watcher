import discord 
from discord.ext import commands
import random

def get_random_emoji():
    # Define a range of common emoji Unicode code points
    emoji_range_start = 0x1F600  # Start of the "Emoticons" block
    emoji_range_end = 0x1F64F  # End of the "Emoticons" block
    
    # Generate a random code point within the range
    random_code_point = random.randint(emoji_range_start, emoji_range_end)
    
    # Convert the code point to its hexadecimal representation
    hex_code_point = hex(random_code_point)[2:].upper().zfill(8)
    
    # Return the emoji as a string
    return f"\\U{hex_code_point}"

class LinkSelect(discord.ui.Select):
    def __init__(self,option_dict):
        self.options_dict = {}
        options = []
        for key,val in option_dict.items():
            op = discord.SelectOption(label= key,description=val)
            options.append(op)
            self.options_dict[key] = op
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):
        mess = self.options_dict[self.values[0]]
        print(mess)
        await interaction.response.send_message(mess,ephemeral=True)

class SelectView(discord.ui.View):
    def __init__(self, opts, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(LinkSelect(option_dict=opts))
