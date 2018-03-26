from datetime import datetime, timedelta
from random import randint
import urllib.parse
import re

def discord_snowflake_to_datetime(snowflake):
    return datetime.fromtimestamp(((int(snowflake) / 4194304) + 1420070400000) / 1000)

def random_date_between(a, b):
    max = int((b - a).total_seconds())
    d = timedelta(seconds=randint(0, max))
    return a + d

def querify(params, allow_duplicates=False):
    return "?" + urllib.parse.urlencode(params, doseq=allow_duplicates)

discord_escape_match_pattern = re.compile(r"([*_~`\[\]\(\)])")
discord_escape_replace_pattern = r"\\\g<1>"
def discord_escape(text):
    return discord_escape_match_pattern.sub(discord_escape_replace_pattern, text)
