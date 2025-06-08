from discord.ext import commands
import re

class Egyebkent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if re.search("egy[eé]bk[eé]nt", message.content.lower()):
            await message.reply("Egyébként meg legyünk büszkék 56-ra 🇭🇺 🇭🇺 ❤️")