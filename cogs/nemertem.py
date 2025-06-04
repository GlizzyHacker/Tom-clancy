from discord.ext import commands
import constants
import re


class Nemertem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != constants.TARGET_USER_ID:
            return

        if re.search("[ns]em* *[eé]rtem", message.content.lower()):
            await message.reply("Nem meglepő")