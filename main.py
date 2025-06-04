from discord.ext import commands
from dotenv import load_dotenv
import os
import discord
import log_handler
import cog_handler

load_dotenv()

TOKEN = os.getenv("DISCORD_API_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)
        
@bot.event
async def on_ready():
    await cog_handler.add_all_cogs(bot)
    await bot.tree.sync()
    print(f"We have logged in as {bot.user}")

if __name__ == "__main__":
    log_handler.setup_handler()

    bot.run(TOKEN)

