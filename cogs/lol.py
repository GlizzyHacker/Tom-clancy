from discord.ext import commands
import discord
import constants

lol_players = [constants.REACTION_USER_ID ,619855173459771402, 1252523980288692297]

class Lol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.purge_command = discord.app_commands.Command(
            name="purge",
            description="Deletes lol threads.",
            callback=self.purge_command
        )
        self.bot.tree.add_command(self.purge_command)

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
            for ass in lol_players + [message.author.id]:
                try:
                    await thread.add_user(await self.bot.fetch_user(ass))
                except:
                    pass
            await thread.send("<:shame:1312885404684386484>")

    async def purge_command(self, interaction):
        if interaction.user == self.bot.user:
            return

        if interaction.user.id in lol_players:
            await interaction.response.send_message("Csináld magad lol")
            return

        await interaction.response.defer()
        deleted = 0
        for thread in interaction.channel.threads:
            if thread.name.startswith("lol"):
                await thread.delete()
                deleted += 1
        print(f"{deleted} lol threads deleted")
        await interaction.followup.send(f"{deleted} lol thread törölve")