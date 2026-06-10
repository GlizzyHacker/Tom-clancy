import asyncio

from discord.ext import commands
import discord
import constants
import encrypt

async def encrypt_command_callback(interaction: discord.Interaction, message: str):
    if interaction.user.id == constants.TARGET_USER_ID:
        await interaction.response.send_message("Ezt csak RNcS tagok használhatják.")
        return
    
    await interaction.response.send_message("Yes king", ephemeral=True)

    words = message.split()
    encrypted_words = []
    for word in words:
        encrypted_words.append(encrypt.encrypt(word))

    webhook = await interaction.channel.create_webhook(name=interaction.user.display_name, avatar=await interaction.user.display_avatar.read())
    message = await webhook.send(
        " ".join(encrypted_words),
        wait=True  # For some reason if this line is not here message variable is NoneType, so I can't delete it
    )
    await webhook.delete()
        
async def decrypt_command_callback(interaction: discord.Interaction, message: discord.Message):
    if interaction.user.id == constants.TARGET_USER_ID:
        await interaction.response.send_message("Ezt csak RNcS tagok használhatják.")
        return
    await interaction.response.defer(ephemeral=True)
    if message.webhook_id == None:
        await interaction.followup.send("Ezt nem így kell használni dummy", ephemeral=True)
        return
    
    words = message.content.split()
    decrypted_words = []
    for word in words:
        decrypted_words.append(encrypt.decrypt(word))
    await interaction.followup.send(" ".join(decrypted_words), ephemeral=True)

class Encrypted(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.decryption_context_menu = discord.app_commands.ContextMenu(
            name="Decrypt",
            callback=decrypt_command_callback
        )
        self.encryption_command = discord.app_commands.Command(
            name="encrypt",
            description="Encrypts the message in a way that only RNcS clan members can decrypt it.",
            callback=encrypt_command_callback
        )
        self.bot.tree.add_command(self.decryption_context_menu)
        self.bot.tree.add_command(self.encryption_command)