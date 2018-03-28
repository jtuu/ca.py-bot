import re

trigger = re.compile("^!help")
keywords = ["help"]

match_pattern = re.compile(r"^!help\s*(.*)")

async def action(bot, msg):
    """**!help** __command__
    Display help for __command__.
    """
    match = match_pattern.match(msg.clean_content)
    if match:
        query = match.groups()[0]
        if query:
            plugin = bot.find_plugin_by_keyword(query)
            if plugin and hasattr(plugin, "action") and plugin.action.__doc__:
                await bot.send_message(msg.channel, plugin.action.__doc__, escape_formatting=False)
            else:
                await bot.send_message(msg.channel, "No help entry found for %s" % query)
        else:
            await bot.send_message(msg.channel, action.__doc__, escape_formatting=False)
