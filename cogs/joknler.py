from discord.ext import commands
import constants
import random

JONKLER_GIF = "https://tenor.com/view/joker369-gif-10911555085276863842"

class Jonkler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != constants.TARGET_USER_ID:
            return

        if random.random() < 0.1:
            await message.reply(JONKLER_GIF)