from discord.ext import commands
import re

class Segg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if re.search("mi *van", message.content.lower()):
            await message.reply("segged kíván\nhttps://cdn.discordapp.com/attachments/1251283088634286183/1378816865798852718/received_615057554184112.jpg?ex=68468c85&is=68453b05&hm=9612b044d3b967e03181fb929349c65827b6a120ba0640a11b7f03cd757ba432&")

        if re.search("mi *lesz", message.content.lower()):
            await message.reply("még jobban kilesz\nhttps://cdn.discordapp.com/attachments/1251283088634286183/1378816866067419186/received_561463979848307.jpg?ex=68468c86&is=68453b06&hm=f5c361496bb2618dbeaf6bac5d6a55969f4e5b6336ab156d36ee262cee7ec8b4&")

        if re.search("segged *k[ií] *v[aá]n", message.content.lower()):
            await message.reply("orrom szám benne van 😋")