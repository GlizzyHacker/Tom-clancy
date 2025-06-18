from discord.ext import commands
import discord
import constants

class Lol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or isinstance(message.channel, discord.Thread):
            return

        if "lol" in message.content.lower():
            lol_threads = 0
            for thread in message.channel.threads:
                if thread.name.startswith("lol"):
                    lol_threads += 1
            thread = await message.channel.create_thread(
                name=f"lol{lol_threads+1}",
            )
            lol_players = [619855173459771402, 1252523980288692297, message.author.id]
            for ass in lol_players:
                try:
                    await thread.add_user(await self.bot.fetch_user(ass))
                except:
                    pass
            await thread.send("<:shame:1312885404684386484>")