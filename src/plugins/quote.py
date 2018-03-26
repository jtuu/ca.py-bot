import re
from ..utils import discord_snowflake_to_datetime, random_date_between
from datetime import datetime, timedelta

trigger = re.compile("^!quote")

def format_quote(msg):
    return str(msg.author.name) + ": " + str(msg.content)

async def action(bot, msg):
    now = datetime.now()
    query_date = random_date_between(msg.channel.created_at, now)
    logs = bot.logs_from(msg.channel, after=query_date, limit=1)
    quote_msg = await logs.__anext__()
    await bot.send_message(msg.channel, format_quote(quote_msg))
