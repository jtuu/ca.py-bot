import re
import random
import sys

trigger = re.compile("^!dice")
match_pattern = re.compile(r"^!dice\s+(\d+)d(\d+)(?:([+-])(\d+))?")

async def action(bot, msg):
    match = match_pattern.match(msg.clean_content)

    if match:
        match_grps = match.groups()
        dice_count = int(match_grps[0])
        dice_sides = int(match_grps[1])

        if match_grps[2] and match_grps[3]:
            modifier_sign = match_grps[2]
            modifier = int(match_grps[3])
            if modifier_sign == "-":
                modifier = -modifier
        else:
            modifier = 0

        if dice_count < sys.maxsize and dice_sides < sys.maxsize and modifier < sys.maxsize:
            result = random.randint(dice_count, dice_count * dice_sides) + modifier
            await bot.send_message(msg.channel, str(result))