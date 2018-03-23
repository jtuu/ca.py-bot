import re
import random

trigger = re.compile("^!decide")

delim = "or"
match_pattern = re.compile("^!decide\s(?!.*\s" + delim + "\s" + delim + ").+?\s" + delim + "\s(?!.*\s" + delim + ").+")
split_pattern = re.compile("\s+" + delim + "\s+")


async def action(bot, msg):
    msg_text = msg.clean_content
    match = match_pattern.match(msg_text)
    if match:
        split = split_pattern.split(trigger.sub("", msg_text))
        choice = random.choice(split).strip()
        await bot.send_message(msg.channel, choice)