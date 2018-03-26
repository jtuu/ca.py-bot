import re
from ..utils import discord_snowflake_to_datetime, random_date_between
from datetime import datetime, timedelta
from random import randint

trigger = re.compile("^!quote")

def format_quote(msg):
    return str(msg.author.name) + ": " + str(msg.content)

max_log_length = 100

async def action(bot, msg):
    now = datetime.now()
    query_date = random_date_between(msg.channel.created_at, now)
    log_limit = randint(1, max_log_length)

    # for some reason the discord api returns the messages in reverse chronological order
    logs = bot.logs_from(msg.channel, after=query_date, limit=log_limit)
    quote_msg = await logs.__anext__()

    await bot.send_message(msg.channel, format_quote(quote_msg))
