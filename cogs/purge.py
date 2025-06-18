from discord.ext import commands
import discord
import constants

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or isinstance(message.channel, discord.Thread):
            return

        if "purge this shit" in message.content.lower():
            lol_threads = 0
            for thread in message.channel.threads:
                if thread.name.startswith("lol"):
                    try:
                        thread.delete()
                        await message.reply("Roger Roger")
                    except:
                        pass

