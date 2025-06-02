import socket
import discord
from discord.ext import commands, tasks

server_address = "84.0.203.129:25565"

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.updateServerStatus.start()

    def cog_unload(self):
        self.updateServerStatus.cancel()

    @tasks.loop(minutes=10)
    async def updateServerStatus(self):
        if ping(server_address):
            await self.bot.change_presence(activity=discord.Game("Minecraft szerver fut"))
        else:
            await self.bot.change_presence(status=None, activity=None)

def ping(host):
    ip = host.split(":")[0]
    port = host.split(":")[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)                                 
    result = sock.connect_ex((ip, int(port)))
    isOpen = result == 0
    sock.close()
    return isOpen


if __name__ == "__main__":
    print(ping("84.0.203.129:25565"))