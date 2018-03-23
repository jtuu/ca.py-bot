import discord
import asyncio
import re

class Bot(discord.Client):
    def __init__(self, config):
        discord.Client.__init__(self)
        self.__config = config
        self.__triggers = [] # tuple(RE trigger, lambda Message m: void)[]

    def run(self):
        super(Bot, self).run(self.__config.get("token"))

    def Trigger(self, regexp):
        def register_trigger(fn):
            trigger = (re.compile(regexp), fn)
            self.__triggers.append(trigger)
            return fn
        return register_trigger

    async def on_ready(self):
        print("Logged in as " + self.user.name)

    async def on_message(self, msg):
        for trigger in self.__triggers:
            pattern = trigger[0]
            action = trigger[1]
            if pattern.search(msg.clean_content):
                await action(msg)
