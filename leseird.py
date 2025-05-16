import asyncio
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone

LE_SE_IRD_TYPING_TRESHOLD = 3
LE_SE_IRD_DELAY = 20

class UserTypingState:
    def __init__(self, user, channel):
        self.user = user
        self.channel = channel

        self.typing_times = []
        self.counter_done = False
        self.responded = False

    async def typed(self, when):
        self.typing_times.append(when)
        if len(self.typing_times) == 1:
            await self.start_counter()
        elif len(self.typing_times) >= LE_SE_IRD_TYPING_TRESHOLD:
            await self.try_respond()

    async def start_counter(self):
        await asyncio.sleep(LE_SE_IRD_DELAY)
        self.counter_done = True
        await self.try_respond()
    
    async def try_respond(self):
            if len(self.typing_times) >= LE_SE_IRD_TYPING_TRESHOLD and self.counter_done and not self.responded:
                await self.channel.send(f"{self.user.mention} le se írd")
                self.responded = True
    
    def __eq__(self, value):
        if len(value) == 2:
            return self.user.id == value[0] and self.channel == value[1]

class Leseird(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #ID : NUMBER OF TYPING EVENTS
        self.type_states = []

        self.cleanup_typing_states.start()

    def cog_unload(self):
        self.cleanup_typing_states.cancel()
        
    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        found = False
        for state in self.type_states:
            if (user.id, channel) == state:
                type_state = state
                found = True
        if (not found):
            type_state = UserTypingState(user, channel)
            self.type_states.append(type_state)
        await type_state.typed(when)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        for state in self.type_states:
            if (message.author.id, message.channel) == state:
                self.type_states.remove((message.author.id, message.channel))

    @tasks.loop(minutes=10)
    async def cleanup_typing_states(self):
        stay = []
        for type_state in self.type_states:
            if len(type_state.typing_times) != 0 and type_state.typing_times[-1] > datetime.now(timezone.utc) - timedelta(minutes=5):
                stay.append(type_state)        
        self.type_states = stay
