import logging
import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer

import constants

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.updateServerStatus.start()

    def cog_unload(self):
        self.updateServerStatus.cancel()

    @tasks.loop(minutes=5)
    async def updateServerStatus(self):
        try:
            server = await JavaServer.async_lookup(constants.MC_SERVER_ADDRESS)
            stats = await server.async_status()
            
            await self.bot.change_presence(activity=discord.Game(f"Minecraft\n{stats.players.online} balfasszal itt: {constants.MC_SERVER_ADDRESS}"))
        except TimeoutError:
            await self.bot.change_presence(status=None, activity=None)
        except Exception as e:
            logging.getLogger("discord").warning(msg="Failed to query Minecraft server", exc_info= e)