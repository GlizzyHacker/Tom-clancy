from discord.ext import commands
import discord
import constants
import random
import asyncio
import words

async def asked_command_callback(interaction, message: discord.Message):
    await interaction.response.send_message("Askedség kiszámítása...")

    if message.author.id != constants.TARGET_USER_ID and random.random() < 0.5:
        asked = True
    else:
        asked = False

    await asyncio.sleep(10)
    try:
        await message.reply(words.generate_response(asked))
    except discord.HTTPException:
        await interaction.followup.send("Leszarom")

class Asked(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.asked_context_menu = discord.app_commands.ContextMenu(
            name="Asked",
            callback=asked_command_callback
        )
        self.bot.tree.add_command(self.asked_context_menu)