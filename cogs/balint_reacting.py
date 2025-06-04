from discord.ext import commands
import constants

class BalintReacting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != constants.REACTION_USER_ID:
            return

        for emoji in message.guild.emojis:
            if emoji.id == constants.REACTION_EMOJI_ID:
                await message.add_reaction(emoji)