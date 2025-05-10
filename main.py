import asyncio
import random
from datetime import datetime, timezone, timedelta
import discord
from discord.ext import commands
import words
import ping
import os
import handler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_API_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Setup constants
TARGET_USER_ID = 423773373152231424 # Ganajdácsi
REACTION_USER_ID = 393797195197054990 # Bálint
REACTION_EMOJI_ID = 1314709458202529883 # Vincze ásít emoji
NEM_DUMBY_CHAT_ID = 1302703027840352309

spam_counter = 0

@bot.tree.command(
    name="insult",
    description="Insults the given user, gaydacsi-style."
)
async def insult_command(interaction, target: discord.Member, length:int = 2):
    """
    Insults the given user, gaydacsi-style.
    :param interaction: discord.Interaction object
    :param target: user to insult
    :param length: length of insult, defaults to 2
    """
    await interaction.response.defer()
    generated = words.generate_insult(length, target.id == TARGET_USER_ID)
    await interaction.followup.send(f"{target.mention} {generated}")

@bot.tree.command(
    name="symouse",
    description="Deletes given number of messages or messages after given date (YYYY-MM-DD HH:MM) from ganajdacsi."
)
async def symouse_command(interaction, amount : int = 1, after : str = None):
    """
        Deletes given number of messages or messages after given date (YYYY-MM-DD HH:MM) from ganajdacsi.
        :param interaction: discord.Interaction object
        :param amount: amount of messages to delete, defaults to 1
        :param after: date (YYYY-MM-DD HH:MM) after all messages will be deleted, defaults to None, if given param amount is ignored
    """

    if interaction.channel.id != NEM_DUMBY_CHAT_ID:
        await interaction.response.send_message("Itt ezt nem használhatod dumby")
        return

    channel = interaction.channel
    # interaction.response.send_message() doesn't work if it takes more than 3 seconds
    await interaction.response.defer()

    messages = []
    msg_contents = []
    # Deleting very old or too many messages may take a while or just not work idk
    async for msg in channel.history(limit=None):
        if msg.author.id == TARGET_USER_ID:
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

@bot.tree.command(
    name="react",
    description="Periodically reacts to target user's messages"
)
async def react_command(interaction, emoji:str, target: discord.Member, amount:int = 1):
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
    async for msg in interaction.channel.history(limit=None):
        if msg.author == target and len(msg.reactions) < reaction_limit:
            bot_already_reacted = False
            for reaction in msg.reactions:
                if str(reaction.emoji) == emoji:
                    async for user in reaction.users():
                        if user.id == bot.user.id:
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

@bot.tree.context_menu(
    name="Asked"
)
async def asked_command(interaction, message: discord.Message):
    await interaction.response.send_message("Askedség kiszámítása...")

    if message.author.id != TARGET_USER_ID and random.random() < 0.5:
        asked = True
    else:
        asked = False

    await asyncio.sleep(10)
    try:
        await message.reply(words.generate_response(asked))
    except discord.HTTPException:
        await interaction.followup.send("Leszarom")

@bot.tree.context_menu(
    name="Ghostping"
)
async def ghostping_command(interaction, target: discord.Member):
    if interaction.user.id == TARGET_USER_ID:
        await interaction.response.send_message("Ezt faszopok nem használhatják <:kispajtas:1314704200092881018>")
        return
    await interaction.response.send_message("Yes king",ephemeral=True)

    ghost = interaction.user
    ghostwebhook = await interaction.channel.create_webhook(name="Ghost")
    message = await ghostwebhook.send(
        target.mention,
        username=ghost.display_name,
        avatar_url=ghost.display_avatar.url,
        wait=True #For some reason if this line is not here message variable is NoneType, so I can't delete it
    )
    await asyncio.sleep(0.5)
    await message.delete()
    await ghostwebhook.delete()

@bot.event
async def on_ready():
    await bot.add_cog(ping.Ping(bot))
    await bot.tree.sync()
    print(f"We have logged in as {bot.user}")


@bot.event
async def on_message(message):
    global REACTION_USER_ID
    global REACTION_EMOJI_ID
    global TARGET_USER_ID
    global spam_counter

    if message.author == bot.user:
        return

    if (TARGET_USER_ID and message.channel.id == 1302703027840352309 and message.author.id == TARGET_USER_ID) or (TARGET_USER_ID and message.channel.id == 1311805189623386216 and message.author.id == 231705462100328458):
        print(f"Deleted message: {message.content} from specimen: {message.author}")
        await message.delete()
        if spam_counter > 5:
            await message.channel.send(f"{message.author.mention} Ahelyett, hogy itt spamelsz inkább menj r6ozni dummy!")
            spam_counter = 0
        else:
            spawnpeek = "<:spawnpeeeek:1254451054095892694>"
            hogykepzeljuk = "<:hogy_kepzeljuk_ezt:1251288927197724693>"
            await message.channel.send(f"{message.author.mention} Erre a csatornára dummy fucker cuntok nem írhatnak! {spawnpeek} {hogykepzeljuk}:")
            spam_counter += 1
        return  # Stop further processing for this message
    elif REACTION_USER_ID and message.author.id == REACTION_USER_ID:
        for emoji in message.guild.emojis:
            if emoji.id == REACTION_EMOJI_ID:
                await message.add_reaction(emoji)

    if "faszopo" in message.content.lower():
        try:
            await message.reply(stickers=[discord.Object(id=1347686845064020071)])
        except discord.Forbidden:
            await message.reply("https://cdn.discordapp.com/attachments/1251283088634286183/1342594424168779879/image.png?ex=68035f3e&is=68020dbe&hm=9e4b3a7e8036ad83e415112759e116ffe88e404ab67d8c6829641fba2a15fdae&")

    if message.author.id == TARGET_USER_ID:
        if "nemértem" in ("".join((message.content.lower()).split(" "))) or "nemertem" in ("".join((message.content.lower()).split(" "))):
            await message.reply("nem meglepő")

    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    if TARGET_USER_ID and member.id == TARGET_USER_ID and after and after.channel.id == 1326920421764890695:
        await member.move_to(None)
        
@bot.event
async def on_typing(channel, user, when):
    await asyncio.sleep(15)
    if not (await did_send_message_after(channel, user, when)):
        await channel.send(f"{user.mention} le se írd")

async def did_send_message_after(channel, user, after):
    async for message in channel.history(after=after):
        if message.author == user:
            return True
    return False

if __name__ == "__main__":
    handler.setup_handler()

    bot.run(TOKEN)

