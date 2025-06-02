from discord.ext import commands
import discord
import words
import constants


async def insult_command_callback(interaction, target: discord.Member, length:int = 2):
    """
    Insults the given user, gaydacsi-style.
    :param interaction: discord.Interaction object
    :param target: user to insult
    :param length: length of insult, defaults to 2
    """
    await interaction.response.defer()
    generated = words.generate_insult(length, target.id == constants.TARGET_USER_ID)
    await interaction.followup.send(f"{target.mention} {generated}")

async def insult_command_context_menu(interaction: discord.Interaction, target: discord.Member):
    await insult_command_callback(interaction, target)

class Insult(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.insult_context_menu = discord.app_commands.ContextMenu(
            name="Insult",
            callback=insult_command_context_menu,
        )
        self.bot.tree.add_command(self.insult_context_menu)

        self.insult_command = discord.app_commands.Command(
            name="insult",
            description="Insults the given user, gaydacsi-style.",
            callback=insult_command_callback
        )
        self.bot.tree.add_command(self.insult_command)