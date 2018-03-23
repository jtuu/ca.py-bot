import re

trigger = re.compile("^!capybot")

text = "ca.py-bot made by esc: https://github.com/jtuu/ca.py-bot"

async def action(bot, msg):
    await bot.send_message(msg.channel, text)