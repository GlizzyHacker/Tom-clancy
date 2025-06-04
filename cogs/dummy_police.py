from discord.ext import commands
import constants

spam_counter = 0
spawnpeek = "<:spawnpeeeek:1254451054095892694>"
hogykepzeljuk = "<:hogy_kepzeljuk_ezt:1251288927197724693>"

class DummyPolice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != constants.NEM_DUMBY_CHAT_ID or message.author.id != constants.TARGET_USER_ID:
            return

        global spam_counter
        global spawnpeek
        global hogykepzeljuk

        print(f"Deleted message: {message.content} from specimen: {message.author}")
        await message.delete()

        if spam_counter > 5:
            await message.channel.send(
                f"{message.author.mention} Ahelyett, hogy itt spamelsz inkább menj r6ozni dummy!")
            spam_counter = 0
        else:
            await message.channel.send(
                f"{message.author.mention} Erre a csatornára dummy fucker cuntok nem írhatnak! {spawnpeek} {hogykepzeljuk}:")
            spam_counter += 1