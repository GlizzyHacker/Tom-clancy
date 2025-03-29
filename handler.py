import asyncio
import logging
import main

log_channel_id = 1354852366309916776

class DiscordHandler(logging.Handler):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    def emit(self, record):
        try:
            log_entry = self.format(record)
            channel = self.bot.get_channel(log_channel_id)
            async def asyncfunc():
                await channel.send(log_entry)
            asyncio.run(asyncfunc())
        except Exception as e:
            print(f"Error sending log to Discord: {e}")

            
# Set up logging
logger = logging.getLogger('discord_logger')
logger.setLevel(logging.DEBUG)

# Create a custom logging formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
discord_handler = DiscordHandler(main.bot)
discord_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(discord_handler)

if __name__ == "__main__":
    main.bot.run(main.TOKEN,log_handler=discord_handler)