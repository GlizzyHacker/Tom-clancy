import discord
from discord.ext import commands, tasks
import insult
import ping
import os
from dotenv import load_dotenv

TOKEN = os.getenv("DISCORD_API_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Variable to store the target username
target_user_id = 423773373152231424 # Ganajdácsi
reaction_user_id = 393797195197054990 # Bálint
reaction_id = 1314709458202529883 # Vincze ásít emoji

spam_counter = 0

@bot.tree.command(
    name="insult",
    description="Insults the given user, gaydacsi-style."
)
async def insult_command(interaction, target: discord.Member, length:int = 2):
    await interaction.response.defer()
    generated = insult.generate_insult(length,target.id==target_user_id)
    await interaction.followup.send(f"{target.mention} {generated}")

@bot.event
async def on_ready():
    await bot.add_cog(ping.Ping(bot))
    await bot.tree.sync()
    print(f"We have logged in as {bot.user}")


@bot.event
async def on_message(message):
    global reaction_user_id
    global reaction_id
    global target_user_id
    global spam_counter

    if message.author == bot.user:
        return

    if (target_user_id and message.channel.id == 1302703027840352309 and message.author.id == target_user_id) or (target_user_id and message.channel.id == 1311805189623386216 and message.author.id == 231705462100328458):
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
    elif reaction_user_id and message.author.id == reaction_user_id:
        for emoji in message.guild.emojis:
            if emoji.id == reaction_id:
                await message.add_reaction(emoji)

    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    if target_user_id and member.id == target_user_id and after and after.channel.id == 1326920421764890695:
        await member.move_to(None)
        
if __name__ == "__main__":
    bot.run(TOKEN)
