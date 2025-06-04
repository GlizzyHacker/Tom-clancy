from discord.ext import commands
import discord
import asyncio


class React(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.react_command = discord.app_commands.Command(
            name="react",
            description="Periodically reacts to target user's messages.",
            callback=self.react_command_callback
        )
        self.bot.tree.add_command(self.react_command)

    async def react_command_callback(self, interaction, target: discord.Member, emoji: str, amount: int = 1):
        """
        Reacts given emoji to given number of messages from target user
        :param interaction: discord.Interaction object
        :param emoji: emoji to react
        :param target: target user
        :param amount: amount of messages to react, defaults to 1
        """
        await interaction.response.defer(ephemeral=True)

        reaction_limit = 20

        messages = []
        added = 0
        async for msg in interaction.channel.history(limit=100):
            if msg.author == target and len(msg.reactions) < reaction_limit:
                bot_already_reacted = False
                for reaction in msg.reactions:
                    if str(reaction.emoji) == emoji:
                        async for user in reaction.users():
                            if user.id == self.bot.user.id:
                                bot_already_reacted = True
                if not bot_already_reacted:
                    messages.append(msg)
                    added += 1
                    if added >= amount:
                        break

        reacted_count = 0
        progress = await interaction.followup.send(f"reagálva {reacted_count}/{len(messages)} üzenetre")
        for msg in messages:
            if len(msg.reactions) >= reaction_limit:
                continue
            try:
                await msg.add_reaction(emoji)
                reacted_count += 1
                await progress.edit(content=f"reagálva {reacted_count}/{len(messages)} üzenetre")
            except discord.HTTPException:
                await progress.edit(content="Nincs is ilyen emoji dumbass")
                return
            await asyncio.sleep(30)

        await progress.edit(content="Kész")
        print(f"Reacted {emoji} to {reacted_count}/{len(messages)} messages from {target}")