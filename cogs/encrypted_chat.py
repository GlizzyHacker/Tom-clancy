from discord.ext import commands
import discord
import constants
import encrypt

async def encrypt_command_callback(interaction, message: str):
    if interaction.user.id == constants.TARGET_USER_ID:
        await interaction.response.send_message("Ezt csak RNcS tagok használhatják.")
        return
      
    words = message.split()
    encrypted_words = []
    for word in words:
        encrypted_words.append(encrypt.encrypt(word))
    await interaction.response.send_message(interaction.user.mention + " ezt üzeni: " + " ".join(encrypted_words))
        
async def decrypt_command_callback(interaction: discord.Interaction, message: discord.Message):
    if interaction.user.id == constants.TARGET_USER_ID:
        await interaction.response.send_message("Ezt csak RNcS tagok használhatják.")
        return
    await interaction.response.defer(ephemeral=True)
    if "ezt üzeni:" not in  message.content:
        await interaction.followup.send("Ezt nem így kell használni dummy", ephemeral=True)
        return
    
    words = message.content.split()
    words = words[words.index("üzeni:")+1:]
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