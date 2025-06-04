from discord.ext import commands
import asyncio
import discord
import constants

async def ghostping_command_callback(interaction, target: discord.Member):
    if interaction.user.id == constants.TARGET_USER_ID:
        await interaction.response.send_message("Ezt faszopok nem használhatják <:kispajtas:1314704200092881018>")
        return
    await interaction.response.send_message("Yes king", ephemeral=True)

    ghostwebhook = await interaction.channel.create_webhook(name=interaction.user.display_name,
                                                            avatar=await interaction.user.display_avatar.read())
    message = await ghostwebhook.send(
        target.mention,
        wait=True  # For some reason if this line is not here message variable is NoneType, so I can't delete it
    )
    await asyncio.sleep(0.5)
    await message.delete()
    await ghostwebhook.delete()


class GhostPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.ghostping_context_menu = discord.app_commands.ContextMenu(
            name="Ghost ping",
            callback=ghostping_command_callback
        )
        self.bot.tree.add_command(self.ghostping_context_menu)

        self.ghostping_command = discord.app_commands.Command(
            name="ghostping",
            description="Pings target user then deletes ping.",
            callback=ghostping_command_callback
        )
        self.bot.tree.add_command(self.ghostping_command)