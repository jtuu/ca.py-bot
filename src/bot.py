import discord
import asyncio
import os
import re
from .module_loader import ModuleLoader
from .utils import discord_escape, levenshtein_distance

def is_well_formed_plugin(plugin):
    return hasattr(plugin, "trigger") and isinstance(plugin.trigger, re._pattern_type) and hasattr(plugin, "action") and callable(plugin.action)

class Bot(discord.Client):
    def __init__(self, config):
        discord.Client.__init__(self)
        self.__config = config
        plugin_dir_path = os.path.abspath(os.path.dirname(__file__) + "/plugins")
        self.__plugin_loader = ModuleLoader(module_dir_path=plugin_dir_path, verbose=True)

    def run(self):
        loop = asyncio.get_event_loop()
        self.__plugin_loader.run(loop)
        loop.run_until_complete(asyncio.wait([
            asyncio.ensure_future(super(Bot, self).start(self.__config.get("token"))),
        ]))

    @asyncio.coroutine
    def send_message(self, destination, content=None, *, tts=False, embed=None, escape_formatting=True):
        if escape_formatting:
            if content:
                content = discord_escape(content)
            
            if embed:
                if embed.title is not discord.Embed.Empty:
                    embed.title = discord_escape(embed.title)
                if embed.description is not discord.Embed.Empty:
                    embed.description = discord_escape(embed.description)
                if embed.fields is not discord.Embed.Empty and len(embed.fields) > 0:
                    for field in embed.fields:
                        field.name = discord_escape(field.name)
                        field.value = discord_escape(field.value)

        return super().send_message(destination, content=content, tts=tts, embed=embed)

    async def on_ready(self):
        print("Logged in as " + self.user.name)

    def is_message_triggering(self, msg):
        for plugin in self.__plugin_loader.get_modules():
            if is_well_formed_plugin(plugin) and plugin.trigger.search(msg.clean_content):
                return True
        return False

    def find_plugin_by_keyword(self, search_kw):
        for plugin in self.__plugin_loader.get_modules():
            if hasattr(plugin, "keywords"):
                for kw in plugin.keywords:
                    if levenshtein_distance(kw, search_kw) < 2:
                        return plugin
        return None

    async def on_message(self, msg):
        if not msg.author.bot:    
            for plugin in self.__plugin_loader.get_modules():
                if is_well_formed_plugin(plugin):
                    if plugin.trigger.search(msg.clean_content):
                        await plugin.action(self, msg)
                else:
                    print("Plugin %s is not well formed" % plugin.__file__)
                    self.__plugin_loader.unload_module(plugin.__file__)
