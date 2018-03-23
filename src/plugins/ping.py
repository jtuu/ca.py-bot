import re

trigger = re.compile("!ping")

async def action(bot, msg):
    await bot.send_message(msg.channel, "pong")
