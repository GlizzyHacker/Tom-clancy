from discord.ext import commands
import discord
import constants
from datetime import datetime, timezone, timedelta

async def symouse_command_callback(interaction, amount : int = 1, after : str = None):
    """
        Deletes given number of messages or messages after given date (YYYY-MM-DD HH:MM) from ganajdacsi.
        :param interaction: discord.Interaction object
        :param amount: amount of messages to delete, defaults to 1
        :param after: date (YYYY-MM-DD HH:MM) after all messages will be deleted, defaults to None, if given param amount is ignored
    """

    if interaction.channel.id != constants.NEM_DUMBY_CHAT_ID:
        await interaction.response.send_message("Itt ezt nem használhatod dumby")
        return

    channel = interaction.channel
    # interaction.response.send_message() doesn't work if it takes more than 3 seconds
    await interaction.response.defer()

    messages = []
    msg_contents = []
    # Deleting very old or too many messages may take a while or just not work idk
    async for msg in channel.history(limit=None):
        if msg.author.id == constants.TARGET_USER_ID:
            # If both parameters are given it ignores the amount
            if after is not None:
                try:
                    # If time is not given set it to midnight
                    if len(after) == 10:
                        after += " 00:00"
                    date = datetime.strptime(after, "%Y-%m-%d %H:%M").replace(tzinfo=timezone(timedelta(hours=1)))  # Offset-aware time utc+1 timezone
                except ValueError:
                    await interaction.followup.send("Rossz dátum formátum dumbass thrower")
                    return
                if msg.created_at > date:
                    messages.append(msg)
                    msg_contents.append(msg.content)
            else:
                messages.append(msg)
                msg_contents.append(msg.content)
                if len(messages) >= amount:
                    break

    if not messages:
        await interaction.followup.send("Ilyen üzenet nem LÉtezik")
        return

    # If some messages are not under 14 days old bulk delete doesn't work, so delete them one by one
    try:
        await channel.delete_messages(messages)
    except Exception as e:
        print(e)
        for msg in messages:
            await msg.delete()

    await interaction.followup.send(f"{len(messages)} üzenet törölve")
    print(f"{len(messages)} messages deleted:\n{msg_contents}")

class Symouse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.symouse_command = discord.app_commands.Command(
            name="symouse",
            description="Deletes given number of messages or messages after given date (YYYY-MM-DD HH:MM) from ganajdacsi.",
            callback=symouse_command_callback
        )
        self.bot.tree.add_command(self.symouse_command)