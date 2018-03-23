from datetime import datetime, timedelta
from random import randint

def discord_snowflake_to_datetime(snowflake):
    return datetime.fromtimestamp(((int(snowflake) / 4194304) + 1420070400000) / 1000)

def random_date_between(a, b):
    max = int((b - a).total_seconds())
    d = timedelta(seconds=randint(0, max))
    return a + d
