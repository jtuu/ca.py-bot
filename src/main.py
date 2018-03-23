import json
from datetime import datetime
from .discord_client import DiscordClient
from .utils import read_file_relative, discord_snowflake_to_datetime, random_date_between

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
        genesis = discord_snowflake_to_datetime(genesis_id)
        query_date = random_date_between(genesis, now)

        logs = bot.logs_from(msg.channel, after=query_date, limit=1)
        quote_msg = await logs.__anext__()

        await bot.send_message(msg.channel, format_quote(quote_msg))
    else:
        print("No genesis found for %s (%s)" % (msg.channel.name, msg.channel.id))

bot.run()
