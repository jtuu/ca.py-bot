import os
import json
from datetime import datetime, timedelta
from random import randint
import asyncio
from discord_client import DiscordClient

def read_file_relative(path):
    return open(os.path.dirname(os.path.realpath(__file__)) + "/" + path)

# specific to discord
def snowflake_to_datetime(snowflake):
    return datetime.fromtimestamp(((int(snowflake) / 4194304) + 1420070400000) / 1000)

def random_date_between(a, b):
    max = int((b - a).total_seconds())
    d = timedelta(seconds=randint(0, max))
    return a + d

def format_quote(msg):
    return str(msg.author.name) + ": " + str(msg.content)

config = json.load(read_file_relative("../config.json"))
channel_geneses = json.load(read_file_relative("./channel_geneses.json"))

bot = DiscordClient(config)

@bot.Trigger("^!quote")
async def quote(msg):
    genesis_id = channel_geneses.get(msg.channel.id)

    if genesis_id:
        now = datetime.now()
        genesis = snowflake_to_datetime(genesis_id)
        query_date = random_date_between(genesis, now)

        logs = bot.logs_from(msg.channel, after=query_date, limit=1)
        quote_msg = await logs.__anext__()

        await bot.send_message(msg.channel, format_quote(quote_msg))
    else:
        print("No genesis found for %s (%s)" % (msg.channel.name, msg.channel.id))

bot.run()
