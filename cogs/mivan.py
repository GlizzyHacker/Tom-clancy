from discord.ext import commands
import re

class Mivan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if re.search("mi *van", message.content.lower()):
            await message.reply("segged kíván\nhttps://cdn.discordapp.com/attachments/1251283088634286183/1378816866067419186/received_561463979848307.jpg?ex=68429806&is=68414686&hm=9d1e25d8e5e216e577e613a52788bf91060b8fe63c1eb09262741a36d681add4&")