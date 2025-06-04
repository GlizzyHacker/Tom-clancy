from discord.ext import commands
import discord
import re

class Faszopo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if re.search("fas+z[oóöő]p[oóöő]", message.content.lower()):
            try:
                await message.reply(stickers=[discord.Object(id=1347686845064020071)])
            except discord.Forbidden:
                await message.reply(
                    "https://cdn.discordapp.com/attachments/1251283088634286183/1342594424168779879/image.png?ex=68035f3e&is=68020dbe&hm=9e4b3a7e8036ad83e415112759e116ffe88e404ab67d8c6829641fba2a15fdae&"
                )