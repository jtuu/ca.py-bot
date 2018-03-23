import json
import re
import os
from ..utils import discord_snowflake_to_datetime, random_date_between
from datetime import datetime, timedelta

trigger = re.compile("^!quote")

channel_geneses = json.load(open(os.path.abspath(os.path.dirname(__file__) + "/channel_geneses.json")))

def format_quote(msg):
    return str(msg.author.name) + ": " + str(msg.content)

async def action(bot, msg):
    genesis_id = channel_geneses.get(msg.channel.id)

    if genesis_id:
        now = datetime.now()
        genesis = discord_snowflake_to_datetime(genesis_id)
        query_date = random_date_between(genesis, now)

        logs = bot.logs_from(msg.channel, after=query_date, limit=1)
        quote_msg = await logs.__anext__()

        await bot.send_message(msg.channel, format_quote(quote_msg))
    else:
        print("No genesis found for %s (%s)" % (msg.channel.name, msg.channel.id))
